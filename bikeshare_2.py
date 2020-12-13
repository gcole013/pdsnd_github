import time, pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while 1:
        city = input('Enter City to analyze from (chicago, new york city, washington): ').lower()
        if city in CITY_DATA:
            break
        else:
            print('Error! Wrong city entered...\n')

    # get user input for month (all, january, february, ... , june)

    while 1:
        month = input(
            "Enter month to analyze from ('all', 'january', 'february', 'march', 'april', 'may', 'june'): ").title()
        if month in ['All', 'January', 'February', 'March', 'April', 'May', 'June']:
            break
        else:
            print('Error! Wrong month entered...\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while 1:
        day = input(
            "Enter day to analyze from ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', "
            "'sunday'): ").title()
        if day in ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            break
        else:
            print('Error! Wrong day entered...\n')

    print('-' * 80)
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
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    if month != 'All':
        df = df[df['Start Time'].dt.strftime('%B') == month]

    if day != 'All':
        df = df[df['Start Time'].dt.strftime('%A') == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = (None, 0)
    MONTHS = ['January', 'February', 'March', 'April', 'May', 'June']

    for month in MONTHS:
        frame_ = df[df['Start Time'].dt.strftime('%B') == month]
        rows = len(frame_.index)
        if rows > common_month[-1]:
            common_month = month, rows

    print('Most Common Month:', common_month[0])

    # display the most common day of week
    common_day = (None, 0)
    DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    for day in DAYS:
        frame_ = df[df['Start Time'].dt.strftime('%A') == day]
        rows = len(frame_.index)
        if rows > common_day[-1]:
            common_day = day, rows

    print('Most Common Day:', common_day[0])

    # display the most common start hour

    common_hour = (None, 0)

    for hour in range(24):
        frame_ = df[df['Start Time'].dt.hour == hour]
        rows = len(frame_.index)
        if rows > common_hour[-1]:
            common_hour = hour, rows

    print('Most Common Start Hour:', common_hour[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    common_station = df['Start Station'].value_counts().idxmax()
    print('Most Common Start Station:', common_station)
    # display most commonly used end station

    common_station = df['End Station'].value_counts().idxmax()
    print('Most Common End Station:', common_station)
    # display most frequent combination of start station and end station trip

    pair = df.groupby(['Start Station', 'End Station']).size().reset_index().rename(columns={0:'count'})
    ans = pair[pair['count'] == pair['count'].max()][['Start Station','End Station']]
    print('Start Station: "' +ans.values[0][0]+ '", End Station: "'+ ans.values[0][1]+'"')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tripDuration = df['Trip Duration'].sum()
    print('Total Trip Duration:', tripDuration)

    # display mean travel time
    print('Mean Travel Time:', tripDuration / len(df.index))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 80)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Types')
    count = df['User Type'].value_counts()
    for i in range(len(count)):
        print(count.index[i], count.values[i])

    # Display counts of gender
    try:
        print('\nGender Count')
        count = df['Gender'].value_counts()
        for i in range(len(count)):
            print(count.index[i], count.values[i])
    except:
        print("The csv file have no columns named 'Gender'")
    # Display earliest, most recent, and most common year of birth

    try:
        print('\nBirth Years')
        common_year = df['Birth Year'].value_counts().idxmax()
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()

        print('Earliest Year of Birth:', earliest)
        print('Most Recent Year of Birth:', recent)
        print('Most Common Year of Birth:', common_year)
    except:
        print("The csv file have no columns named 'Birth Year'")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 80)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
