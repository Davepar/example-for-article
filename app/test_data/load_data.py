from typing import Any, Dict

import yaml
from sqlmodel import Session

from .. import models

LINK_KEY = "name"
link_data: Dict[str, Any] = {}


def _load_table(session: Session, model, model_name: str):
    data = yaml.safe_load(open(f"app/test_data/{model_name}.yaml"))
    for entry in data:
        entry_keys = list(entry.keys())
        for key in entry_keys:
            if key.endswith(f"__{LINK_KEY}"):
                (relation_key, model_name_key, _) = key.split("__")
                entry[relation_key] = link_data[f"{model_name_key}__{entry[key]}"]
                # Delete the link key to avoid warnings about extra keys
                del entry[key]
        obj = model.validate(entry)
        if LINK_KEY in entry_keys:
            link_data[f"{model_name}__{entry[LINK_KEY]}"] = obj
        session.add(obj)


def load_all(session: Session):
    _load_table(session, models.Hero, "hero")
    _load_table(session, models.Team, "team")
    _load_table(session, models.HeroTeamLink, "hero_team_link")
    session.commit()
