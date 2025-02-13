from fastapi import FastAPI, Query
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from langchain.llms import HuggingFacePipeline
from langgraph.graph import StateGraph

app = FastAPI()

DATABASE_URL = "postgresql://user:password@localhost/mydatabase"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String)
    price = Column(Float)
    category = Column(String)
    description = Column(Text)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact_info = Column(Text)
    product_categories = Column(Text)

Base.metadata.create_all(bind=engine)

llm = HuggingFacePipeline.from_model_id("facebook/bart-large-cnn")

@app.get("/query/")
async def chatbot_query(query: str):
    session = SessionLocal()
    
    if "products under brand" in query.lower():
        brand_name = query.split("brand")[-1].strip()
        products = session.query(Product).filter(Product.brand.ilike(f"%{brand_name}%")).all()
        response = [f"{p.name} - ${p.price}" for p in products]
    
    elif "suppliers provide" in query.lower():
        category = query.split("provide")[-1].strip()
        suppliers = session.query(Supplier).filter(Supplier.product_categories.ilike(f"%{category}%")).all()
        response = [s.name for s in suppliers]
    
    elif "details of product" in query.lower():
        product_name = query.split("product")[-1].strip()
        product = session.query(Product).filter(Product.name.ilike(f"%{product_name}%")).first()
        response = f"{product.name}: {product.description} - ${product.price}" if product else "Product not found."
    
    else:
        response = "I didn't understand the query."
    
    session.close()
    return {"response": response}
