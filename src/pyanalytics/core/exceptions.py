class PyAnalyticsError(Exception):
    """Exceção base para o PyAnalytics. Exceções herdadas devem ser interceptadas pelo CLI."""
    pass

class DataFormatError(PyAnalyticsError):
    """Levantada quando o formato do arquivo não é suportado pelo PyAnalytics."""
    pass

class MissingColumnError(PyAnalyticsError):
    """Levantada quando uma operação solicita uma coluna que não existe no DataFrame."""
    pass

class FileLoadError(PyAnalyticsError):
    """Levantada quando ocorre um erro na leitura do arquivo (ex: arquivo não encontrado)."""
    pass
