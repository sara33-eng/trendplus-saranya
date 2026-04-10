import requests
import time
import json
import os
from datetime import datetime

# Base URLs for HackerNews API
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"


CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]}
MAX_PER_CATEGORY = 25


# Fetch top story IDs
def fetch_top_story_ids():
    try:
        response = requests.get(TOP_STORIES_URL, headers={"User-Agent": "TrendPulse/1.0"})
        response.raise_for_status()
        # first 500 IDs
        resp = response.json()[:500]
        # print(resp)
        return resp
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        return []


# Fetch a single story by ID
def fetch_story(story_id):
    try:
        response = requests.get(ITEM_URL.format(story_id), headers={"User-Agent": "TrendPulse/1.0"})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching story {story_id}: {e}")
        return None


# Assign category based on keywords in title
def assign_category(title):
    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category

    return None


def main():
    story_ids = fetch_top_story_ids()

    # Storage for results
    collected_data = []

    # Track how many per category
    category_count = {cat: 0 for cat in CATEGORIES}
    # Loop through each category
    for category in CATEGORIES:
        print(f"Processing category: {category}")
        index = 0

        while category_count[category] < MAX_PER_CATEGORY and index < len(story_ids):
            story_id = story_ids[index]
            index += 1

            story = fetch_story(story_id)

            # Skip if request failed or missing title
            if not story or "title" not in story:
                continue

            assigned = assign_category(story["title"])

            # Only take stories that match current category
            if assigned == category:
                data = {
                    "post_id": story.get("id"),
                    "title": story.get("title"),
                    "category": assigned,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", "unknown"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                collected_data.append(data)
                category_count[category] += 1

        # Sleep AFTER each category
        time.sleep(2)

    # Ensure data folder exists
    if not os.path.exists("data"):
        os.makedirs("data")

    # File name with date
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    # Save JSON file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_data, f, indent=4)

    print(f"Collected {len(collected_data)} stories. Saved to {filename}")


if __name__ == "__main__":
    main()
