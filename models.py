from datetime import datetime

from pony.orm import *

db = Database()
db.bind("sqlite", "slack.sqlite3", create_db=True)

class User(db.Entity):
    id = PrimaryKey(str)

    deleted = Required(bool)
    first_name = Optional(str)
    last_name = Optional(str)
    email = Optional(str)
    username = Required(str)

    is_bot = Required(bool, default=False)
    is_owner = Required(bool, default=False)
    is_admin = Required(bool, default=False)

    created_channels = Set("Channel", reverse="creator")

    in_channels = Set("Channel", reverse="members")


class Channel(db.Entity):
    id = PrimaryKey(str)

    name = Required(str)
    created = Required(datetime)
    creator = Required(User)

    topic_text = Optional(str)
    purpose_text = Optional(str)

    members = Set("User")

db.generate_mapping(create_tables=True)
