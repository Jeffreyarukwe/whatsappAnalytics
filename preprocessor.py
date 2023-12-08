import re
import pandas as pd


def preprocess(data):
    pattern = '\W\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\W\s'
    messages = re.split(pattern, data)[1:]

    pattern2 = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}'
    # extract all dates
    dates = re.findall(pattern2, data)

    # create dataframe
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M:%S')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # separate Users and Message
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(':\s*', message)
        if '\u200e' in entry[0] or 'Three' in entry[0]:  # LRM
            users.append('group_notification')
            messages.append(entry[1])
        else:  # user name
            users.append(entry[0])
            messages.append(entry[1])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract multiple columns from the Date Column
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # add period column that shows data capture between which 24 hour format
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
