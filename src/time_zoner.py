import argparse
import datetime
import re
import zoneinfo

from prettytable import PrettyTable
from timezones import zones

def main() -> None:
    args:argparse.Namespace = get_args()

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
        converted_time:datetime.datetime = convert_to_time(military_time)
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
                        help="Currently not used. Using this argument does nothing.")

    args = parser.parse_args()

    return args


def validate_format(time_to_check) -> None:
    time = re.compile("^(?:(([01]?[0-9]|2[0-3]):([0-5][0-9]))|(([1-9]|1[0-2]):([0-5][0-9]) ?(AM|PM)))$", re.I)

    if time.match(time_to_check.strip()):
        pass
    else:
        raise ValueError


def convert_to_military(time_to_convert:str) -> str:
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
    zone_dict = {}

    # Add the time (and timezone) from time_to_convert
    zone_dict[time_to_convert.tzname()] = str(time_to_convert.hour).rjust(2, "0") + ":" + str(time_to_convert.minute).rjust(2, "0")

    for zone in zones.keys():
        new_time:datetime.datetime = time_to_convert.astimezone(zones[zone])
        zone_dict[new_time.tzname()] = str(new_time.hour).rjust(2, "0") + ":" + str(new_time.minute).rjust(2, "0")

    return zone_dict


def append_to_table(table:PrettyTable, time_dict:dict) -> None:
    for time in time_dict.keys():
        table.add_row([time, time_dict[time]])


if __name__ == "__main__":
    main()
