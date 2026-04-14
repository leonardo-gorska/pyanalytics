import pytest
import pandas as pd
from pathlib import Path
from typer.testing import CliRunner
from pyanalytics.cli import app
from pyanalytics.core.parser import DataParser
from pyanalytics.core.exceptions import FileLoadError, DataFormatError

runner = CliRunner()

@pytest.fixture
def sample_csv(tmp_path):
    """Cria um CSV temporário para os testes."""
    file_path = tmp_path / "data.csv"
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35]
    })
    df.to_csv(file_path, index=False)
    return file_path

def test_parser_valid_csv(sample_csv):
    """Valida se o DataParser carrega o formato básico."""
    df = DataParser.load_data(sample_csv)
    assert not df.empty
    assert len(df) == 3
    assert "name" in df.columns

def test_parser_unsupported_format(tmp_path):
    """Garante que a Exceção Customizada é atirada para extensões sem suporte."""
    file_path = tmp_path / "data.xml"
    file_path.write_text("<data></data>")
    
    with pytest.raises(DataFormatError) as exc:
        DataParser.load_data(file_path)
    assert "Formato não suportado" in str(exc.value)

def test_cli_report(sample_csv):
    """Testa se o subcomando report devolve status code 0 num arquivo válido."""
    result = runner.invoke(app, ["report", str(sample_csv)])
    assert result.exit_code == 0
    assert "Total de Linhas" in result.stdout
    assert "lido com sucesso" in result.stdout

def test_cli_filter(sample_csv):
    """Valida a funcionalidade de filtragem da linha de comando."""
    result = runner.invoke(app, ["filter-data", str(sample_csv), "--col", "age", "--val", "30"])
    assert result.exit_code == 0
    assert "Encontradas 1 linhas" in result.stdout
    assert "Bob" in result.stdout

def test_cli_plot_missing_columns(sample_csv, tmp_path):
    """Testa se o CLI do plotter segura as pontas em caso de colunas que não existem."""
    out_file = tmp_path / "out.png"
    result = runner.invoke(app, ["plot", str(sample_csv), "-t", "bar", "-x", "wrong_col", "-y", "age", "-o", str(out_file)])
    assert result.exit_code == 1
    assert "ERRO:" in result.stdout
