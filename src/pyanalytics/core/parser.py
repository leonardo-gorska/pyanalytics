from pathlib import Path
import pandas as pd
from pyanalytics.core.exceptions import DataFormatError, FileLoadError

class DataParser:
    """Classe responsável por padronizar a ingestão de diferentes formatos de dados estruturados."""
    
    @staticmethod
    def load_data(file_path: str | Path) -> pd.DataFrame:
        """
        Lê um arquivo do sistema e o converte para um pandas DataFrame.
        
        Args:
            file_path: Caminho do arquivo a ser lido (.csv, .json, .parquet)
            
        Returns:
            pd.DataFrame contendo os dados.
            
        Raises:
            FileLoadError: Se o arquivo não existir ou não puder ser lido.
            DataFormatError: Se a extensão do arquivo não for suportada.
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileLoadError(f"O arquivo {path} não foi encontrado no sistema.")
            
        extension = path.suffix.lower()
        
        try:
            if extension == ".csv":
                return pd.read_csv(path)
            elif extension == ".json":
                return pd.read_json(path)
            elif extension == ".parquet":
                return pd.read_parquet(path)
            else:
                raise DataFormatError(f"Formato não suportado: {extension}. Use .csv, .json ou .parquet.")
        except DataFormatError:
            raise
        except Exception as e:
            raise FileLoadError(f"Falha ao carregar o arquivo {path}. Erro original: {str(e)}")
