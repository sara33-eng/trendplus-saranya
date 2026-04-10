import pandas as pd
import os

# File path
INPUT_FILE = "data/trends_20260410.json"
OUTPUT_FILE = "data/trends_clean.csv"


def main():
    try:
        df = pd.read_json(INPUT_FILE)
        print(f"Loaded {len(df)} stories from {INPUT_FILE}")
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Remove  rows with the same post_id
    before = len(df)
    df = df.drop_duplicates(subset="post_id")
    print(f"After removing duplicates: {len(df)}")

    # drop rows where post_id, title, or score is missing
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    #  make sure score and num_comments are integers
    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].fillna(0).astype(int)

    # remove stories where score is less than 5
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")

    #  strip extra spaces from the title column
    df["title"] = df["title"].str.strip()

    if not os.path.exists("data"):
        os.makedirs("data")
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved {len(df)} rows to {OUTPUT_FILE}")

    # quick summary
    print("\nStories per category:")
    print(df["category"].value_counts())


if __name__ == "__main__":
    main()
