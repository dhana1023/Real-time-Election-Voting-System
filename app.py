import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Function to generate random voting statistics
def generate_voting_stats():
    # Generate random numbers for total voters and candidates
    voters_count = np.random.randint(1000, 5000)
    candidates_count = np.random.randint(5, 10)
    return voters_count, candidates_count

# Function to generate random candidate information
def generate_candidate_info(num_candidates):
    candidate_ids = list(range(1, num_candidates + 1))
    candidate_names = ['Candidate {}'.format(i) for i in candidate_ids]
    party_affiliations = ['Party {}'.format(i) for i in np.random.randint(1, 5, num_candidates)]
    total_votes = np.random.randint(100, 1000, num_candidates)
    photo_urls = ['https://via.placeholder.com/200' for _ in range(num_candidates)]

    candidates_data = {
        'candidate_id': candidate_ids,
        'candidate_name': candidate_names,
        'party_affiliation': party_affiliations,
        'total_votes': total_votes,
        'photo_url': photo_urls
    }
    return pd.DataFrame(candidates_data)

# Function to generate random location-based voter information
def generate_location_info(num_locations):
    states = ['State {}'.format(i) for i in range(1, num_locations + 1)]
    counts = np.random.randint(100, 1000, num_locations)

    location_data = {
        'state': states,
        'count': counts
    }
    return pd.DataFrame(location_data)

# Function to paginate a table
def paginate_table(table_data):
    # Pagination logic here
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
    pass

# Function to update data displayed on the dashboard
def update_data():
    # Generate random voting statistics
    voters_count, candidates_count = generate_voting_stats()

    # Display total voters and candidates metrics
    st.markdown("""---""")
    col1, col2 = st.columns(2)
    col1.metric("Total Voters", voters_count)
    col2.metric("Total Candidates", candidates_count)

    # Generate random candidate information
    results = generate_candidate_info(candidates_count)

    # Identify the leading candidate
    leading_candidate = results.loc[results['total_votes'].idxmax()]

    # Display leading candidate information
    st.markdown("""---""")
    st.header('Leading Candidate')
    col1, col2 = st.columns(2)
    with col1:
        st.image(leading_candidate['photo_url'], width=200)
    with col2:
        st.header(leading_candidate['candidate_name'])
        st.subheader(leading_candidate['party_affiliation'])
        st.subheader("Total Vote: {}".format(leading_candidate['total_votes']))

    # Display statistics and visualizations
    st.markdown("""---""")
    st.header('Statistics')
    col1, col2 = st.columns(2)

    # Display bar chart and donut chart (assuming results is a DataFrame)
    with col1:
        st.write("Bar Chart")
    with col2:
        st.write("Donut Chart")

    # Display table with candidate statistics
    st.table(results)

    # Generate random location-based voter information
    location_result = generate_location_info(10)  # Assuming 10 locations
    # Display location-based voter information with pagination
    st.header("Location of Voters")
    paginate_table(location_result)

    # Update the last refresh time
    st.session_state['last_update'] = time.time()

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

# Display sidebar
sidebar()

# Update and display data on the dashboard
update_data()
