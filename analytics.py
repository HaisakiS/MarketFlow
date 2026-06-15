import pandas as pd
import matplotlib.pyplot as plt
from database import connect_db

def plot_product_trend(target_product):
    conn = connect_db()
    if conn is None:
        print("Could not connect to the database.")
        return


    query = """
        SELECT ph.record_date, ph.recorded_price, ps.source_name
        FROM price_history ph
        JOIN price_sources ps ON ph.id_source = ps.id_source
        WHERE ph.product_name = ?
        ORDER BY ph.record_date ASC
    """

    """[TO DO: Differentiate variants, for now it doesn't take them in count]"""

    df = pd.read_sql_query(query, conn, params=(target_product,))
    conn.close()

    if df.empty:
        print(f"Not enough data registered for: {target_product}")
        return
    
    # SQL has Date as a Text, converting and saving it to date using pandas
    df['record_date'] = pd.to_datetime(df['record_date'], format='%d/%m/%Y')
    df = df.sort_values(by='record_date')

    #Basic plot using plt library
    plt.figure(figsize=(10, 6))

    for source in df['source_name'].unique():
        subset = df[df['source_name'] == source]
        plt.plot(
            subset['record_date'], 
            subset['recorded_price'], 
            marker='o', 
            linewidth=2, 
            label=source
        )

    plt.title(f"📈 Price Trend: {target_product}", fontsize=14, fontweight='bold')
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Average Price", fontsize=12)
    plt.legend(title="Sources", loc="best")
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plt.xticks(rotation=45) 
    plt.tight_layout()

    plt.show()