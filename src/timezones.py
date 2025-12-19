from datetime import timedelta

standard_timezones = {
        "CST": timedelta(hours=1),
        "EST": timedelta(hours=2),
        "PST": timedelta(hours=-1),
        "IST": timedelta(hours=12, minutes=30),
        "GMT": timedelta(hours=7),
        "UTC": timedelta(hours=7),
        }

daylight_timezones = {
        "CDT": timedelta(hours=1),
        "EDT": timedelta(hours=2),
        "PDT": timedelta(hours=-1),
        "MST": timedelta(hours=-1),
        "BST": timedelta(hours=7),
        "IST": timedelta(hours=11, minutes=30),
        "UTC": timedelta(hours=6),
        }
