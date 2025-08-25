from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, Shoe, Brand, Size, Stock
import pandas as pd

db_url = "postgresql://postgres:postgres@localhost/progetto"
engine = create_engine(db_url)

def get_db_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def init_db():
    session = get_db_session()
    Base.metadata.create_all(engine)

    df = pd.read_csv('data/brands.csv')
    for index, row in df.iterrows():
        brand = Brand(name=row['name'])
        session.add(brand)
    session.commit()

    df = pd.read_csv('data/shoes.csv')
    for index, row in df.iterrows():
        price = float(row['price'])
        shoe = Shoe(name=row['name'], price=price, description=row['description'], image=row['image'],
                    brand_id=row['brand_id'])
        session.add(shoe)
    session.commit()

    df = pd.read_csv('data/sizes.csv')
    for index, row in df.iterrows():
        number = int(row['number'])
        size = Size(number=number)
        session.add(size)
    session.commit()

    df = pd.read_csv('data/stock.csv')
    for index, row in df.iterrows():
        quantity = int(row['quantity'])
        shoe_id = int(row['shoe_id'])
        size_id = int(row['size_id'])
        stock = Stock(quantity=quantity, shoe_id=shoe_id, size_id=size_id)
        session.add(stock)
    session.commit()

    print('Valori inseriti correttamente nel database')


if __name__ == '__main__':
    init_db()
