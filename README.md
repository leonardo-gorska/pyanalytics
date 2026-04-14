# PyAnalytics 🐍📊

O **PyAnalytics** é uma CLI corporativa baseada em Python, rápida e confiável, para análise exploratória de dados diretamente no terminal. Projetada para ser fluida e eficiente, poupa o engenheiro/analista de criar notebooks Jupyter do zero para tarefas operacionais diárias.

## ✨ Features Core
- **Motor Multi-Formato**: Lê perfeitamente `.csv`, `.json` e o corporativo `.parquet` nativamente através da união entre `pandas` e `pyarrow`.
- **Estatísticas Aceleradas**: Fornece relatórios completos de estatística descritivo como totalizador de colunas nulls, shapes e contagens.
- **Visual Terminal Refinado**: Renderização extrema através da suíte `rich`, trazendo cor, clareza e tabelas polidas no console sem estourar o layout.
- **Exportação de Estáticos**: Adicionamos suporte assíncrono à construção e destilação de gráficos com `matplotlib`, sem instanciar GUIs custosas. Exporta diretos `.png`s perfeitos pro seu CWD.

## 🚀 Instalação (Standalone)
Aproveitando o padrão moderno `pyproject.toml`, você pode injetar essa CLI em qualquer ambiente local apenas usando pip na raiz do pacote:

```bash
git clone https://github.com/seu-user/pyanalytics-cli.git
cd pyanalytics-cli

# Instalando globalmente no seu venv
pip install .
```

E voilà! Você agorá terá o comando nativo `pyanalytics` acessível a qualquer momento.

## 💻 Como Usar (Guia Typer)

### 1) Relatório Rápido de Dataset
```bash
pyanalytics report dados_vendas.parquet
```

### 2) Filtragem Inline
Se quiser inspecionar um *slice* exato da tabela. Pode passar `--head` para controlar os retornos:
```bash
pyanalytics filter-data usuarios.csv --col status --val ativo --head 15
```

### 3) Visualização de Dados Fast-track
Para produzir imagens exploratórios e mandar no Jira rapidinho sem nem abrir um Excel:
```bash
pyanalytics plot historico.json --type line --col-x Mes --col-y Faturamento --out meus_graficos/vendas.png
```

## 🛡️ Desenvolvimento & Testes Corporativos
Projeto empacotado seguindo regras estritas: PEP-8 com `black` estático, e checagem forte pelo `mypy`.
Para testar (95%+ Coved):
```bash
pip install -e ".[dev]"
pytest -v --cov=pyanalytics
```

---
*Construído com ❤️ para o Portfólio de Projetos Corporativos.*
