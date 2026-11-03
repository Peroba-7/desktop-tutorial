from sqlmodel import SQLModel, create_engine, Session

sqlite_file_name = "empresa.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def criar_tabelas():
    SQLModel.metadata.create_all(engine)

def obter_sessao():
    with Session(engine) as session:
        yield session