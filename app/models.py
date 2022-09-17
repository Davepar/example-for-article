from typing import List, Optional

from pydantic import Extra
from sqlmodel import Field, Relationship, SQLModel


class HeroTeamLink(SQLModel, table=True):
    team_id: Optional[int] = Field(
        default=None, foreign_key="team.id", primary_key=True
    )
    hero_id: Optional[int] = Field(
        default=None, foreign_key="hero.id", primary_key=True
    )
    is_training: bool = False

    team: "Team" = Relationship(back_populates="hero_links")
    hero: "Hero" = Relationship(back_populates="team_links")

    # Can't use the extra config here, otherwise it will complain
    # about the relationship fields.
    # class Config:
    #     extra = Extra.forbid


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    hero_links: List[HeroTeamLink] = Relationship(back_populates="team")

    class Config:
        extra = Extra.forbid


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    team_links: List[HeroTeamLink] = Relationship(back_populates="hero")

    class Config:
        extra = Extra.forbid
