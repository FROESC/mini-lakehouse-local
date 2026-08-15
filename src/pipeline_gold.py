from pathlib import Path
import duckdb

def process_gold():
    silver_file = "data/2_silver/transactions_clean.parquet"
    if not Path(silver_file).exists():
        print("[GOLD] Arquivo Silver não encontrado.")
        return

    gold_dir = Path("data/3_gold")
    gold_dir.mkdir(parents=True, exist_ok=True)

    # Conexão com DuckDB em memória
    con = duckdb.connect()

    # Query 1: Faturamento e total de vendas por Categoria
    query_category = f"""
        SELECT 
            product_category,
            COUNT(transaction_id) AS total_vendas,
            ROUND(SUM(amount), 2) AS faturamento_total,
            ROUND(AVG(amount), 2) AS ticket_medio
        FROM '{silver_file}'
        GROUP BY product_category
        ORDER BY faturamento_total DESC
    """
    df_gold_category = con.execute(query_category).df()
    df_gold_category.to_parquet(gold_dir / "sales_by_category.parquet", index=False)

    # Query 2: Faturamento Diário
    query_daily = f"""
        SELECT 
            date,
            COUNT(transaction_id) AS total_transacoes,
            ROUND(SUM(amount), 2) AS faturamento_diario
        FROM '{silver_file}'
        GROUP BY date
        ORDER BY date ASC
    """
    df_gold_daily = con.execute(query_daily).df()
    df_gold_daily.to_parquet(gold_dir / "daily_sales.parquet", index=False)

    print("[GOLD] Visões analíticas geradas com sucesso via DuckDB!")
    print("\n--- Resumo: Vendas por Categoria ---")
    print(df_gold_category)

if __name__ == "__main__":
    process_gold()