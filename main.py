import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post


# Length options for post generation
length_options = ["Short", "Medium", "Long"]


def main():

    st.subheader("AI Social Media Post Generator")

    # Create two columns for UI inputs
    col1, col2 = st.columns(2)

    # Load dataset
    fs = FewShotPosts()
    tags = fs.get_tags()

    with col1:
        selected_tag = st.selectbox("Topic", options=tags)

    with col2:
        selected_length = st.selectbox("Length", options=length_options)


    # Generate button
    if st.button("Generate Post"):

        post = generate_post(
            selected_length,
            "English",
            selected_tag
        )

        st.write(post)


if __name__ == "__main__":
    main()