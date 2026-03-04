from llm_helper import llm
from few_shot import FewShotPosts

# Load processed dataset and few-shot examples
few_shot = FewShotPosts()


def get_length_str(length):
    """
    Convert length category into actual line range.
    This helps the LLM understand how long the post should be.
    """

    if length == "Short":
        return "1 to 5 lines"

    if length == "Medium":
        return "6 to 10 lines"

    if length == "Long":
        return "11 to 15 lines"


def generate_post(length, language, tag):
    """
    Main function used by the Streamlit app.

    Steps:
    1. Build the prompt
    2. Send prompt to LLM
    3. Return generated text
    """

    prompt = get_prompt(length, language, tag)

    response = llm.invoke(prompt)

    return response.content


def get_prompt(length, language, tag):
    """
    Build the prompt that will be sent to the LLM.
    This includes:
    - topic
    - language
    - length
    - few-shot examples
    """

    # Convert length category to text
    length_str = get_length_str(length)

    # Base prompt
    prompt = f"""
Generate a LinkedIn post using the below information. No preamble.

1) Topic: {tag}
2) Length: {length_str}
3) Language: English

Write the post fully in English.
"""

    # Fetch similar examples from dataset
    examples = few_shot.get_filtered_posts(length, language, tag)

    # If examples exist, include them in prompt
    if len(examples) > 0:

        prompt += "\n4) Use the writing style as per the following examples."

    # Add up to 2 few-shot examples
    for i, post in enumerate(examples):

        post_text = post["text"]

        # Limit example size to reduce token usage
        short_example = "\n".join(post_text.split("\n")[:4])

        prompt += f"\n\nExample {i + 1}:\n\n{short_example}"

        # Only include 2 examples
        if i == 1:
            break

    return prompt


# Test the generator directly
if __name__ == "__main__":

    print(generate_post("Medium", "English", "Mental Health"))