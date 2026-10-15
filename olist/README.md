# Olist: relatório executivo para investidores

Trabalho do Tech Challenge da Fase 1 da pós-graduação em Análise de Dados (POSTECH). Usei os pedidos da Olist entre 2016 e 2018 para montar um relatório para investidores. A pergunta que me guiou foi: a empresa cresceu muito, então por que o crescimento parou e o que ela pode fazer para voltar a crescer?

Autor: Harold Sthefan

## O que encontrei

- De janeiro a agosto de 2018, a receita foi 138% maior que no mesmo período de 2017. Mas desde janeiro de 2018 o número de pedidos por mês quase não sobe (fica entre 6 e 7 mil).
- São Paulo concentra 38% da receita, e 10% dos vendedores respondem por 67% dela.
- O Nordeste tem 27% da população do país e só 9,5% dos pedidos.
- Quando a entrega atrasa mais de 7 dias, a nota média cai de 4,3 para 1,7.
- Só 3% dos clientes compram uma segunda vez. Eu esperava que quem deu nota alta voltasse mais, mas a taxa é parecida em todas as notas.

## Como rodar

Os CSVs não estão aqui porque são grandes. Para repetir a análise:

1. Baixe os dados no Kaggle: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) e coloque os 9 arquivos em `data/raw/`.
2. Instale o pandas:

```
pip install -r requirements.txt
```

3. Rode os scripts nesta ordem, a partir da pasta principal do projeto:

```
python src/01_quality.py data/raw
python src/02_build_and_eda.py data/raw data/processed
python src/03_external_ibge.py data/processed/orders_master.csv data/external/ibge_populacao_uf_2022.csv
```

## O que tem em cada pasta

- `src/`: os três scripts. O primeiro checa a qualidade dos dados, o segundo junta as tabelas e calcula as métricas, o terceiro cruza com a população.
- `docs/governanca.md`: problemas que encontrei nos dados, como tratei cada um e como defini as métricas.
- `data/external/`: população por estado, do Censo 2022 do IBGE (usei como dado externo).

## Cuidados com os números

- Nas tendências usei só janeiro de 2017 a agosto de 2018, porque os outros meses têm pouquíssimos pedidos.
- Tirei os pedidos cancelados, indisponíveis e sem itens (1.242 de 99.441).
- A comparação com a população mostra que baixo volume e atraso aparecem nas mesmas regiões, mas não prova que um causa o outro.
- A recompra dos clientes de 2018 pode estar um pouco baixa, porque eles tiveram menos tempo para voltar.

## Apresentação e vídeo

- Apresentação: [link]
- Vídeo (até 5 minutos): [link]
