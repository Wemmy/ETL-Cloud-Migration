import boto3
import streamlit as st
from datetime import datetime,timedelta

# Initialize a DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='ca-central-1') # Choose your AWS region

def get_topic_data_sorted(items, selected_topic):
    select_data = []
    for item in items:
        # Assuming the complex attribute is stored under a key like 'topics'
        topics_data = item.get('topics', [])
        for topic_entry in topics_data:
            topic = topic_entry.get('topic', '')
            if topic == selected_topic:
                # Assuming you want to aggregate the entire item or specific data from it
                select_data.append(item)
                break  # Move to the next item if the selected topic is found
    # Sort data list by date in descending order
    select_data.sort(key=lambda x: datetime.strptime(x.get('time_published',''), "%Y%m%dT%H%M%S"), reverse=True)
    return select_data

# # Function to get data from dynamodb
@st.cache_resource
def get_data_from_dynamodb(table_name):
    # Calculate the start date of the past month
    today = datetime.now()
    first_day_of_current_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_of_past_month = (first_day_of_current_month - timedelta(days=1)).replace(day=1).strftime('%Y%m%dT%H%M%S')
    # Current date in the same format
    end_of_past_month = today.strftime('%Y%m%dT%H%M%S')
    table = dynamodb.Table(table_name)
    # response = table.query(
    #     KeyConditionExpression=boto3.dynamodb.conditions.Key('time_published').between(start_of_past_month, end_of_past_month)
    # )
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('time_published').between(start_of_past_month, today.strftime('%Y%m%dT%H%M%S'))
        )
    items = response.get('Items', [])
    all_topic = set()
    for item in items:
        # Assuming the complex attribute is stored under a key like 'topics'
        topics_data = item.get('topics', [])
        for topic_entry in topics_data:
            topic = topic_entry.get('topic', '')
            all_topic.add(topic)
    return items, all_topic