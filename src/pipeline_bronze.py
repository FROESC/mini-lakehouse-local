import json
from pathlib import Path
import pandas as pd

def process_bronze():
    bronze_dir = Path("data/1_bronze")
    json_files = list(bronze_dir.glob("*.json"))
    
    if not json_files:
        print("[BRONZE] Nenhum arquivo JSON encontrado.")
        return None

    raw_records = []
    for file in json_files:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            raw_records.extend(data)
            
    df_bronze = pd.DataFrame(raw_records)
    print(f"[BRONZE] Ingestão concluída com sucesso. Total de registros brutos: {len(df_bronze)}")
    return df_bronze

if __name__ == "__main__":
    process_bronze()