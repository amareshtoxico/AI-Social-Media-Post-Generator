import pandas as pd
import json


class FewShotPosts:
    """
    This class loads the processed dataset and
    selects example posts for few-shot prompting.
    """

    def __init__(self, file_path="data/processed_posts.json"):

        self.df = None
        self.unique_tags = None

        # Load dataset
        self.load_posts(file_path)


    def load_posts(self, file_path):
        """
        Load processed_posts.json and convert it to a dataframe.
        """

        with open(file_path, encoding="utf-8") as f:

            posts = json.load(f)

            # Convert JSON to pandas dataframe
            self.df = pd.json_normalize(posts)

            # Create a column that categorizes post length
            self.df["length"] = self.df["line_count"].apply(self.categorize_length)

            # Collect all tags from dataset
            all_tags = self.df["tags"].apply(lambda x: x).sum()

            # Remove duplicate tags
            self.unique_tags = list(set(all_tags))

    def get_filtered_posts(self, length, language, tag):
        """
        Return posts that match:
        - selected length
        - selected language
        - selected tag

        Then sort by engagement so the best posts
        are used as few-shot examples.
        """

        df_filtered = self.df[
            (self.df["tags"].apply(lambda tags: tag in tags)) &
            (self.df["language"] == language) &
            (self.df["length"] == length)
            ]

        # Sort by engagement (highest first)
        df_filtered = df_filtered.sort_values(by="engagement", ascending=False)

        return df_filtered.to_dict(orient="records")


    def categorize_length(self, line_count):
        """
        Convert number of lines into categories.
        """

        if line_count < 5:
            return "Short"

        elif 5 <= line_count <= 10:
            return "Medium"

        else:
            return "Long"


    def get_tags(self):
        """
        Return unique tags from dataset.
        Used in the Streamlit dropdown.
        """

        return self.unique_tags


# Test the file independently
if __name__ == "__main__":

    fs = FewShotPosts()

    # Print all available tags
    print(fs.get_tags())

    # Example filtering
    posts = fs.get_filtered_posts("Medium", "English", "Job Search")

    print(posts)