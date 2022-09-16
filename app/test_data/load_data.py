import yaml
from sqlmodel import Session

from .. import models


LINK_KEY = 'name'
link_data = {}


def _load_type(session: Session, model, filename: str):
    data = yaml.safe_load(open(f"app/test_data/{filename}.yaml"))
    for entry in data:
        entry_keys = list(entry.keys())
        for key in entry_keys:
            if key.endswith(f'__{LINK_KEY}'):
                (relation_key, filename_key, _) = key.split('__')
                entry[relation_key] = link_data[f'{filename_key}__{entry[key]}']
                del entry[key]
        obj = model.validate(entry)
        if LINK_KEY in entry_keys:
            link_data[f'{filename}__{entry[LINK_KEY]}'] = obj
        session.add(obj)

def load_all(session: Session):
    _load_type(session, models.Hero, 'hero')
    _load_type(session, models.Team, 'team')
    _load_type(session, models.HeroTeamLink, 'hero_team_link')
    session.commit()
