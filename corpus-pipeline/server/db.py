import pathlib

from pony import orm  # noqa: F401
from pony_up import migrate

from config import DB_CONFIG


def bind_func(db):
    db.bind(**DB_CONFIG)
    db.generate_mapping(create_tables=True)


db = migrate(
    bind_func,
    folder_path=pathlib.Path(__file__).parent.resolve() / "migrations",
    python_import="migrations",
)
