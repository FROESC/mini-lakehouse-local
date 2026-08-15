from pathlib import Path
import pandas as pd

def process_silver(df_bronze: pd.DataFrame):
    if df_bronze is None or df_bronze.empty:
        print("[SILVER] Sem dados para processar.")
        return None

    df_silver = df_bronze.copy()
    
    # 1. Remoção de duplicadas exatas
    initial_len = len(df_silver)
    df_silver = df_silver.drop_duplicates(subset=["transaction_id"])
    print(f"[SILVER] Duplicadas removidas: {initial_len - len(df_silver)}")
    
    # 2. Filtrar apenas transações concluídas
    df_silver = df_silver[df_silver["status"] == "COMPLETED"]
    
    # 3. Conversão de tipos de dados (Casting)
    df_silver["timestamp"] = pd.to_datetime(df_silver["timestamp"])
    df_silver["amount"] = df_silver["amount"].astype(float)
    df_silver["date"] = df_silver["timestamp"].dt.date
    
    # 4. Salvar na camada Silver em formato Parquet
    silver_dir = Path("data/2_silver")
    silver_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = silver_dir / "transactions_clean.parquet"
    df_silver.to_parquet(output_path, index=False)
    
    print(f"[SILVER] Dados limpos salvos em: {output_path} ({len(df_silver)} registros)")
    return df_silver

if __name__ == "__main__":
    from pipeline_bronze import process_bronze
    df_b = process_bronze()
    process_silver(df_b)    