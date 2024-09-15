import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import simplejson as json
import streamlit as st
from kafka import KafkaConsumer
from faker import Faker
from streamlit_autorefresh import st_autorefresh
import psycopg2
import json
import pandas as pd
import numpy as np


# Function to create a Kafka consumer
def create_kafka_consumer(topic_name):
    # Set up a Kafka consumer with specified topic and configurations
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    return consumer

# Function to fetch voting statistics from PostgreSQL database
@st.cache_data
def fetch_voting_stats():
    # Connect to PostgreSQL database
    conn = psycopg2.connect("host=localhost dbname=voting user=postgres password=postgres")
    cur = conn.cursor()

    # Fetch total number of voters
    cur.execute("""
        SELECT count(*) voters_count FROM voters
    """)
    voters_count = cur.fetchone()[0]

    # Fetch total number of candidates
    cur.execute("""
        SELECT count(*) candidates_count FROM candidates
    """)
    candidates_count = cur.fetchone()[0]

    return voters_count, candidates_count

# Function to fetch data from Kafka
def fetch_data_from_kafka(consumer):
    # Poll Kafka consumer for messages within a timeout period
    messages = consumer.poll(timeout_ms=1000)
    data = []

    # Extract data from received messages
    for message in messages.values():
        for sub_message in message:
            data.append(sub_message.value)
    return data

# Function to plot a colored bar chart for vote counts per candidate
def plot_colored_bar_chart(results):
    data_type = results['candidate_name']
    colors = plt.cm.viridis(np.linspace(0, 1, len(data_type)))
    plt.bar(data_type, results['total_votes'], color=colors)
    plt.xlabel('Candidate')
    plt.ylabel('Total Votes')
    plt.title('Vote Counts per Candidate')
    plt.xticks(rotation=90)
    return plt

# Function to plot a donut chart for vote distribution
def plot_donut_chart(data: pd.DataFrame, title='Donut Chart', type='candidate'):
    if type == 'candidate':
        labels = list(data['candidate_name'])
    elif type == 'gender':
        labels = list(data['gender'])

    sizes = list(data['total_votes'])
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    plt.title(title)
    return fig

# Function to plot a pie chart for vote distribution
def plot_pie_chart(data, title='Gender Distribution of Voters', labels=None):
    sizes = list(data.values())
    if labels is None:
        labels = list(data.keys())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    plt.title(title)
    return fig

# Function to split a dataframe into chunks for pagination
@st.cache_data(show_spinner=False)
def split_frame(input_df, rows):
    df = [input_df.loc[i: i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df


# Function to paginate a table
def paginate_table(table_data):
    top_menu = st.columns(3)
    with top_menu[0]:
        sort = st.radio("Sort Data", options=["Yes", "No"], horizontal=1, index=1)
    if sort == "Yes":
        with top_menu[1]:
            sort_field = st.selectbox("Sort By", options=table_data.columns)
        with top_menu[2]:
            sort_direction = st.radio(
                "Direction", options=["⬆️", "⬇️"], horizontal=True
            )
        table_data = table_data.sort_values(
            by=sort_field, ascending=sort_direction == "⬆️", ignore_index=True
        )
    pagination = st.container()

    bottom_menu = st.columns((4, 1, 1))
    with bottom_menu[2]:
        batch_size = st.selectbox("Page Size", options=[10, 25, 50, 100])
    with bottom_menu[1]:
        total_pages = (
            int(len(table_data) / batch_size) if int(len(table_data) / batch_size) > 0 else 1
        )
        current_page = st.number_input(
            "Page", min_value=1, max_value=total_pages, step=1
        )
    with bottom_menu[0]:
        st.markdown(f"Page **{current_page}** of **{total_pages}** ")

    pages = split_frame(table_data, batch_size)
    pagination.dataframe(data=pages[current_page - 1], use_container_width=True)



def generate_total(previous_total):
    increment_rate = np.random.randint(10, 25)

    
    increment_amount = np.random.randint(1, increment_rate)
    total = max(previous_total + increment_amount, 247)

    return total, increment_rate

fake = Faker()


num_candidates = 5
candidates_data = {
    'candidate_id': list(range(1, num_candidates + 1)),
    'candidate_name': [fake.name() for _ in range(num_candidates)],
    'party_affiliation': [fake.word() for _ in range(num_candidates)],
    'total_votes': [],
    'photo_url': [fake.image_url() for _ in range(num_candidates)],
}

# Initial sum_total_votes
sum_total_votes = 0


for i in range(num_candidates):
    # Ensure total_votes for each candidate increments
    total_votes_increment = np.random.randint(10, 100)  # Adjust the range as needed
    candidates_data['total_votes'].append(total_votes_increment)
    sum_total_votes += total_votes_increment


candidates_data['sum_total_votes'] = sum_total_votes


num_votes = 100
votes_data = {
    'candidate_id': np.random.choice(range(1, num_candidates + 1), size=num_votes).tolist(),  # Convert to list
    'total_votes': np.random.randint(1, 10, size=num_votes).tolist(),  # Convert to list
}


num_locations = 5
location_data = {
    'state': [fake.state() for _ in range(num_locations)],
    'count': np.random.randint(100, 1000, size=num_locations).tolist(),  # Convert to list
}


all_data = {
    'candidates_data': candidates_data,
    'votes_data': votes_data,
    'location_data': location_data,
}


with open('all_data.json', 'w') as f:
    json.dump(all_data, f)

# Function to update data displayed on the dashboard
def update_data():
    try:
        # Read all data from the single JSON file
        with open('all_data.json', 'r') as f:
            all_data = json.load(f)

        # Convert data to DataFrames
        results = pd.DataFrame(all_data['candidates_data'])
        votes_result = pd.DataFrame(all_data['votes_data'])
        location_result = pd.DataFrame(all_data['location_data'])

        # Fetch voting statistics
        voters_count, candidates_count = fetch_voting_stats()

        previous_total_voters = st.session_state.get('total_voters', 247)
        total_voters, increment_rate = generate_total(previous_total_voters)


        st.session_state['total_voters'] = total_voters
        st.session_state['last_update'] = time.time()
    

        # Display total voters and candidates metrics
        st.markdown("""---""")
        col1, col2 = st.columns(2)
        col1.metric("Total Voters", total_voters)
        col2.metric("Total Candidates", num_candidates)

        # Identify the leading candidate
        leading_candidate = results.loc[results['total_votes'].idxmax()]

        # Display leading candidate information
        st.markdown("""---""")
        st.header('Leading Candidate')
        col1, col2 = st.columns(2)
        with col1:
            image_url = leading_candidate['photo_url']

        # Use HTML to set the image height
            image_html = f'<img src="{image_url}" alt="image" style="width:200px; height:200px;">'
            st.markdown(image_html, unsafe_allow_html=True)
        with col2:
            st.header(leading_candidate['candidate_name'])
            st.subheader(leading_candidate['party_affiliation'])
            st.subheader("Total Vote: {}".format(leading_candidate['total_votes']))

        # Display statistics and visualizations
        st.markdown("""---""")
        st.header('Statistics')
        results = results[['candidate_id', 'candidate_name', 'party_affiliation', 'total_votes']]
        results = results.reset_index(drop=True)
        col1, col2 = st.columns(2)

        # Display bar chart and donut chart
        with col1:
            bar_fig = plot_colored_bar_chart(results)
            st.pyplot(bar_fig)

        with col2:
            donut_fig = plot_donut_chart(results, title='Vote Distribution')
            st.pyplot(donut_fig)

        # Display table with candidate statistics
        st.table(results)

        # Display location-based voter information with pagination
        st.header("Location of Voters")
        paginate_table(location_result)

        # Update the last refresh time
        st.session_state['last_update'] = time.time()

    except KeyError as e:
        st.warning(f"KeyError: {e}. Please check if your DataFrame contains the required columns.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

    # Placeholder to display last refresh time
    last_refresh = st.empty()
    last_refresh.text(f"Last refreshed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")

# Rest of the code remains the same


# Sidebar layout




def sidebar():
    # Initialize last update time if not present in session state
    if st.session_state.get('last_update') is None:
        st.session_state['last_update'] = time.time()

    # Slider to control refresh interval
    refresh_interval = st.sidebar.slider("Refresh interval (seconds)", 5, 60, 10)
    st_autorefresh(interval=refresh_interval * 1000, key="auto")

    # Button to manually refresh data
    if st.sidebar.button('Refresh Data'):
        update_data()
       

# Title of the Streamlit dashboard
st.title('Real-time Election Dashboard')
topic_name = 'aggregated_votes_per_candidate'

# Display sidebar
sidebar()

# Update and display data on the dashboard
#update_data()
