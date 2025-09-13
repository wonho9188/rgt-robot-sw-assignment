from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 데이터베이스 설정
# 개발 환경에서는 SQLite 사용. 프로덕션에서는 PostgreSQL 사용
DATABASE_URL = "sqlite:///./library.db"

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # SQLite에서만 필요
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델을 위한 베이스 클래스 생성
Base = declarative_base()

def get_db():
    """데이터베이스 세션을 가져오는 의존성"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()