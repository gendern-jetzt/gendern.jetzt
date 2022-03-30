from pony import orm


def register_database(db):
    class Text(db.Entity):
        source = orm.Required(str)
        raw_data = orm.Required(str)
        cleaned_text = orm.Required(str)
        source_id = orm.Required(str)
        orm.composite_key(source, source_id)
        sentences = orm.Set("Sentence")

    class Sentence(db.Entity):
        text = orm.Required(Text)
        sentence_gendered = orm.Optional(str)
        sentence_ungendered = orm.Optional(str)
        to_gender = orm.Required(bool)
        verification_count = orm.Required(int, default=0)
        state = orm.Required(str, default="NEW")
