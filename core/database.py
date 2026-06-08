from sqlalchemy import create_engine, Column, String, Integer, Text, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

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

    # Test info
    test_name = Column(String, index=True)
    prompt = Column(Text)

    # Outputs
    output = Column(Text)
    previous_output = Column(Text, nullable=True)   # 🔥 for diff engine

    # Metrics
    latency = Column(Float, nullable=True)

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)


# Create tables
Base.metadata.create_all(bind=engine)