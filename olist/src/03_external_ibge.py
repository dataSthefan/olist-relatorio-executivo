"""Etapa 3 - Dado externo: populacao por UF (IBGE, Censo 2022) x pedidos Olist.
Uso: python3 -I src/03_external_ibge.py data/processed/orders_master.csv data/external/ibge_populacao_uf_2022.csv
"""
import sys
import pandas as pd
m = pd.read_csv(sys.argv[1], parse_dates=["month"])
pop = pd.read_csv(sys.argv[2])
print("Soma populacao (esperado 203.080.756):", f"{pop.populacao_2022.sum():,}")
P = m[m.valid & (m.month >= "2017-01-01") & (m.month <= "2018-08-01")]
g = P.groupby("customer_state").agg(pedidos=("order_id", "count"), receita=("price", "sum")).reset_index()
d = pop.merge(g, left_on="uf", right_on="customer_state", how="left").fillna({"pedidos": 0, "receita": 0})
d["pct_pop"] = d.populacao_2022 / d.populacao_2022.sum() * 100
d["pct_pedidos"] = d.pedidos / d.pedidos.sum() * 100
d["pedidos_100mil"] = d.pedidos / d.populacao_2022 * 1e5
d["receita_hab"] = d.receita / d.populacao_2022
pd.set_option("display.width", 200)
print(d.sort_values("pedidos_100mil", ascending=False)[["uf", "populacao_2022", "pct_pop", "pct_pedidos", "pedidos", "pedidos_100mil", "receita_hab"]].round(2).to_string(index=False))
nat = d.pedidos.sum() / d.populacao_2022.sum() * 1e5
print(f"\nMedia nacional: {nat:.1f} pedidos por 100 mil hab. | pedidos jan17-ago18: {int(d.pedidos.sum()):,}")
reg = {"Nordeste": ["MA","PI","CE","RN","PB","PE","AL","SE","BA"], "Sudeste": ["SP","RJ","MG","ES"], "Sul": ["PR","SC","RS"], "Norte": ["AC","AP","AM","PA","RO","RR","TO"], "Centro-Oeste": ["DF","GO","MT","MS"]}
for r, ufs in reg.items():
    x = d[d.uf.isin(ufs)]
    print(f"{r:13s} pop={x.populacao_2022.sum()/d.populacao_2022.sum():.1%} pedidos={x.pedidos.sum()/d.pedidos.sum():.1%} ped/100mil={x.pedidos.sum()/x.populacao_2022.sum()*1e5:.1f}")
d.to_csv("data/processed/uf_populacao_pedidos.csv", index=False)
