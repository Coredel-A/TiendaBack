import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

from a_ordenes.models import OrdenDetalle

def cargar_datos():
    detalles = OrdenDetalle.objects.select_related('orden', 'producto').all()

    data = {}

    for detalle in detalles:
        orden_id = detalle.orden.id
        producto_nombre = detalle.producto.nombre

        if orden_id not in data:
            data[orden_id] = set()

        data[orden_id].add(producto_nombre)

    return list(data.values())

def preparar_dataframe(lista_ordenes):
    all_items = set()
    for productos in lista_ordenes:
        all_items.update(productos)

    all_items = list(all_items)

    encoded_vals = []

    for productos in lista_ordenes:
        row = {}
        for item in all_items:
            row[item] = item in productos
        encoded_vals.append(row)

    return pd.DataFrame(encoded_vals)

def generar_reglas(df):
    frequent_itemsets = apriori(df, min_support=0.2, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

    return rules

def main():
    lista_ordenes = cargar_datos()
    df = preparar_dataframe(lista_ordenes)
    reglas = generar_reglas(df)

    print(reglas[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

if __name__ == "__main__":
    main()
