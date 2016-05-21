#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from datetime import datetime
from glob import glob
import os.path

from pony.orm import db_session, commit
from pony.orm.dbapiprovider import IntegrityError

import models

# Users
def import_user(u):
    user = {
        "id": u["id"],
        "deleted": u["deleted"],
        "username": u["name"]
    }
    for k in ("is_admin", "is_bot", "is_owner", "email",):
        if k in u:
            user[k] = u[k]

    for pk in ("first_name", "last_name",):
        if pk in u["profile"]:
            user[pk] = u["profile"][pk]

    models.User(**user)

def import_users(filepath):
    f = open(filepath)
    users = json.load(f)
    f.close()

    nonunique_skipped = 0
    for user in users:
        try:
            import_user(user)
        except:
            nonunique_skipped += 1

    print("Imported {} out of {} users".format(len(users)-nonunique_skipped, len(users)))

# Channels
def import_channel(c):
    chan = {
        "id": c["id"],
        "name": c["name"],
        "purpose_text": c["purpose"]["value"],
        "topic_text": c["topic"]["value"],
        "created": datetime.fromtimestamp(c["created"]),
        "creator": models.User.get(id=c["creator"])
    }

    dchan = models.Channel(**chan)
    for member_id in c["members"]:
        u = models.User.get(id=member_id)
        dchan.members.add(u)


def import_channels(filepath):
    f = open(filepath)
    channels = json.load(f)
    f.close()

    nonunique_skipped = 0
    for chan in channels:
        try:
            import_channel(chan)
        except:
            nonunique_skipped += 1

    print("Imported {} out of {} channels".format(len(channels)-nonunique_skipped, len(channels)))


# Messages
def import_message(channel_name, m):
    msg = {
        "type": m["type"],
        "timestamp": datetime.fromtimestamp(float(m["ts"])),
        "channel": models.Channel.get(name=channel_name)
    }

    if "user" in m:
        msg["user"] = models.User.get(id=m["user"])

    for k in ("subtype", "upload", "bot_id", "text",):
        if k in m:
            msg[k] = m[k]

    models.Message(**msg)

def import_messages_channel(filepath):
    f = open(filepath)
    messages = json.load(f)
    f.close()
    channel_name = os.path.split(filepath)[-1].split(".")[0]

    nonunique_skipped = 0
    for msg in messages:
        try:
            import_message(channel_name, msg)
        except:
            nonunique_skipped += 1

    imported = len(messages) - nonunique_skipped
    print("Imported {} messages from channel {}".format(imported, channel_name))

def import_messages(ddir):
    for f in glob(os.path.join(ddir, "*.json")):
        import_messages_channel(f)

@db_session
def import_all():
    import_users("./data/users.json")
    import_channels("./data/channels.json")
    import_messages("./data/logs")

def main():
    import_all()

if __name__ == "__main__":
    main()
