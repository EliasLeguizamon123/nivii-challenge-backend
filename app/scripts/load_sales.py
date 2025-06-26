import os
import pandas as pd
from sqlmodel import Session
from app.database.config import engine
from app.entities.sales import Sale

def load_sales_from_csv(csv_path: str):
    df = pd.read_csv(csv_path)

    # Parse date con formato mm/dd/yyyy
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')

    with Session(engine) as session:
        for _, row in df.iterrows():
            sale = Sale(
                product_name=row['product_name'],
                waiter=row['waiter'],
                ticket_number=row['ticket_number'],
                date=row['date'].to_pydatetime(),
                week_day=row['week_day'],
                hour=row['hour'],
                quantity=int(row['quantity']),
                unitary_price=float(row['unitary_price']),
                total=float(row['total'])
            )
            session.add(sale)
        session.commit()
    print(f"Cargados {len(df)} registros de sales.")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(BASE_DIR, "..", "database", "data.csv")
    load_sales_from_csv(csv_path)
