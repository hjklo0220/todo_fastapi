from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "mysql+pymysql://root:todos@127.0.0.1:3306/todos"

# engine 객체 생성 / echo=True옵션 어떤 sql이 사용되었는지 프린트 해주는것 product버전에선 사용x 
engine = create_engine(DATABASE_URL, echo=True)

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 제너레이터 생성
def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()


