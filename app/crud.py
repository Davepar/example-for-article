from sqlmodel import Session, select

from .models import Hero, HeroTeamLink, Team


def create_heroes(session: Session):
    # The difficult way to add test data
    team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
    team_z_force = Team(name="Z-Force", headquarters="Sister Margaret’s Bar")

    hero_deadpond = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_rusty_man = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    deadpond_team_z_link = HeroTeamLink(team=team_z_force, hero=hero_deadpond)
    deadpond_preventers_link = HeroTeamLink(
        team=team_preventers, hero=hero_deadpond, is_training=True
    )
    spider_boy_preventers_link = HeroTeamLink(
        team=team_preventers, hero=hero_spider_boy, is_training=True
    )
    rusty_man_preventers_link = HeroTeamLink(team=team_preventers, hero=hero_rusty_man)

    session.add(deadpond_team_z_link)
    session.add(deadpond_preventers_link)
    session.add(spider_boy_preventers_link)
    session.add(rusty_man_preventers_link)
    session.commit()


def read_heroes(session: Session):
    return session.exec(select(Hero)).all()


def read_teams(session: Session):
    return session.exec(select(Team)).all()


def read_links(session: Session):
    return session.exec(select(HeroTeamLink)).all()


# Not needed???????


def update_heroes(session: Session):
    hero_spider_boy = session.exec(select(Hero).where(Hero.name == "Spider-Boy")).one()
    team_z_force = session.exec(select(Team).where(Team.name == "Z-Force")).one()

    spider_boy_z_force_link = HeroTeamLink(
        team=team_z_force, hero=hero_spider_boy, is_training=True
    )
    team_z_force.hero_links.append(spider_boy_z_force_link)
    session.add(team_z_force)
    session.commit()

    print("Updated Spider-Boy's Teams:", hero_spider_boy.team_links)
    print("Z-Force heroes:", team_z_force.hero_links)

    for link in hero_spider_boy.team_links:
        if link.team.name == "Preventers":
            link.is_training = False

    session.add(hero_spider_boy)
    session.commit()

    for link in hero_spider_boy.team_links:
        print("Spider-Boy team:", link.team, "is training:", link.is_training)
