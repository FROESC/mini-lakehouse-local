from pathlib import Path
import pandas as pd


def process_silver(df_bronze: pd.DataFrame):
    if df_bronze is None or df_bronze.empty:
        print("[SILVER] Sem dados para processar.")
        return None

    df_silver = df_bronze.copy()

    # 1. Limpeza de duplicadas na coluna de data original
    df_silver = df_silver.drop_duplicates(subset=["data"])

    # 2. Tratamento do campo 'valor' (conversão para numérico seguro)
    # Substitui vírgula por ponto caso venha formatado como string "5,2510"
    df_silver["valor"] = df_silver["valor"].astype(str).str.replace(",", ".")

    # pd.to_numeric com errors='coerce' transforma qualquer texto inválido em NaN com segurança
    df_silver["valor"] = pd.to_numeric(df_silver["valor"], errors="coerce")

    # 3. Tratamento do campo 'data'
    df_silver["data"] = pd.to_datetime(df_silver["data"], format="%d/%m/%Y")

    # 4. Remove linhas onde a cotação ou a data ficaram nulas (NaN)
    df_silver = df_silver.dropna(subset=["data", "valor"])

    # 5. Renomear e ordenar
    df_silver = df_silver.rename(
        columns={"data": "dt_cotacao", "valor": "cotacao_usd"}
    )
    df_silver = df_silver.sort_values(by="dt_cotacao")

    # 6. Salvar na camada Silver em formato Parquet
    silver_dir = Path("data/2_silver")
    silver_dir.mkdir(parents=True, exist_ok=True)

    output_path = silver_dir / "usd_cotacao_clean.parquet"
    df_silver.to_parquet(output_path, index=False)

    print(
        f"[SILVER] Dados reais de câmbio salvos em: {output_path} ({len(df_silver)} registros)"
    )
    return df_silver