import pandas as pd
from typing import Dict, Any

class DataMetrics:
    """Ferramenta para extrair métricas de relatórios descritivos a partir de DataFrames."""
    
    @staticmethod
    def descriptive_report(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Gera um relatório descritivo simples sobre o DataFrame fornecido.
        
        Args:
            df: DataFrame com os dados alvo.
            
        Returns:
            Dicionário contendo sumário de linhas, colunas, num nulos, e descrição estatística se aplicável.
        """
        report: Dict[str, Any] = {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "columns_names": list(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
        }
        
        # Filtrar apenas as colunas numéricas para gerar estatísticas (média, sd, min, max, etc)
        numeric_df = df.select_dtypes(include=['number'])
        if not numeric_df.empty:
            # fillna(0) ou dropna() na description não é estritamente necessário, mas podemos converter para dit
            stats = numeric_df.describe().to_dict()
            report["numeric_stats"] = stats
        else:
            report["numeric_stats"] = {}
            
        return report
