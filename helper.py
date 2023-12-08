from urlextract import URLExtract
# import wordcloud
from collections import Counter
import pandas as pd
import string
import re
import emoji

extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = (df[df['message'] == '‎image omitted\n'].shape[0]) + (df[df['message'] == '‎video omitted\n'].shape[0]) + (df[df['message'] == '‎sticker omitted\n'].shape[0]) + (df[df['message'] == '‎audio omitted\n'].shape[0]) + (df[df['message'] == '‎GIF omitted\n'].shape[0])

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


# func will only work in group chat analysis
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df


def remove_punctuation(message):
    x = re.sub('[%s]' % re.escape(string.punctuation), '', message)
    return x


# def create_wordcloud(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
#
#     # Data Cleaning
#     temp = df[df['user'] != 'group_notification']  # remove group notification
#     temp = temp[temp['user'] != 'Meta AI']  # remove Meta AI messages
#     temp = temp[temp['message'] != '\u200evideo omitted\n']  # remove video message
#     temp = temp[temp['message'] != '\u200eimage omitted\n']  # remove image message
#     temp = temp[temp['message'] != '\u200esticker omitted\n']  # remove sticker message
#     temp = temp[temp['message'] != '\u200eGIF omitted\n']  # remove GIF message
#     temp = temp[temp['message'] != '\u200eaudio omitted\n']  # remove audio message
#     temp['message'] = temp['message'].apply(remove_punctuation)  # remove punctuations
#
#     custom_stopwords = ['the', 'is', 'of', 'and', 'to', 'a', 'in', 'that', 'it',
#                         'image', 'omitted', 'https', 'na', 'dey', 'don', 'ooh', 'us',
#                         'go', 'lol', 'one', 'make', 'now', 'guy', 'u', 'o', 'e', '.',
#                         'come', 'will', 'see', 'today', 'know', 'say', 'even', 'still',
#                         'im', 'una', 'omo', 'im', 'haha', 'nah', 'video', 'sticker',
#                         'em', 'ooh', 'oo', 'ooo', 'ohh', 'ok', 'abeg', 'fit',
#                         'wey', 'wetin', 'wan', 's', 'audio']
#
#     stopwords = set(STOPWORDS).union(custom_stopwords)
#
#     wc = WordCloud(width=800,height=500,min_font_size=10,stopwords=stopwords,background_color='white')
#     df_wc = wc.generate(temp['message'].str.cat(sep=" "))
#     return df_wc


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']  # remove group notification
    temp = temp[temp['user'] != 'Meta AI']  # remove Meta AI messages
    temp = temp[temp['message'] != '\u200evideo omitted\n']  # remove video message
    temp = temp[temp['message'] != '\u200eimage omitted\n']  # remove image message
    temp = temp[temp['message'] != '\u200esticker omitted\n']  # remove sticker message
    temp = temp[temp['message'] != '\u200eGIF omitted\n']  # remove GIF message
    temp = temp[temp['message'] != '\u200eaudio omitted\n']  # remove audio message
    temp['message'] = temp['message'].apply(remove_punctuation)  # remove punctuations

    words = []

    for message in temp['message']:
        words.extend(message.split())

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(20))
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    month_timeline = []
    for i in range(timeline.shape[0]):
        month_timeline.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = month_timeline
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period',
                                  values='message', aggfunc='count').fillna(0)
    return user_heatmap
