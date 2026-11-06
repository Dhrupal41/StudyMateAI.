
import re
import streamlit as st

from study_assistant import explain_topic
from notes_generator import generate_notes
from quiz_generation import get_quiz_questions
from pdf_generator import generate_notes_pdf
from ai_helper import generate_chat_response
from career_roadmap import (
    generate_roadmap,
    CAREER_CATEGORIES,
    CAREER_EXAMPLES,
    validate_career_goal,
)


# =========================================
# PAGE CONFIGURATION
# =========================================

st.set_page_config(
    page_title="StudyMate AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #25205b 0%, transparent 35%),
        radial-gradient(circle at 90% 20%, #24205a 0%, transparent 35%),
        linear-gradient(135deg, #090d1b, #11152b 55%, #0a1020);
    color: #f5f5ff;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3, p, label {
    color: #f5f5ff;
}

.hero {
    text-align: center;
    padding: 45px 15px 30px 15px;
}

.hero-tag {
    display: inline-block;
    padding: 8px 16px;
    border: 1px solid #6659c9;
    border-radius: 30px;
    background: #211d48;
    color: #c9c2ff;
    font-size: 13px;
    margin-bottom: 20px;
}

.hero h1 {
    font-size: clamp(38px, 6vw, 62px);
    font-weight: 800;
    margin-bottom: 12px;
    background: linear-gradient(90deg, #ffffff, #b7aaff, #83d7ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #b7bfd8;
    font-size: 17px;
}

.section-heading {
    text-align: center;
    font-size: 27px;
    font-weight: 750;
    margin-top: 30px;
    margin-bottom: 8px;
}

.section-subtitle {
    text-align: center;
    color: #aab3d0;
    margin-bottom: 25px;
}

.feature-card {
    background: linear-gradient(145deg, #1c2340, #151a31);
    border: 1px solid #343d62;
    border-radius: 20px;
    padding: 28px 22px;
    min-height: 225px;
    text-align: center;
    box-shadow: 0 10px 35px rgba(0,0,0,0.18);
    transition: 0.25s ease;
}

.feature-card:hover {
    border-color: #8b7cff;
    transform: translateY(-4px);
}

.feature-icon {
    font-size: 42px;
    margin-bottom: 12px;
}

.feature-card h3 {
    font-size: 21px;
    font-weight: 700;
    margin-bottom: 10px;
}

.feature-card p {
    font-size: 14px;
    line-height: 1.6;
    color: #b5bfd8;
}

.small-card {
    background: #171d35;
    border: 1px solid #303957;
    border-radius: 16px;
    padding: 22px;
    text-align: center;
    min-height: 130px;
}

.small-card h3 {
    font-size: 18px;
}

.small-card p {
    color: #b5bfd8;
    font-size: 13px;
}

div.stButton > button {
    border-radius: 12px;
    min-height: 44px;
    font-weight: 650;
    border: 1px solid #7568e8;
    background: linear-gradient(90deg, #6554d9, #8271f2);
    color: white;
    transition: 0.2s;
}

div.stButton > button:hover {
    border-color: #a99eff;
    background: linear-gradient(90deg, #7768ed, #9384ff);
    color: white;
}

div.stDownloadButton > button {
    border-radius: 10px;
    background: #252d4b;
    border: 1px solid #59658d;
    color: white;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: #171e36;
    color: white;
    border: 1px solid #394568;
    border-radius: 10px;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #171e36;
    color: white;
    border-radius: 10px;
}

div[data-testid="stRadio"] label {
    color: #e8eaff;
}

div[data-testid="stMetric"] {
    background: #171e36;
    border: 1px solid #343e61;
    padding: 15px;
    border-radius: 14px;
}

hr {
    border-color: #343d5d;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# =========================================
# SESSION STATE
# =========================================

DEFAULTS = {
    "current_page": "Dashboard",
    "learning_mode": "Explain Topic",
    "learning_mode_selector": "Explain Topic",
    "generated_notes": "",
    "notes_config": None,
    "explanation_result": "",
    "quiz_questions": [],
    "quiz_submitted": False,
    "quiz_config": None,
    "chat_history": [],
    "roadmap_result": "",
    "roadmap_goal": "",
    "roadmap_category": "",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================
# NAVIGATION
# =========================================

def open_page(page, learning_mode=None):
    st.session_state.current_page = page

    if learning_mode:
        st.session_state.learning_mode = learning_mode
        st.session_state.learning_mode_selector = learning_mode

    st.rerun()


def back_to_dashboard():
    open_page("Dashboard")


def page_header(title, description=""):
    if st.button("← Back to Dashboard", key=f"back_{title}"):
        back_to_dashboard()

    st.markdown(f"# {title}")

    if description:
        st.caption(description)

    st.divider()


# =========================================
# DASHBOARD
# =========================================

def dashboard():

    st.markdown("""
    <div class="hero">
        <div class="hero-tag">✨ YOUR AI-POWERED LEARNING PARTNER</div>
        <h1>Welcome to StudyMate AI</h1>
        <p>Learn smarter. Create notes. Test your knowledge. Build your future.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">What would you like to do today?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Choose a learning experience to get started.</div>',
        unsafe_allow_html=True
    )

    main_features = [
        {
            "title": "Learning Studio",
            "icon": "📚",
            "description": "Understand topics, generate study notes and practise with interactive quizzes.",
            "button": "Start Learning",
            "page": "Learning Studio",
            "mode": "Explain Topic",
        },
        {
            "title": "PDF Notes",
            "icon": "📄",
            "description": "Create organised study notes and download them as PDF documents.",
            "button": "Create Notes",
            "page": "Learning Studio",
            "mode": "Generate Notes",
        },
        {
            "title": "Chat Tutor",
            "icon": "🤖",
            "description": "Ask questions and get explanations from your AI study companion.",
            "button": "Open Chat Tutor",
            "page": "Chat Tutor",
            "mode": None,
        },
    ]

    columns = st.columns(3, gap="large")

    for index, feature in enumerate(main_features):
        with columns[index]:

            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{feature['icon']}</div>
                <h3>{feature['title']}</h3>
                <p>{feature['description']}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                feature["button"],
                key=f"main_{feature['title']}",
                use_container_width=True
            ):
                open_page(
                    feature["page"],
                    feature["mode"]
                )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">Explore More</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Tools to help you plan and grow.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="small-card">
            <h3>🚀 Career Roadmap</h3>
            <p>Explore career paths and create a step-by-step learning plan.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Explore Career Roadmap",
            key="career_dashboard",
            use_container_width=True
        ):
            open_page("Career Roadmap")

    with col2:
        st.markdown("""
        <div class="small-card">
            <h3>ℹ️ About StudyMate AI</h3>
            <p>Discover the features and purpose of your learning companion.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "About StudyMate AI",
            key="about_dashboard",
            use_container_width=True
        ):
            open_page("About")

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; color:#8792b3; font-size:13px;">
        Made for curious minds 💜 | StudyMate AI
    </div>
    """, unsafe_allow_html=True)


# =========================================
# LEARNING STUDIO
# =========================================

def learning_studio():

    page_header(
        "📚 Learning Studio",
        "Understand concepts, create notes and test your knowledge."
    )

    modes = [
        "Explain Topic",
        "Generate Notes",
        "Generate Quiz",
    ]

    current_mode = st.session_state.learning_mode_selector

    if current_mode not in modes:
        current_mode = "Explain Topic"

    selected_mode = st.selectbox(
        "Choose your learning tool",
        modes,
        index=modes.index(current_mode),
        key="learning_mode_selector"
    )

    st.session_state.learning_mode = selected_mode

    st.markdown("### Learning Details")

    col1, col2 = st.columns(2)

    with col1:
        subject = st.text_input(
            "Subject",
            placeholder="Example: Python"
        )

    with col2:
        level = st.selectbox(
            "Student Level",
            ["Beginner", "Intermediate", "Advanced"]
        )

    topic = st.text_input(
        "Topic",
        placeholder="Example: Python Functions"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------
    # EXPLAIN TOPIC
    # -------------------------------------

    if selected_mode == "Explain Topic":

        if st.button("✨ Explain Topic", use_container_width=True):

            if not subject.strip() or not topic.strip():
                st.warning("Please enter both subject and topic.")

            else:
                with st.spinner("Preparing your explanation..."):

                    try:
                        result = explain_topic(
                            subject,
                            level,
                            topic
                        )

                        st.session_state.explanation_result = result

                    except Exception as error:
                        st.error(
                            f"Error type: {type(error).__name__}"
                        )
                        st.exception(error)

        if st.session_state.explanation_result:
            st.markdown("### 📖 Your Explanation")
            st.markdown(st.session_state.explanation_result)

    # -------------------------------------
    # GENERATE NOTES
    # -------------------------------------

    elif selected_mode == "Generate Notes":

        if st.button("📝 Generate Notes", use_container_width=True):

            if not subject.strip() or not topic.strip():
                st.warning("Please enter both subject and topic.")

            else:
                with st.spinner("Creating your notes..."):

                    try:
                        result = generate_notes(
                            subject,
                            level,
                            topic
                        )

                        st.session_state.generated_notes = result
                        st.session_state.notes_config = {
                            "subject": subject,
                            "level": level,
                            "topic": topic,
                        }

                    except Exception as error:
                        st.error(
                            f"Error type: {type(error).__name__}"
                        )
                        st.exception(error)

        if st.session_state.generated_notes:

            st.markdown("### 📄 Generated Notes")
            st.markdown(st.session_state.generated_notes)

            config = st.session_state.notes_config

            if config:
                try:
                    pdf_file = generate_notes_pdf(
                        st.session_state.generated_notes,
                        config["subject"],
                        config["level"],
                        config["topic"]
                    )

                    safe_topic = re.sub(
                        r"[^a-zA-Z0-9_-]",
                        "_",
                        config["topic"]
                    )

                    st.download_button(
                        "⬇️ Download Notes as PDF",
                        data=pdf_file,
                        file_name=f"{safe_topic}_notes.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                except Exception as error:
                    st.error("Could not create the PDF.")
                    st.exception(error)

    # -------------------------------------
    # GENERATE QUIZ
    # -------------------------------------

    elif selected_mode == "Generate Quiz":

        if st.button("🧠 Generate Quiz", use_container_width=True):

            if not subject.strip() or not topic.strip():
                st.warning("Please enter both subject and topic.")

            else:
                with st.spinner("Preparing your quiz..."):

                    try:
                        questions = get_quiz_questions(
                            subject,
                            level,
                            topic
                        )

                        st.session_state.quiz_questions = questions
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_config = {
                            "subject": subject,
                            "level": level,
                            "topic": topic,
                        }

                    except Exception as error:
                        st.error(
                            f"Error type: {type(error).__name__}"
                        )
                        st.exception(error)

        questions = st.session_state.quiz_questions

        if questions:

            st.markdown("### 📝 Your Quiz")

            if not st.session_state.quiz_submitted:

                with st.form("quiz_form"):

                    for index, question in enumerate(questions):

                        question_text = question.get(
                            "question",
                            f"Question {index + 1}"
                        )

                        st.markdown(
                            f"**Q{index + 1}. {question_text}**"
                        )

                        options = question.get("options", [])

                        st.radio(
                            "Choose your answer",
                            options,
                            key=f"quiz_answer_{index}",
                            index=None
                        )

                        st.markdown("---")

                    submitted = st.form_submit_button(
                        "Submit Quiz",
                        use_container_width=True
                    )

                    if submitted:
                        st.session_state.quiz_submitted = True
                        st.rerun()

            else:

                score = 0

                for index, question in enumerate(questions):

                    correct_answer = question.get("answer")
                    selected_answer = st.session_state.get(
                        f"quiz_answer_{index}"
                    )

                    if selected_answer == correct_answer:
                        score += 1

                total = len(questions)

                st.metric(
                    "Your Score",
                    f"{score} / {total}"
                )

                if total:
                    st.progress(score / total)

                if score == total:
                    st.success("Excellent! You got every answer correct.")
                elif score >= total / 2:
                    st.info("Good effort! Keep practising.")
                else:
                    st.warning("Keep learning and try again.")

                st.markdown("### Answer Review")

                for index, question in enumerate(questions):

                    selected_answer = st.session_state.get(
                        f"quiz_answer_{index}"
                    )

                    correct_answer = question.get("answer")

                    st.markdown(
                        f"**Q{index + 1}. {question.get('question', '')}**"
                    )

                    st.write(f"Your answer: {selected_answer}")
                    st.write(f"Correct answer: {correct_answer}")

                    explanation = question.get("explanation")

                    if explanation:
                        st.caption(explanation)

                    if selected_answer == correct_answer:
                        st.success("Correct")
                    else:
                        st.error("Incorrect")

                    st.markdown("---")

                if st.button("🔄 Try Again", use_container_width=True):

                    for index in range(total):
                        key = f"quiz_answer_{index}"

                        if key in st.session_state:
                            del st.session_state[key]

                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_questions = []
                    st.rerun()


# =========================================
# CHAT TUTOR
# =========================================

def chat_tutor():

    page_header(
        "🤖 Chat Tutor",
        "Ask questions and learn with your AI study companion."
    )

    st.markdown("### Start a Conversation")

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_prompt = st.chat_input(
        "Ask anything about your studies..."
    )

    if user_prompt:

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_prompt,
        })

        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:
                    response = generate_chat_response(
                        user_prompt,
                        st.session_state.chat_history[:-1]
                    )

                    st.markdown(response)

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response,
                    })

                except Exception as error:
                    st.error(
                        f"Error type: {type(error).__name__}"
                    )
                    st.exception(error)

    if st.session_state.chat_history:

        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()


# =========================================
# CAREER ROADMAP
# =========================================

def career_roadmap_page():

    page_header(
        "🚀 Career Roadmap",
        "Create a learning roadmap for your future career."
    )

    st.markdown("### Choose Your Career Category")

    categories = list(CAREER_CATEGORIES)

    selected_category = st.selectbox(
        "Select your stream",
        categories
    )

    selected_examples = CAREER_EXAMPLES.get(
        selected_category,
        []
    )

    if selected_examples:
        example_text = ", ".join(
            str(example) for example in selected_examples[:2]
        )
    else:
        example_text = "Example: Your preferred career"

    career_goal = st.text_input(
        "Enter your career goal",
        placeholder=example_text
    )

    roadmap_level = st.selectbox(
        "Your current level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    if st.button(
        "Generate My Career Roadmap",
        use_container_width=True
    ):

        if not career_goal.strip():
            st.warning("Please enter a career goal.")

        else:

            is_valid, detected_stream = validate_career_goal(
                career_goal,
                selected_category
            )

            if not is_valid:

                st.session_state.roadmap_result = ""

                st.error(
                    f"Your selected stream is {selected_category}, "
                    f"but this career belongs to {detected_stream}."
                )

                st.warning(
                    f"Please select {detected_stream} or enter a career "
                    "related to your selected stream."
                )

            else:

                with st.spinner("Building your career roadmap..."):

                    try:
                        result = generate_roadmap(
                            career_goal,
                            selected_category,
                            roadmap_level
                        )

                        st.session_state.roadmap_result = result
                        st.session_state.roadmap_goal = career_goal
                        st.session_state.roadmap_category = selected_category

                    except Exception as error:
                        st.error(
                            f"Error type: {type(error).__name__}"
                        )
                        st.exception(error)

    if st.session_state.roadmap_result:

        st.markdown("---")
        st.markdown("### 🎯 Your Career Roadmap")

        st.markdown(st.session_state.roadmap_result)

        roadmap_text = st.session_state.roadmap_result

        safe_goal = re.sub(
            r"[^a-zA-Z0-9_-]",
            "_",
            st.session_state.roadmap_goal
        )

        st.download_button(
            "⬇️ Download Roadmap as Markdown",
            data=roadmap_text,
            file_name=f"{safe_goal}_roadmap.md",
            mime="text/markdown",
            use_container_width=True
        )

        try:
            roadmap_pdf = generate_notes_pdf(
                roadmap_text,
                "Career Roadmap",
                roadmap_level,
                st.session_state.roadmap_goal
            )

            st.download_button(
                "📄 Download Roadmap as PDF",
                data=roadmap_pdf,
                file_name=f"{safe_goal}_roadmap.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        except Exception as error:
            st.warning("The Markdown download is available, but PDF creation failed.")
            st.caption(str(error))


# =========================================
# ABOUT PAGE
# =========================================

def about_page():

    page_header(
        "ℹ️ About StudyMate AI",
        "Your personal AI-powered study companion."
    )

    st.markdown("""
    ## 🎓 What is StudyMate AI?

    StudyMate AI is designed to make learning easier, smarter and more
    organised with the help of artificial intelligence.

    ## ✨ Main Features

    - **Learning Studio:** Understand difficult topics in simple language.
    - **AI Notes Generator:** Create structured notes for your subjects.
    - **PDF Downloads:** Save your notes for offline study.
    - **Interactive Quiz:** Test your knowledge and review your answers.
    - **Chat Tutor:** Ask questions and get learning support.
    - **Career Roadmap:** Explore career paths and plan your learning journey.

    ## 🎯 Our Goal

    To help students learn independently, improve their knowledge and
    prepare for their future careers.

    ---

    <div style="text-align:center; color:#aab3d0;">
        Made with 💜 for students.
    </div>
    """, unsafe_allow_html=True)


# =========================================
# MAIN PAGE ROUTER
# =========================================

current_page = st.session_state.current_page

if current_page == "Dashboard":
    dashboard()

elif current_page == "Learning Studio":
    learning_studio()

elif current_page == "Chat Tutor":
    chat_tutor()

elif current_page == "Career Roadmap":
    career_roadmap_page()

elif current_page == "About":
    about_page()

else:
    st.session_state.current_page = "Dashboard"
    st.rerun()
