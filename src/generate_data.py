import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from faker import Faker

fake = Faker('pt_BR')

CATEGORIAS = ['Eletrônicos', 'Vestuário', 'Alimentos', 'Livros', 'Eletrodomésticos']

def generate_events(num_records=100):
    events = []
    base_date = datetime.now()
    
    for _ in range(num_records):
        # Simula datas nos últimos 3 dias
        random_days = random.randint(0, 2)
        event_time = base_date - timedelta(days=random_days, minutes=random.randint(0, 1440))
        
        event = {
            "transaction_id": fake.uuid4(),
            "customer_id": random.randint(1000, 1050),
            "product_category": random.choice(CATEGORIAS),
            "amount": round(random.uniform(10.0, 1500.0), 2),
            "status": random.choice(["COMPLETED", "COMPLETED", "CANCELLED", "PENDING"]),
            "timestamp": event_time.isoformat()
        }
        events.append(event)
    
    # Injeta alguns duplicados propositais para tratarmos na Silver
    events.append(events[0])
    events.append(events[1])
    
    return events

def save_raw_events():
    Path("data/1_bronze").mkdir(parents=True, exist_ok=True)
    data = generate_events(150)
    
    filename = f"data/1_bronze/events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"[BRONZE GENERATOR] {len(data)} eventos salvos em {filename}")

if __name__ == "__main__":
    save_raw_events()