import streamlit as st

from study_assistant import explain_topic
import notes_generator
import quiz_generation

# Page configuration
st.set_page_config(
    page_title="StudyMate AI",
    page_icon="📚",
    layout="wide"
)

# Application title
st.title("📚 StudyMate AI")

st.subheader("Your Personal AI Study Assistant")

st.write(
    "Learn difficult topics, prepare revision notes, "
    "and practise with quizzes."
)

st.divider()

# Select subject
subject = st.selectbox(
    "Choose your subject",
    [
        "Python",
        "NumPy",
        "Pandas",
        "Artificial Intelligence",
        "Machine Learning",
        "Mathematics",
        "Other"
    ]
)

# Select learning level
level = st.selectbox(
    "Choose your learning level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

# Enter a topic
topic = st.text_input(
    "What do you want to learn?",
    placeholder="Example: NumPy arrays"
)

# Select a learning tool
feature = st.radio(
    "Choose what you want",
    [
        "Explain Topic",
        "Generate Notes",
        "Generate Quiz"
    ],
    horizontal=True
)

# Submit button
if st.button("Start Learning"):
    if not topic.strip():
        st.warning("Please enter a topic first.")

    else:
        try:
            with st.spinner("StudyMate AI is preparing your content..."):

                if feature == "Explain Topic":
                    result = explain_topic(subject, topic, level)
                    st.markdown(result)

                elif feature == "Generate Notes":
                    result = notes_generator.generate_notes(subject, topic, level)
                    st.markdown(result)

                elif feature == "Generate Quiz":
                    result = quiz_generation.generate_quiz(subject, topic, level)
                    st.markdown(result)

            st.markdown(result)

        except Exception as error:
            st.error(
                f"Error type: {type(error).__name__}\n"
            )
            st.caption(str(error))        