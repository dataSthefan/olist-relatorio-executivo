# Governança dos dados

## Fonte

Brazilian E-Commerce Public Dataset by Olist (Kaggle). Cerca de 100 mil pedidos entre 2016 e 2018, anonimizados. Nove tabelas: clientes, geolocalização, itens, pagamentos, avaliações, pedidos, produtos, vendedores e tradução de categorias.

## Tamanho das tabelas

| Tabela | Linhas |
|---|---|
| customers | 99.441 |
| orders | 99.441 |
| order_items | 112.650 |
| order_payments | 103.886 |
| order_reviews | 99.224 |
| products | 32.951 |
| sellers | 3.095 |
| geolocation | 1.000.163 (261.831 linhas duplicadas) |

## Problemas encontrados e tratamento

| Problema | Quantidade | Tratamento |
|---|---|---|
| Meses incompletos no início e no fim (set a dez/2016, set e out/2018) | Menos de 30 pedidos por mês, exceto out/2016 (324) | Tendências só de jan/2017 a ago/2018 |
| Pedidos cancelados ou indisponíveis | 1.234 | Excluídos da receita e das métricas |
| Pedidos sem itens | 775 (767 já cancelados ou indisponíveis; 8 a mais) | Fora da receita (não há valor) |
| Total de pedidos excluídos | 1.242 | Sobram 98.199 pedidos válidos |
| Pedidos sem data de entrega | 2.965 | Fora das métricas de entrega |
| Entregue antes da postagem | 23 | Mantidos; impacto desprezível |
| Entregue sem data de entrega | 8 | Fora das métricas de entrega |
| Pedidos com mais de uma avaliação | 551 | Usada a avaliação mais recente |
| Pedidos sem avaliação | 768 | Fora das métricas de nota |
| Produtos sem categoria | 610 | Categoria "unknown" |
| Geolocalização duplicada | 261.831 | Tabela não usada na análise |

## Definições das métricas

- **Pedido válido:** todos os pedidos, menos os com status `canceled` ou `unavailable`, e que tenham itens.
- **Receita:** soma de `price` dos itens dos pedidos válidos, sem frete.
- **Ticket médio:** receita dividida pelo número de pedidos válidos.
- **Atraso:** `order_delivered_customer_date` posterior a `order_estimated_delivery_date`.
- **Nota do pedido:** `review_score` mais recente do pedido.
- **Cliente único:** `customer_unique_id`. Um mesmo cliente tem vários `customer_id`, um por pedido.
- **Recompra:** cliente com dois ou mais pedidos válidos.
- **Vendedor e categoria do pedido:** os do primeiro item do pedido.

## Limitações

- Clientes que fizeram a primeira compra em 2018 tiveram menos tempo para voltar, o que pode reduzir a taxa de recompra.
- A atribuição de vendedor e categoria pelo primeiro item simplifica pedidos com vários itens.
- O cruzamento com a população mostra associação entre regiões, e não causa.

## Dado externo

IBGE, Censo Demográfico 2022, população residente por unidade da federação. Conferência: a soma dos 27 estados é 203.080.756, igual ao total divulgado.
