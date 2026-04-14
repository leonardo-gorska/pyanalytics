import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from pyanalytics.core.exceptions import PyAnalyticsError

class DataPlotter:
    """Motor dedicado para renderizar gráficos de DataFrames do pandas."""
    
    @staticmethod
    def export_plot(df: pd.DataFrame, plot_type: str, col_x: str, col_y: str, output_path: str | Path):
        """
        Salva uma visualização simplificada do tipo de gráfico solicitado em arquivo .png.
        
        Args:
            df: DataFrame carregado.
            plot_type: Tipo do gráfico ('bar', 'scatter', 'line').
            col_x: Coluna para o eixo X.
            col_y: Coluna para o eixo Y.
            output_path: Caminho de saída onde salvar o arquivo gerado.
        """
        if col_x not in df.columns or col_y not in df.columns:
            raise PyAnalyticsError(f"A(s) coluna(s) especificadas ({col_x}, {col_y}) não existem no DataFrame.")
            
        fig, ax = plt.subplots(figsize=(10, 6))
        
        try:
            if plot_type == "bar":
                # Agrupa primeiro para evitar excesso de barras se tiver muitas rows
                grouped = df.groupby(col_x, as_index=False)[col_y].sum()
                ax.bar(grouped[col_x].astype(str), grouped[col_y], color='cornflowerblue')
            elif plot_type == "scatter":
                ax.scatter(df[col_x], df[col_y], color='tomato', alpha=0.7)
            elif plot_type == "line":
                ax.plot(df[col_x].astype(str), df[col_y], color='mediumseagreen', marker='o')
            else:
                raise PyAnalyticsError(f"Tipo de gráfico não suportado: {plot_type}. Use 'bar', 'line' ou 'scatter'.")
                
            ax.set_title(f"Gráfico de {plot_type.capitalize()}: {col_y} vs {col_x}", fontsize=14, fontweight='bold')
            ax.set_xlabel(col_x, fontsize=12)
            ax.set_ylabel(col_y, fontsize=12)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            
            # Gira os rótulos do eixo X caso sejam muitos ou longos
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            out_file = Path(output_path)
            # Cria possiveis diretorios parentes se n exitir
            out_file.parent.mkdir(parents=True, exist_ok=True)
            
            fig.savefig(out_file, dpi=300)
            
        except Exception as e:
            raise PyAnalyticsError(f"Erro ao gerar gráfico: {str(e)}")
        finally:
            plt.close(fig) # Prevenir memory leaks
