import pandas as pd
from  urlextract import URLExtract
from collections import Counter
from wordcloud import WordCloud
import emoji

extract = URLExtract()

month_name = {
    1 : 'Jan',
    2 : 'Feb',
    3 : 'Mar',
    4 : 'Apr',
    5 : 'May',
    6 : 'Jun',
    7 : 'Jul',
    8 : 'Aug',
    9 : 'Sept',
    10 : 'Oct',
    11 : 'Nov',
    12 : 'Dec'
}

def fetch_stats(df,selected_user):
    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    num_media_msg = df[df['message']=='<Media omitted>'].shape[0]
    num_del_msg = df[df['message'] == 'This message was deleted'].shape[0]
    num_msg = df.shape[0]
    
    words = []
    links = []
    for msg in df['message']:
        links.extend(extract.find_urls(msg))
        words.extend(msg.split(' '))
    num_words = len(words)
    num_links = len(links)
    
    return num_msg,num_media_msg,num_links,num_words,num_del_msg


def monthly_statistic(selected_user,df):
    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    df = df.groupby(['year','month']).count().reset_index()
    df['month_name'] = df['month'].apply(lambda x : month_name[int(x)])
    months_year =[]
    for i in range(df.shape[0]):
        months_year.append(str(df.iloc[i]['month_name'])+'-'+str(df.iloc[i]['year']))

    df['month_year'] = months_year
    return df[['month_year','message']]



def daily_statistic(selected_user,df):
    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    df = df.groupby(['date']).count().reset_index()

    return df[['date','message']]




def day_activity_map(selected_user,df):
    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    df = df.groupby(['week']).count()

    return df


def month_activity_map(selected_user,df):
    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    df = df.groupby(['month_name']).count()
    return df


def most_busy_user(df):
    df = df.groupby(['user']).count().reset_index()
    df = df.sort_values(by=['message'], ascending=False)
    return df
    
def remove_stopwords(msg):
    file = open('stopwords.txt' ,'r')
    common_words = file.read()
    words = []
    for word in msg.lower().split(' '):
        if word not in common_words:
            words.append(word)
    return ' '.join(words) 

def most_common_words(selected_user,df):
    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    df = df[df['message']!='<Media omitted>']
    df = df[df['message']!='This message was deleted']

    df['message'].apply(remove_stopwords)
    words = []
    for msg in df['message']:
        for word in msg.lower().split(' '):
            words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def create_wordcloud(selected_user,df):
    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    df = df[df['message']!='<Media omitted>']
    df = df[df['message']!='This message was deleted']
    
    wc = WordCloud(width = 500, height = 500 , min_font_size = 10, background_color = 'white')
    df['message'].apply(remove_stopwords)
    word_cloud = wc.generate(df['message'].str.cat(sep = ' '))
    return word_cloud


def emoji_statistics(selected_user,df):
    if(selected_user != 'Overall'):
        df = df[df['user'] == selected_user]
    
    emojis = []
    for msg in df['message']:
        emojis.extend([x for x in msg if x in emoji.EMOJI_DATA])
    
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    
    return emoji_df