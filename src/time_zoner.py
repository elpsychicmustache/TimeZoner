import argparse
import datetime
import re
import zoneinfo

from prettytable import PrettyTable
from timezones import zones

def main() -> None:
    args:argparse.Namespace = get_args()

    # Checking to make sure the timezone database is populated; otherwise, throw an error
    if not zoneinfo.available_timezones():
        raise ValueError("Time zone data does not exist in this system. Please run 'pip install tzdata' to populate the timezone database for zoneinfo.")

    # if now is provided, then use the time as of right now
    if args.now:
        now = datetime.datetime.today()
        time_to_convert:str = str(now.hour).rjust(2, "0") + ":" + str(now.minute).rjust(2, "0")
    # else get args.time or ask user to create the time
    elif not args.time:
        time_to_convert:str = input("[+] Please enter the time to convert: ")
    else:
        time_to_convert = args.time

    # Try/catch block to control flow if user provides or enters an incorrect time format.
    try:
        validate_format(time_to_convert)  # Throws ValueError if the user does not enter a valid time.
        military_time:str = convert_to_military(time_to_convert)
        converted_time:datetime.datetime = convert_to_time(military_time, args.timezone)
    except ValueError:
        print(f"[!] {time_to_convert} is not a valid time. Some examples to try: '21:00' or '9:00 PM'")
    else:
        # Build the times based on ZoneInfo objects
        times = build_zones_dict(converted_time)

        # Build the table
        table = PrettyTable()
        table.field_names = ["Time Zone", "Time"]
        append_to_table(table, times)

        # Show the table
        print(table)
    finally:
        # Pause for the user to press ENTER in case the console auto-clears the screen
        input("Press ENTER ...")


def get_args() -> argparse.Namespace:
    """Get the program arguments.

    :returns: Args from argparse.
    :rtype: argparse.Namespace
    """

    parser = argparse.ArgumentParser()

    time_group = parser.add_mutually_exclusive_group()
    time_group.add_argument("-t", "--time",
                        help="The time to convert. Can be in 12 hour or 24 hour")
    time_group.add_argument("-n", "--now",
                        help="Use the current time to convert.",
                        action="store_true")

    parser.add_argument("-z", "--timezone",
                        choices=[time_key for time_key in zones.keys()],
                        default="Mountain",
                        help="Currently not used. Using this argument does nothing.")

    args = parser.parse_args()

    return args


def validate_format(time_to_check:str) -> None:
    """Validate the format of a time as a string using regex

    Needs to be in 12 or 24-hour format. No space between AM/PM and the time is just fine.
    In other words, 9:00PM and 9:00 PM will both work.

    There are also rules built in to try to minimize invalid times.
    For example, the following inputs will NOT work:
    - 24:00
    - 13:00 AM
    - 000:004
    - 12:68 PM

    :param time_to_check: The string to validate is in a proper time format.
    :type time_to_check: str
    """
    time = re.compile("^(?:(([01]?[0-9]|2[0-3]):([0-5][0-9]))|(([1-9]|1[0-2]):([0-5][0-9]) ?(AM|PM)))$", re.I)

    if time.match(time_to_check.strip()):
        pass
    else:
        raise ValueError


def convert_to_military(time_to_convert:str) -> str:
    """Attempts to convert a time entered in 12-hour into 24-hour time.

    If the time is in 24-hour this method does nothing.

    :param time_to_convert: The time to check and convert.
    :type time_time_convert: str
    :returns: Returns the 24-hour time of time_to_convert.
    :rtype: str
    """

    if "am" in time_to_convert.lower():
        time_to_convert = time_to_convert.lower().replace("am", "").strip()
        time_to_convert_split:list = time_to_convert.split(":")
        if int(time_to_convert_split[0]) == 12:
            time_to_convert_split[0] = "0"
        time_to_conver = ":".join(time_to_convert_split)
    elif "pm" in time_to_convert.lower():
        time_to_convert = time_to_convert.lower().replace("pm", "").strip()
        time_to_convert_split:list = time_to_convert.split(":")
        hour = int(time_to_convert_split[0])
        if hour < 12:
            hour += 12
        time_to_convert_split[0] = str(hour)
        time_to_convert = ":".join(time_to_convert_split)

    return time_to_convert


def convert_to_time(time_to_convert:str, timezone="Mountain") -> datetime.datetime:
    """Transforms a time as a string into a datetime object.

    This will assume that the time is for today. More wore will be needed to accomodate different days.

    :param time_to_convert: The time to turn into a datetime object.
    :type time_to_convert: str
    :param timezone: The key from timezones to use for the timezone.
    :type timezone: str
    :returns: The datetime object from time_to_convert
    :rtype: datetime.datetime
    """
    hours_minutes_list = time_to_convert.split(":")
    today = datetime.date.today()
    return datetime.datetime(
            year=today.year,
            month=today.month,
            day=today.day,
            hour=int(hours_minutes_list[0]),
            minute=int(hours_minutes_list[1]),
            tzinfo=zones.get(timezone)
            )


def build_zones_dict(time_to_convert:datetime.datetime, zones:dict[str,"TimeZone"]=zones) -> dict[str, datetime.datetime]:
    """Creates a dictionary of timezone keys and datetime objects as values.

    :param time_to_convert: The original datetime object from which to assume all other times.
    :type time_to_convert: datetime.datetime
    :param zones: A dictionary of string keys and TimeZone objects
    :type zones: dict[str, TimeZone]
    :returns: A dictionary of timezone keys (i.e. PST, MDT, etc.) and datetime objects based off of time_to_convert.
    :rtype: dict[str, datetime.datetime]
    """
    zone_dict = {}

    # Add the time (and timezone) from time_to_convert
    zone_dict[time_to_convert.tzname()] = str(time_to_convert.hour).rjust(2, "0") + ":" + str(time_to_convert.minute).rjust(2, "0")

    for zone in zones.keys():
        new_time:datetime.datetime = time_to_convert.astimezone(zones[zone])
        zone_dict[new_time.tzname()] = str(new_time.hour).rjust(2, "0") + ":" + str(new_time.minute).rjust(2, "0")

    return zone_dict


def append_to_table(table:PrettyTable, time_dict:dict) -> None:
    """Runs through time_dict and adds it to the PrettyTable object

    :param table: The PrettyTable object to add timezone information to.
    :type table: PrettyTable
    :param time_dict: The dictionary of timezones and datetime objects.
    :type time_dict: dict[str, datetime.datetime]
    """
    for time in time_dict.keys():
        table.add_row([time, time_dict[time]])


if __name__ == "__main__":
    main()
