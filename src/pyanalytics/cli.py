import typer
from pathlib import Path
from rich.console import Console

# Core imports
from pyanalytics.core.parser import DataParser
from pyanalytics.core.exceptions import PyAnalyticsError
from pyanalytics.core.metrics import DataMetrics
from pyanalytics.core.plotter import DataPlotter
from pyanalytics.ui import UIFormatter

app = typer.Typer(
    name="pyanalytics",
    help="Ferramenta CLI corporativa para Análise Exploratória de Dados no Terminal.",
    add_completion=False,
)

console = Console()

@app.command()
def report(
    file_path: Path = typer.Argument(..., help="Caminho para o arquivo de dados (.csv, .json, .parquet)"),
):
    """
    Carrega o arquivo especificado e exibe um relatório descritivo das métricas base.
    """
    try:
        df = DataParser.load_data(file_path)
        report_data = DataMetrics.descriptive_report(df)
        
        table = UIFormatter.build_report_table(report_data)
        
        UIFormatter.print_success(console, f"Arquivo '{file_path.name}' lido com sucesso.")
        console.print(table)
        
    except PyAnalyticsError as e:
        UIFormatter.print_error(console, str(e))
        raise typer.Exit(code=1)
    except Exception as e:
        UIFormatter.print_error(console, f"Erro inesperado: {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def filter_data(
    file_path: Path = typer.Argument(..., help="Caminho para o arquivo"),
    column: str = typer.Option(..., "--col", "-c", help="Nome da coluna a ser filtrada"),
    value: str = typer.Option(..., "--val", "-v", help="Valor esperado"),
    head: int = typer.Option(5, "--head", help="Número de linhas a exibir na pré-visualização"),
):
    """
    Filtra dados de um arquivo baseado em colunas e valores exatos.
    """
    from rich.table import Table
    try:
        df = DataParser.load_data(file_path)
        
        if column not in df.columns:
            UIFormatter.print_error(console, f"A coluna '{column}' não existe no DataFrame.")
            raise typer.Exit(code=1)
            
        # Converte o valor baseado no tipo atual da coluna
        # Forma simplificada: converte a coluna pra string para comparar
        filtered_df = df[df[column].astype(str) == value]
        
        UIFormatter.print_success(console, f"Encontradas {len(filtered_df)} linhas onde {column} == {value}.")
        
        # Build table for head
        if not filtered_df.empty:
            preview = filtered_df.head(head)
            table = Table(title=f"Pré-visualização (Top {head})")
            
            # Adiciona as colunas do preview na tabela. Para evitar tabelas muito largas, limitamos as colunas.
            cols_to_show = list(preview.columns)[:10] 
            for col_name in cols_to_show:
                table.add_column(str(col_name))
                
            for _, row in preview.iterrows():
                row_str = [str(item) for item in list(row)[:10]]
                table.add_row(*row_str)
                
            if len(preview.columns) > 10:
                console.print("[dim]Aviso: Ocultando algumas colunas na pré-visualização...[/dim]")
                
            console.print(table)
            
    except PyAnalyticsError as e:
        UIFormatter.print_error(console, str(e))
        raise typer.Exit(code=1)
    except Exception as e:
        UIFormatter.print_error(console, f"Erro inesperado: {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def plot(
    file_path: Path = typer.Argument(..., help="Caminho para o arquivo"),
    plot_type: str = typer.Option(..., "--type", "-t", help="Tipo de gráfico (bar, scatter, line)"),
    col_x: str = typer.Option(..., "--col-x", "-x", help="Coluna do Eixo X"),
    col_y: str = typer.Option(..., "--col-y", "-y", help="Coluna do Eixo Y"),
    output: Path = typer.Option("chart.png", "--out", "-o", help="Caminho do arquivo de saída .png"),
):
    """
    Gera um gráfico analítico e exporta para PNG sem travar o terminal.
    """
    try:
        df = DataParser.load_data(file_path)
        
        UIFormatter.print_success(console, f"Preparando gráfico '{plot_type}'...")
        DataPlotter.export_plot(df, plot_type, col_x, col_y, output)
        
        UIFormatter.print_success(console, f"Excelente! Seu gráfico está pronto: {output.absolute()}")
            
    except PyAnalyticsError as e:
        UIFormatter.print_error(console, str(e))
        raise typer.Exit(code=1)
    except Exception as e:
        UIFormatter.print_error(console, f"Erro inesperado no pipeline de imagem: {str(e)}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
