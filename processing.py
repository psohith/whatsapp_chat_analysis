import pandas as pd
import datetime
import calendar

def create_dataFrame(data):
    dates =[]
    times =[]
    users =[]
    msgs =[]
    for line in data.split('\n'):
        try :
            date_time , user_msg = line.split(' - ')
            date , time = date_time.split(', ')
            user, msg = user_msg.split(': ')
            dates.append(date)
            times.append(time)
            msgs.append(msg)
            users.append(user)
        except:
            pass
    df = pd.DataFrame({
        'date' : dates,
        'time' : times,
        'user': users,
        'message': msgs 
    })

    dates = []
    day = []
    year=[]
    month = [] 
    week = []
    for date in df['date']:
        dates.append(date[:-2]+str(int(date[-2:])+2000))
        date = dates[-1].split('/')
        date = [int(x) for x in date]
        day.append(date[0])
        month.append(date[1])
        year.append(date[2])
        date_Val = datetime.date(date[2],date[1],date[0])
        day_of_week = date_Val.weekday()
        week.append(calendar.day_name[day_of_week])


    df['date'] = dates
    df['day'] = day
    df['month'] = month
    df['year'] = year
    df['week'] = week
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

    df['month_name'] = df['month'].apply(lambda x : month_name[int(x)])

    period = []
    for time in df['time']:
        hour = int(time.split(':')[0])
        if hour == 12:
            period.append(str(hour) + "-" + str('01')+' '+time.split(' ')[-1])
        else:
            period.append(str(hour) + "-" + str(hour + 1) +' '+time.split(' ')[-1])

    df['period'] = period

    return df