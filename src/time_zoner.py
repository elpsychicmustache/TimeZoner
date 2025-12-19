import argparse
import datetime

from prettytable import PrettyTable
from timezones import standard_timezones, daylight_timezones

def main() -> None:
    args:argparse.Namespace = get_args()

    if not args.time:
        time_to_convert:str = input("[+] Please enter the time to convert: ")
    else:
        time_to_convert = args.time

    military_time:str = convert_to_military(time_to_convert)
    try:
        converted_time:datetime.datetime = convert_to_time(military_time)
    except ValueError:
        print(f"[!] {time_to_convert} is not a valid time. Some examples to try: '21:00' or '9:00 PM'")
        converted_time = None

    if converted_time:
        table = PrettyTable()
        table.field_names = ["Time Zone", "Time"]

        if args.standard:
            append_to_table(table, standard_timezones, converted_time)
        if args.standard and args.daylight:
            table.add_divider()
        if args.daylight:
            append_to_table(table, daylight_timezones, converted_time)

        print(table)

    input("Press ENTER ...")


def get_args() -> argparse.Namespace:
    """Get the program arguments.

    :returns: Args from argparse.
    :rtype: argparse.Namespace
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--time",
                        help="The time to convert. Can be in 12 hour or 24 hour")
    parser.add_argument("-s", "--standard",
                        action="store_true")
    parser.add_argument("-d", "--daylight",
                        action="store_true")
    parser.add_argument("-z", "--timezone",
                        help="Currently not used. Using this argument does nothing.")

    args = parser.parse_args()

    # if user did not provide standard or daylight, just set both to True
    if not args.standard and not args.daylight:
        args.standard = True
        args.daylight = True

    return args


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


def convert_to_time(time_to_convert:str) -> datetime.datetime:
    hours_minutes_list = time_to_convert.split(":")
    today = datetime.date.today()
    return datetime.datetime(
            year=today.year,
            month=today.month,
            day=today.day,
            hour=int(hours_minutes_list[0]),
            minute=int(hours_minutes_list[1]),
            )


def append_to_table(table:PrettyTable, time_dict:dict, entered_time:datetime.datetime) -> None:
    if time_dict == standard_timezones:
        table.add_row(["MST", str(entered_time.hour).rjust(2, "0") + ":" + str(entered_time.minute).rjust(2, "0")])
    else:
        table.add_row(["MDT", str(entered_time.hour).rjust(2, "0") + ":" + str(entered_time.minute).rjust(2, "0")])

    for key,item in time_dict.items():
        table.add_row([key, str((entered_time + item).hour).rjust(2, "0") + ":" + str((entered_time + item).minute).rjust(2, "0")])


if __name__ == "__main__":
    main()
