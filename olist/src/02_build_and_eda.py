"""Etapa 2 - Tabela unica de pedidos + analise exploratoria inicial.
Uso: python3 -I src/02_build_and_eda.py data/raw data/processed
"""
import sys
from pathlib import Path
import pandas as pd

raw, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
r = lambda n: pd.read_csv(raw / n)

orders = r("olist_orders_dataset.csv")
items = r("olist_order_items_dataset.csv")
pay = r("olist_order_payments_dataset.csv")
rev = r("olist_order_reviews_dataset.csv")
cust = r("olist_customers_dataset.csv")
prod = r("olist_products_dataset.csv")
sell = r("olist_sellers_dataset.csv")
tr = r("product_category_name_translation.csv")

for c in ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date",
          "order_delivered_customer_date", "order_estimated_delivery_date"]:
    orders[c] = pd.to_datetime(orders[c])

# --- agregados por pedido ---
it = items.groupby("order_id").agg(
    n_items=("order_item_id", "count"),
    n_sellers=("seller_id", "nunique"),
    price=("price", "sum"),
    freight=("freight_value", "sum"),
).reset_index()
pg = pay.groupby("order_id").agg(
    payment_value=("payment_value", "sum"),
    max_installments=("payment_installments", "max"),
    main_payment=("payment_type", lambda s: s.mode().iat[0]),
).reset_index()
# review: ultima resposta por pedido (551 pedidos tem mais de uma)
rev["review_answer_timestamp"] = pd.to_datetime(rev["review_answer_timestamp"])
rv = (rev.sort_values("review_answer_timestamp").drop_duplicates("order_id", keep="last")
      [["order_id", "review_score"]])
# categoria e seller do 1o item (para analises por categoria/UF vendedor)
first = (items.sort_values(["order_id", "order_item_id"]).drop_duplicates("order_id")
         .merge(prod[["product_id", "product_category_name"]], on="product_id", how="left")
         .merge(tr, on="product_category_name", how="left")
         .merge(sell[["seller_id", "seller_state"]], on="seller_id", how="left"))
first["category"] = first["product_category_name_english"].fillna(first["product_category_name"]).fillna("unknown")
first = first[["order_id", "seller_id", "seller_state", "category"]]

df = (orders.merge(cust, on="customer_id", how="left")
      .merge(it, on="order_id", how="left")
      .merge(pg, on="order_id", how="left")
      .merge(rv, on="order_id", how="left")
      .merge(first, on="order_id", how="left"))

df["month"] = df["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp()
df["valid"] = ~df["order_status"].isin(["canceled", "unavailable"]) & df["price"].notna()
d = df["order_delivered_customer_date"]
df["lead_days"] = (d - df["order_purchase_timestamp"]).dt.total_seconds() / 86400
df["approval_hours"] = (df["order_approved_at"] - df["order_purchase_timestamp"]).dt.total_seconds() / 3600
df["post_days"] = (df["order_delivered_carrier_date"] - df["order_approved_at"]).dt.total_seconds() / 86400
df["carrier_days"] = (d - df["order_delivered_carrier_date"]).dt.total_seconds() / 86400
df["promised_days"] = (df["order_estimated_delivery_date"] - df["order_purchase_timestamp"]).dt.total_seconds() / 86400
df["delay_days"] = (d - df["order_estimated_delivery_date"]).dt.total_seconds() / 86400
df["late"] = df["delay_days"] > 0
df.to_csv(out / "orders_master.csv", index=False)
print("orders_master:", df.shape, "| pedidos validos:", int(df.valid.sum()))

pd.set_option("display.width", 200)
P = df[df.valid & (df.month >= "2017-01-01") & (df.month <= "2018-08-01")]

print("\n== 1. CRESCIMENTO (jan/17 a ago/18, pedidos validos) ==")
m = P.groupby("month").agg(pedidos=("order_id", "count"), receita=("price", "sum"),
                           frete=("freight", "sum")).assign(ticket=lambda x: x.receita / x.pedidos)
print(m.round(1).to_string())
a17 = P[(P.month >= "2017-01-01") & (P.month <= "2017-08-01")]
a18 = P[(P.month >= "2018-01-01") & (P.month <= "2018-08-01")]
print(f"\nJan-Ago 2017: pedidos={len(a17):,} receita={a17.price.sum():,.0f} ticket={a17.price.sum()/len(a17):.1f}")
print(f"Jan-Ago 2018: pedidos={len(a18):,} receita={a18.price.sum():,.0f} ticket={a18.price.sum()/len(a18):.1f}")
print(f"Crescimento pedidos: {len(a18)/len(a17)-1:.1%} | receita: {a18.price.sum()/a17.price.sum()-1:.1%}")
print(f"Receita total (pedidos validos, todo periodo): {df[df.valid].price.sum():,.0f}")

print("\n== Categorias (top 10, receita, % do total) ==")
c = df[df.valid].groupby("category").agg(pedidos=("order_id", "count"), receita=("price", "sum"))
c["pct"] = c.receita / c.receita.sum() * 100
print(c.sort_values("receita", ascending=False).head(10).round(1).to_string())
print("\n== UF do cliente (top 8) ==")
s = df[df.valid].groupby("customer_state").agg(pedidos=("order_id", "count"), receita=("price", "sum"))
s["pct"] = s.receita / s.receita.sum() * 100
print(s.sort_values("receita", ascending=False).head(8).round(1).to_string())
print("\n== Sellers: concentracao ==")
sv = df[df.valid].groupby("seller_id").price.sum().sort_values(ascending=False)
print(f"sellers com venda (1o item): {len(sv):,} | top 10% sellers = {sv.head(int(len(sv)*0.1)).sum()/sv.sum():.1%} da receita | top 1% = {sv.head(int(len(sv)*0.01)).sum()/sv.sum():.1%}")

print("\n== 2. LOGISTICA (pedidos entregues) ==")
E = df[(df.order_status == "delivered") & df.lead_days.notna()]
print(E[["approval_hours", "post_days", "carrier_days", "lead_days", "promised_days", "delay_days"]].describe().round(1).to_string())
print(f"% entregues com atraso (apos data estimada): {E.late.mean():.1%}")
print("\nAtraso por UF (cliente) - top piores, UFs com >=500 pedidos:")
u = E.groupby("customer_state").agg(n=("order_id", "count"), lead=("lead_days", "mean"),
                                    late=("late", "mean"), frete=("freight", "mean"), nota=("review_score", "mean"))
print(u[u.n >= 500].sort_values("late", ascending=False).round(3).to_string())
print("\nNota media por situacao da entrega:")
E2 = E[E.review_score.notna()].copy()
E2["faixa"] = pd.cut(E2.delay_days, [-1e9, 0, 3, 7, 1e9], labels=["no prazo/antes", "atraso 0-3d", "atraso 3-7d", "atraso >7d"])
print(E2.groupby("faixa", observed=True).agg(n=("order_id", "count"), nota=("review_score", "mean"),
      pct_nota1_2=("review_score", lambda x: (x <= 2).mean())).round(3).to_string())
print(f"correlacao delay_days x nota: {E2[['delay_days','review_score']].corr().iat[0,1]:.3f}")
print(f"correlacao lead_days x nota: {E2[['lead_days','review_score']].corr().iat[0,1]:.3f}")

print("\n== 3. CLIENTE ==")
V = df[df.valid]
nped = V.groupby("customer_unique_id").order_id.nunique()
print(f"clientes unicos: {len(nped):,} | com 2+ pedidos: {(nped>=2).mean():.2%} | 3+: {(nped>=3).mean():.2%}")
print("Nota media geral:", round(df.review_score.mean(), 2), "| % nota 4-5:", f"{(df.review_score>=4).sum()/df.review_score.notna().sum():.1%}",
      "| % nota 1-2:", f"{(df.review_score<=2).sum()/df.review_score.notna().sum():.1%}")
# recompra x nota do 1o pedido
first_o = V.sort_values("order_purchase_timestamp").drop_duplicates("customer_unique_id")
first_o = first_o.assign(recompra=first_o.customer_unique_id.map(nped) >= 2)
print("\nRecompra por nota do 1o pedido:")
print(first_o[first_o.review_score.notna()].groupby("review_score").recompra.agg(["count", "mean"]).round(4).to_string())
print("\nMeio de pagamento (pedidos validos):")
print(V.main_payment.value_counts(normalize=True).round(3).to_string())
print("Parcelas medias (cartao):", round(V[V.main_payment == "credit_card"].max_installments.mean(), 1))
print("Frete / preco medio:", f"{V.freight.sum()/V.price.sum():.1%}")
