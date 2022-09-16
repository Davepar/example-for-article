from typing import List

from fastapi import Depends, FastAPI
from sqlmodel import Session, SQLModel, create_engine

from . import crud, models

app = FastAPI()


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/heroes", response_model=List[models.Hero])
def get_heroes(*, session: Session = Depends(get_session)):
    return crud.read_heroes(session)


@app.get("/teams", response_model=List[models.Team])
def get_teams(*, session: Session = Depends(get_session)):
    return crud.read_teams(session)


@app.get("/links", response_model=List[models.HeroTeamLink])
def get_links(*, session: Session = Depends(get_session)):
    return crud.read_links(session)
