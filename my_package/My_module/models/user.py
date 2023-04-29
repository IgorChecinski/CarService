from sqlalchemy import MetaData,create_engine
from sqlalchemy.orm import registry,Mapped,mapped_column,sessionmaker

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


@mapper_registry.mapped_as_dataclass
class User:
    __tablename__ = "users"

    idUser: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] 
    last_name: Mapped[str] 

print(User.__table__.columns.keys())

DB_URL = "sqlite:////Users/igor/Documents/School/PPY/CarService1.2/My_package/database/my.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
connection = engine.connect()
metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)