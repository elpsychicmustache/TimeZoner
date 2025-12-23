# TimeZoner

## A CLI Python program to help Mountain Time users coordinate with others in different time zones.

This CLI program helps users collaborate with other users/partners who exist in different time zones. **This program, currently, assumes that the user is in Mountain Time.** More work will be required to determine the user's timezone and then make changes accordingly.

### ValueError upon running
If you get a ValueError stating: "Time zone data does not exist in this system. Please run 'pip install tzdata' to populate the timezone database for zoneinfo"
then you will need to run `pip install tzdata' to populate the timezone database for zoneinfo.

## Steps to run
There are a couple of ways to run this program.

### Running as a CLI one-liner
Let us assume you want to know the times for users if your time is 9:00 AM MT.
1. Run `python src/time_zoner.py -t "9:00 AM"` or `python src/time_zoner.py -t "9:00" from the project's root directory.
    - Note: this program can use 12 or 24-hour time. However, conversions will only be displayed in 24-hour time.
2. Observe that the program spits out different zones based on the time frame you entered.

You can also use your current time with the `-n` flag:
1. Run 'python src/time_zoner.py -n`, which creates time conversions based on the user's current time.

### Running with no arguments
The program lets you run the program without any arguments.

Running `python src/time_zoner.py` prompts the user for the time they would like to use.

## How to install this project
You need to install the requirements to your environment.

To do so, run `pip install -r requirements.txt` from the project's root directory.

## How to use this project in your own builds
The file 'src/timezones.py' contains the ZoneInfo objects (which are used to create conversions).

This is just a dictionary with a simple "zone" description - like "Mountain" and the ZoneInfo() object.
`dict["A string descriptor": ZoneInfo("TimeZoneKey")]`

For example:
I would add Brisbane, Australia to the conversion table. I need to add the following entry:
`"Brisbane Australia": ZoneInfo("Australia/Brisbane"),`
This will pull in the appropriate time for Brisbane when you run the program.

To obtain more timezones you can add, please run in the python interpreter:
`import zoneinfo`
`zoneinfo.available_timezones()`

## How to contribute
This is a very simple program currently. Not a lot of thought has been put into it as it was created to simplify things for myself.

Future iterations may include more functionality. If you find a bug, please create an issue.

If you wish to contribute, please pull fork this project into your own repo.
Then, create a pull request by pushing the changes you made into a different branch.
Please ensure that your pull request contains the issue you are resolving for fixing.
If an issue doesn't exist for your pull request, then feel free to create one and then tie to the pull request :).

Thanks for checking out this project!
