import requests
import tweepy
from bs4 import BeautifulSoup
from datetime import datetime
import random

import json

# Load secrets from the JSON file
with open("secrets.json", "r") as file:
    secrets = json.load(file)

def create_twitter_client():
    client = tweepy.Client(
        bearer_token=secrets["bearer_token"],
        consumer_key=secrets["consumer_key"],
        consumer_secret=secrets["consumer_secret"],
        access_token=secrets["access_token"],
        access_token_secret=secrets["access_token_secret"]
    )
    return client


def fetch_event():
    print("Fetching event...")
    url = "https://en.wikipedia.org/wiki/Wikipedia:On_this_day/Today"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    print("HTTP request sent.")
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return "No event found for today."
    
    soup = BeautifulSoup(response.text, 'html.parser')
    print("Page fetched successfully.")
    
    events_section = soup.find("div", {"id": "mp-otd-img"})
    if not events_section:
        print("No 'On This Day' section found.")
        return "No events found for today."
    events_list = events_section.find_next("ul")
    if not events_list:
        print("No event list found.")
        return "No events found for today."
    events = events_list.find_all("li")
    if not events:
        print("No events found in the 'On This Day' section.")
        return "No events found for today."
    event_list = [event.get_text() for event in events]
    selected_event = random.choice(event_list)
    print("Event fetched:", selected_event)
    return selected_event





def format_tweet(event):
    """Format the tweet with the event and hashtags.
    
    The tweet will have the form: "On this day: <event>... #OnThisDay #History"
    """
    tweet_text = f"🗓️ On this day: {event[:240]}... #OnThisDay #History"
    return tweet_text


def main():
    client = create_twitter_client()
    event = fetch_event()
    tweet_text = format_tweet(event)
    client.create_tweet(text=tweet_text)

if __name__ == "__main__":
    main()

