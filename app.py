import os
import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError  # ✅ Import HttpError
from dotenv import load_dotenv
from datetime import datetime

# Load API Key from .env file
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    st.error("❌ API key not found! Please set YOUTUBE_API_KEY in a .env file.")
    st.stop()

# Set up YouTube API client
youtube = build("youtube", "v3", developerKey=API_KEY)

def search_small_channels(query, min_subs, max_subs, max_results=50):
    """Search for YouTube channels with subscriber count within the specified range."""
    channels = []
    next_page_token = None

    while len(channels) < max_results:
        search_response = youtube.search().list(
            q=query,
            type="channel",
            part="snippet",
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for search_result in search_response.get("items", []):
            channel_id = search_result["snippet"]["channelId"]
            channel_title = search_result["snippet"]["title"]

            # Skip channels with "Topic" in the title
            if "Topic" in channel_title:
                continue

            # Get channel statistics
            channel_response = youtube.channels().list(
                id=channel_id,
                part="statistics,contentDetails"
            ).execute()

            for channel in channel_response.get("items", []):
                subs = int(channel["statistics"].get("subscriberCount", 0))
                videos = int(channel["statistics"].get("videoCount", 0))

                # ✅ Fetch the uploads playlist ID safely
                uploads_playlist_id = channel["contentDetails"]["relatedPlaylists"].get("uploads")

                # ✅ Skip if the playlist ID is not found
                if not uploads_playlist_id:
                    print(f"⚠️ Skipping channel {channel_title} (No uploads playlist found)")
                    continue  # Move to the next channel

                # ✅ Filter channels based on subscriber count
                if min_subs <= subs <= max_subs:
                    latest_video_date = None

                    try:
                        # Fetch the latest video date
                        latest_video_response = youtube.playlistItems().list(
                            playlistId=uploads_playlist_id,
                            part="snippet",
                            maxResults=1
                        ).execute()

                        if latest_video_response["items"]:
                            latest_video_date = latest_video_response["items"][0]["snippet"]["publishedAt"]
                            latest_video_date = datetime.strptime(latest_video_date, "%Y-%m-%dT%H:%M:%SZ")

                    except HttpError as e:
                        # ✅ Handle 404 Playlist Not Found Error
                        if e.resp.status == 404:
                            print(f"❌ Playlist not found for {channel_title}, skipping...")
                        else:
                            print(f"⚠️ API error for {channel_title}: {e}")
                        continue  # ✅ Skip this channel and move to the next

                    # ✅ Append to the list only if valid data is found
                    channels.append({
                        "Channel Title": channel_title,
                        "Subscribers": subs,
                        "Videos": videos,
                        "Latest Video": latest_video_date,
                        "Channel Link": f"https://www.youtube.com/channel/{channel_id}"
                    })

            # Stop if enough results are collected
            if len(channels) >= max_results:
                break

        next_page_token = search_response.get("nextPageToken")
        if not next_page_token:
            break

    return pd.DataFrame(channels[:max_results])

# --- Streamlit UI ---
st.title("🎵 YouTube Small Channels Finder")

# Input fields for query and subscriber count range
query = st.text_input("🔍 Enter a search query:", placeholder="musicians strategy")

min_subs = st.number_input("Minimum Subscribers", min_value=0, max_value=1000000, value=1000)
max_subs = st.number_input("Maximum Subscribers", min_value=0, max_value=1000000, value=10000)

if st.button("Search"):
    with st.spinner("Searching..."):
        df = search_small_channels(query, min_subs, max_subs)
        st.write(f"✅ Found {len(df)} channels!")
        st.dataframe(df)

        # ✅ Option to download results as CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="youtube_channels.csv",
            mime="text/csv"
        )
