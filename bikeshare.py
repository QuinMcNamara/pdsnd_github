import time
import math
import statistics
import pandas as pd
import numpy as np

# Helper Functions
def print_pause(message_to_print):
    print(message_to_print)
    time.sleep(2)

def valid_input(prompt, options):
    while True:
        response = input(prompt).lower()
        for option in options:
            if option == response:
                return response
        print_pause("Please select one of the options.")

# Global Variables
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york city', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']


# Main Program Functions
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # Empty starting variables
    city = ''
    month = ''
    day = ''
    
    print('Hello! Let\'s explore some US bikeshare data!')
    print('')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = valid_input('Please Select the city for which you would like to see Bikeshare Data.\n'
                        'Options: Chicago, New York City, or Washington\n'
                        'Please type the name of the city (not case sensitive):', cities)
    print_pause('You have selected ' + city.title())
    print('')

    # get user input for month (all, january, february, ... , june)
    month = valid_input('Please Select the month for which you would like to see Bikeshare Data\n'
                         'Pick a month from January to June or type "all" to see cumulative data\n'
                         'Please type the full name of the month (not case sensitive):', months)
    print_pause('You have selected ' + month.title())
    print('')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = valid_input('Please Select the day of the week for which you would like to see Bikeshare Data\n'
                        'Pick any day of the week or type "all" to see cumulative data\n'
                        'Please type the full name of the day (not case sensitive):', days)
    print_pause('You have selected ' + day.title())
    print('')

    print('-'*40)
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load selected city file into dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        month = months.index(month) + 1

        # create new dataframe
        df = df[df['month'] == month]
    
    # filter by day of the week if applicable
    if day != 'all':
        # create new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most popular month
    popular_month = df['month'].mode()[0]
    print('The most popular month to ride is ' + months[popular_month - 1].title())

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day of the week for a ride is ' + common_day)

    # display the most common start hour
    df['hours'] = df['Start Time'].dt.hour
    common_hour = df['hours'].mode()[0]
    if common_hour > 0 and common_hour < 12:
        print('The most common hour to begin a ride was ' + str(common_hour) + 'am')
    elif common_hour > 12:
        common_hour -= 12
        print('The most common hour to begin a ride was ' + str(common_hour) + 'pm')
    elif common_hour == 12:
        print('The most common hour to begin a ride was ' + str(common_hour) + 'pm')
    elif common_hour == 0 or 24:
        print('The most common hour to begin a ride was ' + str(common_hour) + 'am')

    print('* Please note that if you selected a specific month and/or day of the week \n'
            'that this will always be the result for popular month and day *')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print_pause('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('The most common station from which a ride began was ' + common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('The most common station from which a ride ended was ' + common_end)

    # display most frequent combination of start station and end station trip
    # As seen here:
    # https://stackoverflow.com/questions/55719762/how-to-calculate-mode-over-two-columns-in-a-python-dataframe
    common_trip = (df['Start Station'] + ' to ' + df['End Station']).mode()[0]
    print('The most common trip was from ' + common_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print_pause('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    travel_hours = math.floor(total_time / 3600)
    travel_minutes = round((total_time/60) % 60, 1)
    print('The total travel time during the defined period was:')
    print(str(travel_hours) + ' hours and ' + str(travel_minutes) + ' minutes')

    # display typical trip duration
    # used median instead of mean to reduce impact of outliers
    avg_trip_duration = statistics.median(df['Trip Duration'])
    avg_trip_hours = math.floor(avg_trip_duration / 3600)
    avg_trip_minutes = round((avg_trip_duration/60) % 60, 1)

    print('The typical ride duration was:')
    print(str(avg_trip_hours) + ' hours and ' + str(avg_trip_minutes) + ' minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_pause('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_types = df['User Type'].value_counts()
    print('The breakdown of user types is as follows:')
    print(user_types.to_string())

    # display counts of gender
    # check for gender column as seen here:
    # https://stackoverflow.com/questions/24870306/how-to-check-if-a-column-exists-in-pandas
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('The breakdown of user gender is as follows:')
        print(gender_counts.to_string())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        common_birthyear = df['Birth Year'].mode()[0]
        youngest_user = df['Birth Year'].max()
        oldest_user = df['Birth Year'].min()
        print('The most common user birthyear was: ' + str(common_birthyear))
        print('The youngest user was born in: ' + str(youngest_user))
        print('The oldest user was born in: ' + str(oldest_user))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print_pause('-'*40)


def view_raw_data(df):
    # asks user for input - if "yes", displays the next 5 lines of raw bikeshare data
    # this process will repeat until user inputs "no"
    count = 0
    while True:
        more_data = valid_input('Would you like to view 5 lines of raw data?\n'
                                'Please enter yes or no:\n', ['yes', 'no'])
        if more_data == 'yes':
            print(df.iloc[count:count+5])
            count += 5
        else:
            print('Thank you for using BikeShare Data')
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
