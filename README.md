# TimeZoner

## A CLI Python program to help Mountain Time users coordinate with others in different time zones.

This CLI program helps users collaborate with other users/partners who exist in different time zones. **This program, currently, assumes that the user is in Mountain Time.** More work will be required to determine the user's timezone and then make changes accordingly.

## Steps to run
There are a couple of ways to run this program.

### Running as a CLI one-liner
Let us assume you want to know the times for users if your time is 9:00 MST.
1. Run `python src/time_zoner.py -t "9:00"` from the project's root directory.
2. Observe that the program spits out different zones based on the time frame you entered.

### Running with no arguments
The program lets you run the program without any arguments.

Running `python src/time_zoner.py` prompts the user for the time they would like to use.

## How to install this project
You need to install the requirements to your environment.

To do so, run `pip install -r requirements.txt` from the project's root directory.

## How to use this project in your own builds
The file 'src/timezones.py' contains the timezones based on standard or daylight savings time.

To add a new timezone, please enter it by copying the other examples, but ensure you are setting hours= in respect to MDT (daylight) or MST (standard).
For example, let us assume there is a fictional timezone called "XYZ" that is 3 hours ahead of MDT.

I would add the following entry to `daylight_timezones`:
`"XYZ": timedelta(hours=3),`

This will pull in the timezone whenever the program displays daylight savings timezones.

## How to contribute
This is a very simple program currently. Not a lot of thought has been put into it as it was created to simplify things for myself.

Future iterations may include more functionality. If you find a bug, please create an issue.

If you wish to contribute, please pull fork this project into your own repo.
Then, create a pull request by pushing the changes you made into a different branch.
Please ensure that your pull request contains the issue you are resolving for fixing.
If an issue doesn't exist for your pull request, then feel free to create one and then tie to the pull request :).

Thanks for checking out this project!
