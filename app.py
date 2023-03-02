import streamlit as st
import processing , helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("choose the file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = processing.create_dataFrame(data)

    # st.dataframe(df)

    # fetche unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox("show analysis",user_list)

    if st.sidebar.button("Show Analysis"):
        
        num_msg,num_media_msg,num_links,num_words,num_del_msg = helper.fetch_stats(df,selected_user)
        st.title(":green[Top Statistics]")
        col1,col2,col3,col4,col5 = st.columns(5)
        with col1:
            st.header('Total Messages')
            st.title(':blue[{}]'.format(num_msg))
        with col2:
            st.header('Total Links')
            st.title(':blue[{}]'.format(num_links))
        with col3:
            st.header('Total Media')
            st.title(':blue[{}]'.format(num_media_msg))
        with col4:
            st.header('Total Deleted Msg')
            st.title(':blue[{}]'.format(num_del_msg))
        with col5:
            st.header('Total words')
            st.title(':blue[{}]'.format(num_words))

        #monthly timeline
        st.title('Monthly Timeline')
        montly_timeline = helper.monthly_statistic(selected_user,df)
        fig,axis = plt.subplots()
        axis.plot(montly_timeline['month_year'] , montly_timeline['message'], color='green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        st.caption("<p style='text-align: center;'>monthly timeline based on num of messages</p>", unsafe_allow_html=True)


        #daily timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_statistic(selected_user,df)
        fig,axis = plt.subplots()
        axis.plot(daily_timeline['date'] , daily_timeline['message'], color='black')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        st.caption("<p style='text-align: center;'>daily timeline based on num of messages</p>", unsafe_allow_html=True)


        # activity map
        st.title('Activity Map')
        col1 , col2 = st.columns(2)

        with col1:
            st.header(':blue[Most busy day]')
            day_df = helper.day_activity_map(selected_user , df)
            fig , axis = plt.subplots()
            axis.bar(day_df.index, day_df['message'] , color = 'red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            st.caption("<p style='text-align: center;'>day vs number of messages</p>", unsafe_allow_html=True)

        with col2:
            st.header(':blue[Most busy Month]')
            month_df = helper.month_activity_map(selected_user , df)
            fig , axis = plt.subplots()
            axis.bar(month_df.index, month_df['message'] ,color='blue')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            st.caption("<p style='text-align: center;'>month vs number of messages</p>", unsafe_allow_html=True)

        # finding the busiest users in the group(Group level)
        if(selected_user == 'Overall'):
            st.title('Most Busy users')
            busy_user = helper.most_busy_user(df)
            
            col1 , col2 = st.columns(2)

            with col1:
                fig , axis = plt.subplots()
                axis.bar(busy_user['user'].head(), busy_user['message'].head() ,color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
                st.caption("<p style='text-align: center;'>Top Members</p>", unsafe_allow_html=True)

            with col2:
                st.dataframe(busy_user[['user','message']])

        # Most common words
        st.title("Most common Words")
        df_wd = helper.most_common_words(selected_user,df)
        fig ,axis = plt.subplots()
        axis.barh(df_wd[0],df_wd[1] ,color='orange')
        st.pyplot(fig)


        # wordcloud
        st.title("WordCloud")
        word_cloud = helper.create_wordcloud(selected_user,df)
        fig,axis = plt.subplots()
        axis.imshow(word_cloud)
        st.pyplot(fig)
        st.caption("<p style='text-align: center;'>Some of the most occuring Words</p>", unsafe_allow_html=True)


        # emoji analysis
        emoji_df = helper.emoji_statistics(selected_user,df)
        st.title("Emoji Analysis")
        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,axis = plt.subplots()
            explode = (0.1, 0, 0, 0,0,0)
            axis.pie(emoji_df[1].head(6),labels = emoji_df[0].head(6) , shadow=True , explode=explode, startangle = 90)
            # axis.pie(emoji_df[1].head(), emoji_df[0].head() ,autopct = '%0.2f')
            st.pyplot(fig)
            st.caption("<p style='text-align: center;'>Mostly used Emojis</p>", unsafe_allow_html=True)


