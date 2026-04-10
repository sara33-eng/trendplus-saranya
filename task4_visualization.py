import pandas as pd
import matplotlib.pyplot as plt
import os

INPUT_FILE = "data/trends_analysed.csv"
OUTPUT_DIR = "outputs"


def shorten_title(title, max_len=50):
    return title if len(title) <= max_len else title[:max_len] + "..."


def main():
    try:
        df = pd.read_csv(INPUT_FILE)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # create outputs folder if does not exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Chart 1: Top 10 Stories by Score - horizontal bar chart
    top10 = df.sort_values(by="score", ascending=False).head(10)

    # shorten titles
    top10["short_title"] = top10["title"].apply(shorten_title)

    plt.figure(figsize=(10, 6))
    plt.barh(top10["short_title"], top10["score"])
    plt.xlabel("Score")
    plt.ylabel("Story Title")
    plt.title("Top 10 Stories by Score")
    plt.gca().invert_yaxis()

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/chart1_top_stories.png")
    plt.close()

    # Chart 2: Stories per Category - bar chart
    category_counts = df["category"].value_counts()

    plt.figure(figsize=(8, 5))
    plt.bar(category_counts.index, category_counts.values)
    plt.xlabel("Category")
    plt.ylabel("Number of Stories")
    plt.title("Stories per Category")

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/chart2_categories.png")
    plt.close()

    # Chart 3: Score vs Comments - scatter Plot
    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]

    plt.figure(figsize=(8, 5))
    plt.scatter(popular["score"], popular["num_comments"], label="Popular")
    plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.title("Score vs Comments")
    plt.legend()

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/chart3_scatter.png")
    plt.close()

    # Combimed Dashboard
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Chart 1
    axes[0].barh(top10["short_title"], top10["score"])
    axes[0].set_title("Top Stories")
    axes[0].invert_yaxis()

    # Chart 2
    axes[1].bar(category_counts.index, category_counts.values)
    axes[1].set_title("Categories")

    # Chart 3
    axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
    axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
    axes[2].set_title("Score vs Comments")
    axes[2].legend()

    fig.suptitle("TrendPulse Dashboard")

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/dashboard.png")
    plt.close()

    print("Charts saved in outputs/ folder")


if __name__ == "__main__":
    main()
