import pandas as pd
import numpy as np
import os

INPUT_FILE = "data/trends_clean.csv"
OUTPUT_FILE = "data/trends_analysed.csv"


def main():
    # shape of the DataFrame
    try:
        df = pd.read_csv(INPUT_FILE)
        print(f"Loaded data: {df.shape}")
    except Exception as e:
        print(f"Error loading file: {e}")
        return
    print("\nFirst 5 rows:")
    print(df.head())

    #  average score and average num_comments across all stories
    avg_score = df["score"].mean()
    avg_comments = df["num_comments"].mean()

    print(f"\nAverage score: {int(avg_score)}")
    print(f"Average comments: {int(avg_comments)}")

    print("NumPy Analysis")

    scores = df["score"].to_numpy()
    comments = df["num_comments"].to_numpy()

    # mean, median, and standard deviation of score
    print(f"Mean score: {int(np.mean(scores))}")
    print(f"Median score: {int(np.median(scores))}")
    print(f"Std deviation: {int(np.std(scores))}")

    #  highest score and lowest score
    print(f"High score: {int(np.max(scores))}")
    print(f"Low score: {int(np.min(scores))}")

    # category with most stories
    category_counts = df["category"].value_counts()
    top_category = category_counts.idxmax()
    print(f"\nMost stories in: {top_category} ({category_counts[top_category]} stories)")

    # story has the most comments
    max_comments_index = np.argmax(comments)
    top_story = df.iloc[max_comments_index]

    print(f"Most commented story: '{top_story['title']}' — '{top_story['num_comments']}' comments")


    # Engagement = comments / (score + 1)
    df["engagement"] = df["num_comments"] / (df["score"] + 1)

    # is_popular = score > average score
    df["is_popular"] = df["score"] > avg_score

    # Ensure folder exists
    if not os.path.exists("data"):
        os.makedirs("data")

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nSaved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
