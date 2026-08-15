from src.generate_data import save_raw_events
from src.pipeline_bronze import process_bronze
from src.pipeline_silver import process_silver
from src.pipeline_gold import process_gold

def run_pipeline():
    print("=== INICIANDO PIPELINE MINI LAKEHOUSE ===\n")
    
    print("1. Gerando dados sintéticos (Origem)...")
    save_raw_events()
    print("-" * 50)
    
    print("2. Processando Camada BRONZE...")
    df_bronze = process_bronze()
    print("-" * 50)
    
    print("3. Processando Camada SILVER...")
    df_silver = process_silver(df_bronze)
    print("-" * 50)
    
    print("4. Processando Camada GOLD...")
    process_gold()
    print("-" * 50)
    
    print("\n=== PIPELINE EXECUTADO COM SUCESSO! ===")

if __name__ == "__main__":
    run_pipeline()  