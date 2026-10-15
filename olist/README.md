# Olist: relatório executivo para investidores

Projeto do Tech Challenge da Fase 1 (Pós-graduação em Análise de Dados). A análise transforma dados de pedidos da Olist em uma narrativa para investidores: o crescimento de 2017 a 2018, por que ele estagnou e o que fazer para retomá-lo.

**Autor:** [seu nome]

## Principais achados

- A receita de jan–ago/2018 foi 138% maior que a de jan–ago/2017, mas o volume mensal está parado desde janeiro de 2018.
- São Paulo responde por 38% da receita; 10% dos vendedores geram 67% dela.
- O Nordeste tem 27% da população e 9,5% dos pedidos (17 pedidos por 100 mil habitantes, contra 79 no Sudeste).
- O atraso na entrega derruba a nota: de 4,3 (no prazo) para 1,7 (mais de 7 dias de atraso).
- Só 3% dos clientes compram uma segunda vez, e a nota da primeira compra não muda isso.

## Como reproduzir

1. Baixe o dataset no Kaggle: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).
2. Coloque os 9 arquivos CSV em `data/raw/`.
3. Instale as dependências e rode os scripts, sempre a partir da raiz do repositório:

```bash
pip install -r requirements.txt

python src/01_quality.py data/raw
python src/02_build_and_eda.py data/raw data/processed
python src/03_external_ibge.py data/processed/orders_master.csv data/external/ibge_populacao_uf_2022.csv
```

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `src/01_quality.py` | Qualidade dos dados: nulos, duplicados, status, integridade entre tabelas |
| `src/02_build_and_eda.py` | Tabela única de pedidos e análise exploratória (crescimento, logística, clientes) |
| `src/03_external_ibge.py` | Cruzamento com a população por estado do IBGE |
| `data/raw/` | CSVs originais da Olist (não versionados) |
| `data/external/` | População por estado, Censo 2022 do IBGE |
| `data/processed/` | Tabelas geradas pelos scripts (não versionadas) |
| `docs/governanca.md` | Dicionário, regras de limpeza e problemas encontrados |

## Dado externo

População por unidade da federação, Censo Demográfico 2022 do IBGE (total de 203.080.756 habitantes). O arquivo está em `data/external/ibge_populacao_uf_2022.csv`.

## Apresentação e vídeo

- Apresentação executiva: [link]
- Vídeo executivo (até 5 minutos): [link]
