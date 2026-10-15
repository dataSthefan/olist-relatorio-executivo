"""Etapa 1 - Qualidade dos dados (governanca).
Uso: python3 -I src/01_quality.py data/raw
"""
import sys
from pathlib import Path
import pandas as pd

raw = Path(sys.argv[1])
files = {
    "customers": "olist_customers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
}
d = {k: pd.read_csv(raw / v) for k, v in files.items()}

print("== LINHAS / NULOS / DUPLICADOS ==")
for k, df in d.items():
    nulls = df.isna().sum()
    nulls = nulls[nulls > 0].to_dict()
    print(f"{k:12s} linhas={len(df):>8,} dup_linhas={df.duplicated().sum():>6,} nulos={nulls}")

o = d["orders"]
print("\n== STATUS DOS PEDIDOS ==")
print(o["order_status"].value_counts())

dcols = [c for c in o.columns if c.endswith("_date") or c.endswith("_timestamp") or c.endswith("_at")]
for c in dcols:
    o[c] = pd.to_datetime(o[c])
print("\nPeriodo:", o["order_purchase_timestamp"].min(), "->", o["order_purchase_timestamp"].max())
print("\nPedidos por mes (compra):")
print(o.set_index("order_purchase_timestamp").resample("MS").size().to_string())

print("\n== CHECAGENS DE CONSISTENCIA ==")
print("entrega < compra:", (o["order_delivered_customer_date"] < o["order_purchase_timestamp"]).sum())
print("entrega < postagem:", (o["order_delivered_customer_date"] < o["order_delivered_carrier_date"]).sum())
print("entregue sem data de entrega:", ((o.order_status == "delivered") & o.order_delivered_customer_date.isna()).sum())
print("data de entrega mas status != delivered:", ((o.order_status != "delivered") & o.order_delivered_customer_date.notna()).sum())

print("\n== INTEGRIDADE ENTRE TABELAS ==")
print("pedidos sem itens:", (~o.order_id.isin(d["items"].order_id)).sum())
print("pedidos sem pagamento:", (~o.order_id.isin(d["payments"].order_id)).sum())
print("pedidos sem review:", (~o.order_id.isin(d["reviews"].order_id)).sum())
print("itens sem produto:", (~d["items"].product_id.isin(d["products"].product_id)).sum())
print("itens sem seller:", (~d["items"].seller_id.isin(d["sellers"].seller_id)).sum())
print("pedidos sem cliente:", (~o.customer_id.isin(d["customers"].customer_id)).sum())
print("reviews: order_id duplicado:", d["reviews"].order_id.duplicated().sum())
print("customer_unique_id distintos:", d["customers"].customer_unique_id.nunique(), "de", len(d["customers"]))

print("\n== VALORES ==")
print(d["items"][["price", "freight_value"]].describe().to_string())
print("price <= 0:", (d["items"].price <= 0).sum())
print(d["payments"].payment_type.value_counts().to_string())
print("review_score:\n", d["reviews"].review_score.value_counts().sort_index().to_string())
