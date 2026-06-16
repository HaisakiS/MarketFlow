import pandas as pd
import matplotlib.pyplot as plt
from database import connect_db

def plot_product_trend(target_product):
    conn = connect_db()
    if conn is None:
        print("Could not connect to the database.")
        return

    query = """
        SELECT ph.record_date, ph.recorded_price, ph.variant, ps.source_name
        FROM price_history ph
        JOIN price_sources ps ON ph.id_source = ps.id_source
        WHERE ph.product_name = ?
        ORDER BY ph.record_date ASC
    """

    df = pd.read_sql_query(query, conn, params=(target_product,))
    conn.close()

    if df.empty:
        print(f"Not enough data registered for: {target_product}")
        return
    
    # SQL has Date as a Text, converting and saving it to date using pandas
    df['record_date'] = pd.to_datetime(df['record_date'], format='%d/%m/%Y')
    df = df.sort_values(by='record_date')

    #Differentiate variants of teh same product
    df['legend_label'] = df['source_name'] + " (" + df['variant'] + ")"

    #Basic plot using plt library
    plt.figure(figsize=(10, 6))

    for label in df['legend_label'].unique():
        subset = df[df['legend_label'] == label]
        plt.plot(
            subset['record_date'], 
            subset['recorded_price'], 
            marker='o', 
            linewidth=2, 
            label=label
        )

    plt.title(f"📈 Price Trend: {target_product}", fontsize=14, fontweight='bold')
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Average Price", fontsize=12)
    plt.legend(title="Sources & Variants", loc="best")
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plt.xticks(rotation=45) 
    plt.tight_layout()

    plt.show()