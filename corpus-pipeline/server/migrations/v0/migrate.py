from pony_up import Migrator


def do_update(migrator):
    assert isinstance(migrator, Migrator)
    assert migrator.new_db
    db = migrator.new_db
    db.execute(
        'ALTER TABLE "text"  ADD COLUMN "state" TEXT DEFAULT "ACCEPTED" NOT NULL;'
    )
    db.execute('ALTER TABLE "text"  ADD COLUMN "comment" TEXT;')
    return 1, {"message": "Added `state` and `comment` column, to `text` table."}
