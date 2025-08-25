from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Brand(Base):
    __tablename__ = 'brands'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    def get_all(session):
        return session.query(Brand).all()

class Size(Base):
    __tablename__ = 'sizes'
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)

    def get_all(session):
        return session.query(Size).all()

class Shoe(Base):
    __tablename__ = 'shoes'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    image = Column(String, nullable=False)

    brand_id = Column(Integer, ForeignKey('brands.id'), nullable=False)
    brand_rel = relationship("Brand")
    stock_rel = relationship("Stock")

    def get_shoes_query(session):
        query = session.query(Shoe)
        return query

    def filter_by_name(query, name):
        return query.filter(Shoe.name.ilike(f"%{name}%"))

    def filter_by_brand(query, brand):
        return query.filter(Shoe.brand_rel.has(Brand.name == brand))

    def filter_by_size(query, size):
        return query.filter(Shoe.stock_rel.any(Stock.size_rel.has(Size.number == size)))

    def filter_by_price_max(query, price_max):
        return query.filter(Shoe.price <= price_max)

    def filter_by_price_min(query, price_min):
        return query.filter(Shoe.price >= price_min)

    def finalize_query(query):
        return query.all()

class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)

    shoe_id = Column(Integer, ForeignKey('shoes.id'), nullable=False)
    size_id = Column(Integer, ForeignKey('sizes.id'), nullable=False)
    size_rel = relationship("Size")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False)
