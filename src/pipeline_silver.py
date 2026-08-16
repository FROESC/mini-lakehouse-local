from pathlib import Path
import pandas as pd


def process_silver(df_bronze: pd.DataFrame):
    if df_bronze is None or df_bronze.empty:
        print("[SILVER] Sem dados para processar.")
        return None

    df_silver = df_bronze.copy()

    # 1. Limpeza de duplicadas
    df_silver = df_silver.drop_duplicates(subset=["data"])

    # 2. Conversão e tratamento de tipos (Casting)
    # A API retorna data como 'DD/MM/YYYY' e valor como string "5.2510"
    df_silver["data"] = pd.to_datetime(df_silver["data"], format="%d/%m/%Y")
    df_silver["valor"] = df_silver["valor"].astype(float)

    # Renomeando colunas para o padrão do pipeline
    df_silver = df_silver.rename(
        columns={"data": "dt_cotacao", "valor": "cotacao_usd"}
    )

    # Ordenar por data
    df_silver = df_silver.sort_values(by="dt_cotacao")

    # 3. Salvar na camada Silver em formato Parquet
    silver_dir = Path("data/2_silver")
    silver_dir.mkdir(parents=True, exist_ok=True)

    output_path = silver_dir / "usd_cotacao_clean.parquet"
    df_silver.to_parquet(output_path, index=False)

    print(
        f"[SILVER] Dados reais de câmbio salvos em: {output_path} ({len(df_silver)} registros)"
    )
    return df_silver