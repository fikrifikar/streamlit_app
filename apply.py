import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title('Analysis of Google Drive Audit Log')
st.sidebar.title('Analysis of Google Drive Audit Log')

st.markdown(" This application is contained Google Drive Audit Log data to analyze the usage of G-Drive")
st.sidebar.markdown(" This application is contained Google Drive Audit Log data to analyze the usage of G-Drive")

DATA_URL = ('C:\\Users\\User\\Documents\\Data Science\\Python\\Analisis GDrive\\drive_logs_1623654488962.csv')

@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['Date'] = pd.to_datetime(data['Date'])
    return data

data = load_data()

st.sidebar.subheader("Show visibility type of Documents")
visibility = st.sidebar.radio('Visibility', ('Shared Externally', 'Shared Internally', 'Private', 'Anyone with the link', 'Anyone with the link within the audience', 'Anyone within the audience'))
st.sidebar.markdown(data.query("Visibility == @visibility").sample(n=1).iat[0, 0])

st.sidebar.markdown("### Number of visibility type")
select = st.sidebar.selectbox('Visualization Type', ['Bar plot', 'Pie Chart'], key='1')
visibility_count = data['Visibility'].value_counts()
visibility_count = pd.DataFrame({'Visibility_type':visibility_count.index, 'Count':visibility_count.values})

if not st.sidebar.checkbox("Hide", True):
    st.markdown("### Number of visibility type")
    if select == 'Bar plot':
        fig = px.bar(visibility_count, x='Visibility_type', y='Count', color='Count', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(visibility_count, values='Count', names='Visibility_type')
        st.plotly_chart(fig)

st.sidebar.subheader("When are the users access the data ?")
hour = st.sidebar.slider("Hour of day", 0, 23)
modified_data = data[data['Date'].dt.hour == hour]
if not st.sidebar.checkbox("Close", True, key='1'):
    st.markdown('%i data between %i:00 and %i:00' % (len(modified_data), hour, (hour+1)%24))
    #st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)

st.sidebar.subheader("Breakdown Event Name")
choice = st.sidebar.multiselect('Pick Event Name', ('Edit', 'View', 'Download', 'Sheets ImportRange', 'User Sharing Permissions Change', 'Rename', 'Create', 'Upload', 'Move', 'User Sharing Permissions Change from Parent Folder', 'Link Sharing Access Type Change', 'Link Sharing visibility change', 'Trash', 'Sheets ImportRange access change', 'Shared Drive Membership Change', 'Delete', 'Restore', 'Print', 'Editor Settings Change', 'Remove from folder', 'Link Sharing visibility change from Parent Folder', 'Link Sharing Access Type Change from Parent Folder'), key='0')

if len(choice) > 0:
    choice_data = data[data.Event_Name.isin(choice)]
    fig_choice = px.histogram(choice_data, x='Event_Name', y='Visibility', histfunc='count', color='Visibility',
    facet_col='Visibility', labels={'Visibility':'Type of Access'}, height=600, width=2000)
    st.plotly_chart(fig_choice)

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for what Event_Name ?', ('Edit', 'View', 'Download', 'Rename', 'Create', 'Upload', 'Move'))

if not st.sidebar.checkbox("Close", True, key='3'):
    st.header('Word cloud for %s sentiment' % (word_sentiment))
    df = data[data['Event_Name']==word_sentiment]
    words = ' '.join(df['Owner'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()
    st.set_option('deprecation.showPyplotGlobalUse', False)#
