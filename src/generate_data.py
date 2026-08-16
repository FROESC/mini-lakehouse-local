import json
from datetime import datetime, timedelta
from pathlib import Path
import requests


def fetch_usd_exchange_rate(days_back=30):
    """Busca o histórico da cotação do Dólar (PTAX) na API do Banco Central do Brasil."""
    end_date = datetime.now().strftime("%d/%m/%Y")
    start_date = (datetime.now() - timedelta(days=days_back)).strftime(
        "%d/%m/%Y"
    )

    # Código 10813 = Cotação do Dólar americano (venda) no sistema SGS do BACEN
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.10813/dados?formato=json&dataInicial={start_date}&dataFinal={end_date}"

    print(f"[BRONZE] Requisitando dados da API do Bacen: {url}")
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro ao acessar API: Status {response.status_code}")


def save_raw_events():
    Path("data/1_bronze").mkdir(parents=True, exist_ok=True)

    # Busca dados reais da API
    raw_data = fetch_usd_exchange_rate(days_back=60)

    # Salva o JSON bruto preservando a camada Bronze (Raw)
    filename = f"data/1_bronze/usd_rate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, indent=2, ensure_ascii=False)

    print(
        f"[BRONZE GENERATOR] {len(raw_data)} registros reais de câmbio salvos em {filename}"
    )


if __name__ == "__main__":
    save_raw_events()