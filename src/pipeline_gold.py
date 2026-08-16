from pathlib import Path
import duckdb


def process_gold():
    silver_file = "data/2_silver/usd_cotacao_clean.parquet"
    if not Path(silver_file).exists():
        print("[GOLD] Arquivo Silver não encontrado.")
        return

    gold_dir = Path("data/3_gold")
    gold_dir.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect()

    # Query Analítica: Métricas de Câmbio + Média Móvel de 7 dias
    query_gold = f"""
        SELECT 
            dt_cotacao,
            cotacao_usd,
            ROUND(AVG(cotacao_usd) OVER (
                ORDER BY dt_cotacao 
                ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
            ), 4) AS media_movel_7d
        FROM '{silver_file}'
        ORDER BY dt_cotacao DESC
    """

    df_gold = con.execute(query_gold).df()
    df_gold.to_parquet(gold_dir / "usd_metrics.parquet", index=False)

    print("[GOLD] Visões analíticas da cotação geradas via DuckDB!")
    print("\n--- Últimas Cotações do Dólar com Média Móvel ---")
    print(df_gold.head(10))


if __name__ == "__main__":
    process_gold()