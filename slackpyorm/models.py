from datetime import datetime

from pony.orm import *

db = Database()

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

    messages = Set("Message", reverse="user")


class Channel(db.Entity):
    id = PrimaryKey(str)

    name = Required(str)
    created = Required(datetime)
    creator = Required(User)

    topic_text = Optional(str)
    purpose_text = Optional(str)

    members = Set("User")

    messages = Set("Message", reverse="channel")


class Message(db.Entity):
    type = Required(str)
    timestamp = Required(datetime)
    # Some bots have text in attachments
    text = Optional(str)

    user = Optional(User)
    bot_id = Optional(str, nullable=True)
    subtype = Optional(str)

    upload = Required(bool, default=False)

    channel = Required(Channel)
