#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from datetime import datetime

from pony.orm import db_session, commit
from pony.orm.dbapiprovider import IntegrityError

import models

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

@db_session
def import_all():
    import_users("./data/users.json")
    import_channels("./data/channels.json")

def main():
    import_all()

if __name__ == "__main__":
    main()