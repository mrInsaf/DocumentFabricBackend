from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./documents.db"

# Создание базы данных и движка
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Определение модели документа
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    person_code = Column(String, nullable=False)
    kks_code = Column(String, nullable=False)
    work_type = Column(String, nullable=False)
    doc_type = Column(String, nullable=False)
    version_prefix = Column(String, nullable=False)
    version = Column(String, nullable=False)
    date_input = Column(String, nullable=False)

# Создание таблиц в базе данных
def init_db():
    Base.metadata.create_all(bind=engine)
    print("db created")

