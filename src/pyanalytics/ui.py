from pyanalytics.core.exceptions import PyAnalyticsError

class UIFormatter:
    """Ferramenta para centralizar a criação de interfaces de texto bonitas via rich."""
    
    @staticmethod
    def print_error(console, message: str):
        console.print(f"[bold red]❌ ERRO:[/bold red] {message}")
        
    @staticmethod
    def print_success(console, message: str):
        console.print(f"[bold green]✔️ SUCESSO:[/bold green] {message}")
        
    @staticmethod
    def build_report_table(report_data: dict):
        from rich.table import Table
        
        table = Table(title="📊 Relatório Descritivo Base", show_header=True, header_style="bold magenta")
        table.add_column("Métrica", style="cyan", width=25)
        table.add_column("Valor", style="yellow")
        
        table.add_row("Total de Linhas", str(report_data["rows"]))
        table.add_row("Total de Colunas", str(report_data["columns"]))
        table.add_row("Colunas", ", ".join(report_data["columns_names"]))
        
        return table
