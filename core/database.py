from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

# Create engine
engine = create_engine("sqlite:///data/results.db", echo=False)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class
Base = declarative_base()

# Table
class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    test_name = Column(String)
    prompt = Column(String)
    output = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)