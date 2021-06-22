import time
import pandas as pd
import numpy as np
#I didnt use numpy, i dont know where to use it.
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
months = ['january', 'february', 'march', 'april', 'may', 'june', 'none']


# Function to check if the input is acceptable INPUT: in_str string to write in input
# , in_type to specify which values to be checked
def check_input(in_str, in_type):
    while True:
        try:
            x = input(in_str).lower()
            if in_type == 0 and x in CITY_DATA.keys():
                return x
            elif in_type == 1 and x.lower() in months:
                return x.lower()
            elif in_type == 2 and int(x) in range(1, 8):
                return int(x) - 1
            elif in_type == 3 and int(x) in range(1, 5):
                return int(x)
            elif in_type == 4 and x in ['yes','no']:
                return x

        except:
            print("Please enter a right value")


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = check_input("Please choose chicago , new york city or washington\n", 0)
    month = " "
    day = " "
    filter_type = " "

    # Choose the filter

    filter_type = check_input("Which type of filter do you want? \n choose 1 for Month \n 2 for days\n"
                              " 3 for both \n 4 for no filter.\n", 3)

    # TO DO: get user input for month (all, january, february, ... , june)
    # If user chose only month, then day = none
    # If he chose only day filter make month = none and day from the function
    # If both are chosen then we recall check_input function
    # and finally if filter type is none then both month and day = none
    if filter_type == 1:
        month = check_input("Please enter the month from January to June\n", 1)
        day = 'none'


    elif filter_type == 2:
        day = check_input(
            "Please enter the day as an integer, (1-monday ,2-teusday ,3-wednesday ,4-thursday ,5-friday ,6-saturday, 7-sunday)  \n",
            2)
        month = 'none'


    elif filter_type == 3:
        month = check_input("Please enter the month from January to June\n", 1)
        day = check_input("Please enter the day as an integer, ex: 1 = Sunday\n", 2)

    elif filter_type == 4:
        month, day = 'none', 'none'

    print('-' * 40)

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

    df = pd.read_csv(CITY_DATA[city])
    # editing both start time and end time to DATETIME

    df['Start Time'] = pd.DatetimeIndex(df['Start Time'])
    df['End Time'] = pd.DatetimeIndex(df['End Time'])

    if month != 'none' and day != 'none':
        df = df.loc[(df['Start Time'].dt.strftime('%B') == month.title()) & (df['Start Time'].dt.weekday == day)]
    elif month != 'none' and day == 'none':
        df = df.loc[(df['Start Time'].dt.strftime('%B') == month.title())]
    elif month == 'none' and day != 'none':
        df = df.loc[(df['Start Time'].dt.weekday == day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("The most common month is {}".format(df['Start Time'].dt.strftime("%B").mode()[0]))
    # TO DO: display the most common day of week
    print("The most common day of the week is {}".format(df['Start Time'].dt.strftime("%A").mode()[0]))
    # TO DO: display the most common start hour
    print("The most common hour is {}".format(df['Start Time'].dt.strftime("%H").mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most common start station is ', df['Start Station'].mode()[0])
    # TO DO: display most commonly used end station
    print('The most common end station is', df['End Station'].mode()[0])
    # TO DO: display most frequent combination of start station and end station trip
    df['Start to End'] = df['Start Station'] + df['End Station']
    print('The most frequent combination of start and end station is', df['Start to End'].mode()[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['Duration'] = df['End Time'] - df['Start Time']
    total_travel_time = df['Duration'].sum()
    total_travel_time = (total_travel_time.days * 24) + (total_travel_time.seconds/3600)
    print('Total time of traveling is', total_travel_time)
    # TO DO: display mean travel time
    average_travel_time = df['Duration'].mean()

    print('The average time of a single trip is ', average_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    count_user_type = df['User Type'].value_counts()
    for index, value in count_user_type.iteritems():
        print("The number of {} is {}.".format(index, value))

    # TO DO: Display counts of gender
    # as there is Nan values, I added them them with the same proportion
    if city != 'washington':
        count_male = df['Gender'].value_counts()[0]
        count_female = df['Gender'].value_counts()[1]
        count_nan = df['Gender'].isna().sum()

        # making ratio between male and female
        ratio = count_male / count_female
        # male hypotheticly
        count_male += (count_nan * ratio) / (ratio + 1)
        print("Hypotheticly number of Male could be {}".format(int(count_male)))
        # female hypotheticly
        count_female += (count_nan * 1) / (ratio + 1)
        print("Hypotheticly number of Female could be {}".format(int(count_female)))

        # TO DO: Display earliest, most recent, and most common year of birth
        print("The most common year of birth is {}.".format(df['Birth Year'].mode()[0]))
        print("The earliest year of birth is {}.".format(df['Birth Year'].min()))
        print("The most recent year of birth is {}.".format(df['Birth Year'].max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
def show_individual_data(df2,city):
    """ Function to show individual data
        Input : DataFrame , city
        city to reset the dataframe to its original states
        Output 5 indivdual data per 'yes' input
        if no is inputed the loop breaks 
       
    """
    df2 = pd.read_csv(CITY_DATA[city])
    cond_want_data = check_input("Would you like to see some individual data?\n",4)
    i = 0
    j = 4
    while cond_want_data == 'yes':
        for index in range(i,j+1):
            print('-'*40)
            print(df2.iloc[index,:])
            print('-' * 40)
        i+=5
        j+=5
        cond_want_data = check_input("Would you like to see more individual data?\n", 4)
def main():
    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_individual_data(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
