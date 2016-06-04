# slack-pyorm
Pony based ORM for Slack message, user and channel data plus a non-admin export all script

## Usage
If you intend on using this as a library you should bind the database and
generate mappings after importing models.

```python
from slackorm.models import *

db.bind("sqlite", "slack.sqlite3", create_db=True)
db.generate_mapping(create_tables=True)
```

You should download and use the `importer` script to import the Slack data into
your database.
