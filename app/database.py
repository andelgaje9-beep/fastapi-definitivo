from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.config import settings

# SQLALCHEMY_DATABASE_URL="postgresql+psycopg://postgres:0624@localhost:5432/fastapi"

# URL con las variables sin hardcode
SQLALCHEMY_DATABASE_URL= settings.database_url
print("DATABASE URL:", settings.database_url)
print("DATABASE HOST:", settings.database_url.split("@")[-1])

# Crea el "engine" de SQLAlchemy, que es el objeto principal para conectarse a la base de datos.
# El engine maneja la comunicación con PostgreSQL.
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# Define una fábrica de sesiones (SessionLocal).
# - autocommit=False → no confirma automáticamente las transacciones, debes usar db.commit().
# - autoflush=False → evita que se envíen cambios automáticamente antes de cada consulta.
# - bind=engine → conecta las sesiones al engine definido arriba.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para declarar modelos ORM.
# Todos tus modelos (User, Post, Vote, etc.) heredan de esta clase.
Base = declarative_base()

# Se usa para crear automaticamente las tablas en postgres siempre y cuando no usemos alembic
# Base.metadata.create_all(bind=engine)

#Dependency
def get_session():
    with Session(engine) as session:
        yield session




