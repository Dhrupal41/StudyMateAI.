
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
    initial_sidebar_state="collapsed"
)


# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

#MainMenu, footer, header {
    visibility: hidden;
}

[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none;
}

.stApp {
    background:
        radial-gradient(circle at top left, #172554 0%, transparent 35%),
        radial-gradient(circle at bottom right, #312e81 0%, transparent 30%),
        #080d1b;
    color: #f8fafc;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3, h4 {
    color: #f8fafc !important;
    text-align: center;
}

p, label, li {
    color: #cbd5e1;
}

/* HERO */

.hero {
    text-align: center;
    padding: 45px 15px 30px;
}

.hero-title {
    font-size: clamp(38px, 6vw, 64px);
    font-weight: 900;
    letter-spacing: -2px;
    background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #cbd5e1;
    font-size: 18px;
    margin-top: 12px;
}

/* DASHBOARD CARDS */

.feature-card {
    background: linear-gradient(
        145deg,
        rgba(30, 41, 75, 0.95),
        rgba(15, 23, 42, 0.95)
    );
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 20px;
    padding: 28px 20px;
    min-height: 190px;
    text-align: center;
    transition: all 0.3s ease;
    box-shadow: 0 8px 25px rgba(0,0,0,0.18);
}

.feature-card:hover {
    transform: translateY(-9px) scale(1.02);
    border-color: #818cf8;
    box-shadow: 0 15px 35px rgba(99,102,241,0.25);
}

.feature-icon {
    font-size: 42px;
    margin-bottom: 12px;
}

.feature-title {
    color: white;
    font-size: 21px;
    font-weight: 800;
    margin-bottom: 9px;
}

.feature-description {
    color: #cbd5e1;
    font-size: 14px;
    line-height: 1.5;
}

/* BUTTONS */

div.stButton > button,
div[data-testid="stDownloadButton"] button,
div[data-testid="stFormSubmitButton"] button {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    border-radius: 12px;
    border: 1px solid rgba(129, 140, 248, 0.45);
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    color: white;
    font-weight: 700;
    padding: 12px 15px;
    transition: all 0.25s ease;
}

div.stButton > button:hover,
div[data-testid="stDownloadButton"] button:hover {
    transform: translateY(-2px);
    border-color: #c4b5fd;
    box-shadow: 0 7px 20px rgba(124,58,237,0.3);
    color: white;
}

/* INPUTS */

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: #111827;
    color: white;
    border: 1px solid #475569;
    border-radius: 10px;
    text-align: center;
}

div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stRadio"] > label {
    width: 100%;
    justify-content: center;
    text-align: center;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #111827;
    color: white;
}

div[data-testid="stRadio"] > div {
    justify-content: center;
    text-align: center;
}

div[data-testid="stMetric"] {
    text-align: center;
}

div[data-testid="stCaptionContainer"] {
    text-align: center;
}

/* PROGRESS */

div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #6366f1, #ec4899);
}

/* SECTION CARDS */

.section-card {
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 15px;
    text-align: center;
}

.small-note {
    color: #94a3b8;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# =========================================
# SESSION STATE
# =========================================

defaults = {
    "current_page": "Dashboard",
    "learning_mode": "Explain Topic",
    "roadmap_result": "",
    "roadmap_config": {},
    "chat_history": [],
    "quiz_questions": [],
    "quiz_submitted": False,
    "quiz_answers": {},
    "quiz_topic": "",
    "explanation_result": "",
    "notes_result": "",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================
# NAVIGATION
# =========================================

def open_page(page, learning_mode=None):

    st.session_state.current_page = page

    if learning_mode:
        st.session_state.learning_mode = learning_mode

    st.rerun()


def back_to_home():

    if st.button("← Back to Home", key="back_home"):
        open_page("Dashboard")


# =========================================
# HELPER FUNCTIONS
# =========================================

def show_result(result):

    if result is None:
        st.warning("No result was generated. Please try again.")
        return

    if isinstance(result, str):
        st.markdown(result)
    else:
        st.write(result)


def call_generator(function, argument_sets):

    last_error = None

    for args in argument_sets:

        try:
            return function(*args)

        except TypeError as error:
            last_error = error

    if last_error:
        raise last_error


# =========================================
# DASHBOARD
# =========================================

def dashboard():

    st.markdown("""
    <div class="hero">
        <div class="hero-title">🎓 StudyMate AI</div>
        <div class="hero-subtitle">
            Your personal AI-powered learning companion
        </div>
        <p style="color:#94a3b8; margin-top:15px;">
            Learn smarter • Practise better • Build your future
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<h3>Explore Your Learning Space</h3>",
        unsafe_allow_html=True
    )

    features = [
        (
            "📖", "Learning Studio",
            "Understand topics and generate study notes.",
            "Learning Studio", None
        ),
        (
            "📄", "PDF Notes",
            "Generate notes and download them as PDF.",
            "Learning Studio", "Generate Notes"
        ),
        (
            "🧠", "Interactive Quiz",
            "Test your knowledge and check your score.",
            "Learning Studio", "Generate Quiz"
        ),
        (
            "💬", "Chat Tutor",
            "Ask questions and learn through conversation.",
            "Chat Tutor", None
        ),
        (
            "🚀", "Career Roadmap",
            "Explore career paths and track your progress.",
            "Career Roadmap", None
        ),
        (
            "ℹ️", "About StudyMate",
            "Learn about StudyMate AI.",
            "About", None
        ),
    ]

    for row_start in range(0, len(features), 3):

        columns = st.columns(3, gap="large")

        for column, feature in zip(
            columns,
            features[row_start:row_start + 3]
        ):

            icon, title, description, page, mode = feature

            with column:

                st.markdown(f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-description">
                        {description}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(
                    f"Open {title}",
                    key=f"open_{title}"
                ):
                    open_page(page, mode)


# =========================================
# LEARNING STUDIO
# =========================================

def learning_studio():

    back_to_home()

    st.title("📖 Learning Studio")

    st.write(
        "Learn topics, generate notes and practise with quizzes."
    )

    modes = [
        "Explain Topic",
        "Generate Notes",
        "Generate Quiz",
    ]

    selected_mode = st.selectbox(
        "Choose Learning Mode",
        modes,
        index=(
            modes.index(st.session_state.learning_mode)
            if st.session_state.learning_mode in modes
            else 0
        ),
        key="learning_mode_selector"
    )

    st.session_state.learning_mode = selected_mode

    st.divider()

    subject = st.selectbox(
        "Select Subject",
        [
            "Python",
            "NumPy",
            "Pandas",
            "Artificial Intelligence",
            "Machine Learning",
            "Data Science",
            "Web Development",
            "Computer Science",
            "Other",
        ],
        key="learning_subject"
    )

    level = st.selectbox(
        "Select Student Level",
        ["Beginner", "Intermediate", "Advanced"],
        key="learning_level"
    )

    topic = st.text_input(
        "Enter Topic",
        placeholder="Example: Python Functions",
        key="learning_topic"
    )

    # EXPLAIN TOPIC

    if selected_mode == "Explain Topic":

        if st.button("✨ Explain Topic", key="explain_button"):

            if not topic.strip():

                st.warning("Please enter a topic.")

            else:

                with st.spinner("Preparing your explanation..."):

                    try:

                        result = call_generator(
                            explain_topic,
                            [
                                (subject, level, topic),
                                (subject, topic, level),
                                (topic, subject, level),
                                (topic,),
                            ]
                        )

                        st.session_state.explanation_result = result

                    except Exception as error:
                        st.error(f"Error: {error}")

        if st.session_state.explanation_result:

            st.divider()
            show_result(st.session_state.explanation_result)

    # GENERATE NOTES

    elif selected_mode == "Generate Notes":

        if st.button("📝 Generate Notes", key="notes_button"):

            if not topic.strip():

                st.warning("Please enter a topic.")

            else:

                with st.spinner("Generating your notes..."):

                    try:

                        result = call_generator(
                            generate_notes,
                            [
                                (subject, level, topic),
                                (subject, topic, level),
                                (topic, subject, level),
                                (topic,),
                            ]
                        )

                        st.session_state.notes_result = result

                    except Exception as error:
                        st.error(f"Error: {error}")

        notes_result = st.session_state.notes_result

        if notes_result:

            st.divider()
            show_result(notes_result)

            if isinstance(notes_result, str):

                st.download_button(
                    "⬇️ Download Notes as Markdown",
                    data=notes_result,
                    file_name="StudyMate_Notes.md",
                    mime="text/markdown",
                    key="download_notes_md"
                )

                try:

                    pdf_file = generate_notes_pdf(
                        notes_result,
                        "StudyMate Notes",
                        level,
                        topic
                    )

                    if pdf_file:

                        st.download_button(
                            "📄 Download Notes as PDF",
                            data=pdf_file,
                            file_name="StudyMate_Notes.pdf",
                            mime="application/pdf",
                            key="download_notes_pdf"
                        )

                except Exception as error:
                    st.info(f"PDF generation issue: {error}")

    # GENERATE QUIZ

    elif selected_mode == "Generate Quiz":

        if st.button(
            "🧠 Generate Quiz",
            key="generate_quiz_button"
        ):

            if not topic.strip():

                st.warning("Please enter a quiz topic.")

            else:

                with st.spinner("Preparing quiz questions..."):

                    try:

                        questions = call_generator(
                            get_quiz_questions,
                            [
                                (subject, level, topic),
                                (subject, topic, level),
                                (topic, subject, level),
                                (topic,),
                            ]
                        )

                        if isinstance(questions, dict):
                            questions = questions.get("questions", [])

                        st.session_state.quiz_questions = questions or []
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_topic = topic

                    except Exception as error:
                        st.error(f"Quiz error: {error}")

        if st.session_state.quiz_questions:
            display_quiz()


# =========================================
# INTERACTIVE QUIZ
# =========================================

def display_quiz():

    questions = st.session_state.quiz_questions

    st.divider()

    st.subheader(
        f"🧠 Quiz: {st.session_state.quiz_topic}"
    )

    if not st.session_state.quiz_submitted:

        with st.form("quiz_form"):

            for index, question in enumerate(questions):

                question_text = question.get(
                    "question",
                    f"Question {index + 1}"
                )

                options = question.get("options", [])

                st.markdown(
                    f"**Q{index + 1}. {question_text}**"
                )

                if options:

                    answer = st.radio(
                        "Choose your answer",
                        options,
                        key=f"quiz_answer_{index}",
                        index=None
                    )

                    st.session_state.quiz_answers[index] = answer

                st.write("")

            submitted = st.form_submit_button(
                "Submit Quiz",
                use_container_width=True
            )

            if submitted:

                st.session_state.quiz_submitted = True
                st.rerun()

    else:

        score = 0
        total = len(questions)

        for index, question in enumerate(questions):

            correct_answer = question.get(
                "answer",
                question.get("correct_answer", "")
            )

            user_answer = st.session_state.quiz_answers.get(index)

            if user_answer == correct_answer:
                score += 1

        percentage = score / total * 100 if total else 0

        st.markdown("## 🏆 Quiz Result")

        col1, col2, col3 = st.columns(3)

        col1.metric("Correct Answers", f"{score}/{total}")
        col2.metric("Percentage", f"{percentage:.1f}%")

        col3.metric(
            "Performance",
            "Excellent" if percentage >= 80
            else "Good" if percentage >= 60
            else "Keep Practising"
        )

        st.progress(percentage / 100)

        st.divider()

        st.subheader("📋 Answer Review")

        for index, question in enumerate(questions):

            correct_answer = question.get(
                "answer",
                question.get("correct_answer", "")
            )

            user_answer = st.session_state.quiz_answers.get(index)

            st.markdown(
                f"**Q{index + 1}. {question.get('question', '')}**"
            )

            st.write(f"Your answer: {user_answer or 'Not answered'}")
            st.write(f"Correct answer: {correct_answer}")

            if user_answer == correct_answer:
                st.success("Correct answer!")
            else:
                st.error("Incorrect answer.")

            explanation = question.get("explanation")

            if explanation:
                st.info(f"Explanation: {explanation}")

            st.divider()

        if st.button("🔄 Try Again", key="try_again"):

            st.session_state.quiz_submitted = False
            st.session_state.quiz_answers = {}

            st.rerun()


# =========================================
# CAREER ROADMAP
# =========================================

def career_roadmap_page():

    back_to_home()

    st.title("🚀 Career Roadmap")

    st.write(
        "Discover your career path and follow a structured learning plan."
    )

    st.markdown("""
    <div class="section-card">
        <h3>🎯 Build Your Future</h3>
        <p>
            Select your career category, enter your goal and choose
            your current level. StudyMate AI will create a roadmap
            with skills, projects, tools and a portfolio checklist.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # CATEGORY

    selected_category = st.selectbox(
        "Select Career Category",
        CAREER_CATEGORIES,
        key="career_category"
    )

    # DYNAMIC EXAMPLES

    selected_examples = CAREER_EXAMPLES.get(
        selected_category,
        CAREER_EXAMPLES.get("Auto-detect", [])
    )

    if selected_examples:

        st.caption(
            "Career examples: " + " • ".join(selected_examples)
        )

        example_text = " or ".join(selected_examples[:2])

    else:

        example_text = "your desired career"

    # CAREER GOAL

    career_goal = st.text_input(
        "Enter Your Career Goal",
        placeholder=f"Example: {example_text}",
        key="career_goal"
    )

    # LEVEL

    roadmap_level = st.selectbox(
        "Your Current Level",
        ["Beginner", "Intermediate", "Advanced"],
        key="career_level"
    )

    st.write("")

    # GENERATE ROADMAP

    if st.button(
        "🚀 Generate My Career Roadmap",
        key="generate_roadmap_button"
    ):

        if not career_goal.strip():

            st.warning("Please enter your career goal.")

        else:

            is_valid, detected_category = validate_career_goal(
                career_goal,
                selected_category
            )

            if not is_valid:

                st.session_state.roadmap_result = ""
                st.session_state.roadmap_config = {}

                st.error(
                    f"Your selected category is {selected_category}, "
                    f"but this career belongs to {detected_category}."
                )

                st.warning(
                    f"Please select {detected_category} "
                    "or enter a career related to your selected category."
                )

            else:

                try:

                    with st.spinner(
                        "Generating your career roadmap..."
                    ):

                        result = generate_roadmap(
                            career_goal,
                            selected_category,
                            roadmap_level
                        )

                        st.session_state.roadmap_result = result

                        st.session_state.roadmap_config = {
                            "career_goal": career_goal,
                            "category": (
                                detected_category
                                if selected_category == "Auto-detect"
                                else selected_category
                            ),
                            "level": roadmap_level,
                        }

                except Exception as error:

                    st.error(f"Roadmap error: {error}")

    # DISPLAY ROADMAP

    if st.session_state.roadmap_result:

        st.divider()

        roadmap_text = st.session_state.roadmap_result

        checklist_pattern = (
            r"(?ms)^##\s*🏆\s*Portfolio Checklist\s*\n"
            r"(.*?)(?=^##\s|\Z)"
        )

        checklist_match = re.search(
            checklist_pattern,
            roadmap_text
        )

        if checklist_match:

            checklist_section = checklist_match.group(1)

            checklist_items = re.findall(
                r"^\s*-\s*\[\s*\]\s*(.+)$",
                checklist_section,
                re.MULTILINE
            )

            before_checklist = roadmap_text[:checklist_match.start()]
            after_checklist = roadmap_text[checklist_match.end():]

            st.markdown(before_checklist)

            st.markdown("## 🏆 Portfolio Checklist")

            st.caption(
                "Click each checkbox when you complete a task."
            )

            safe_goal = re.sub(
                r"[^a-zA-Z0-9]+",
                "_",
                st.session_state.roadmap_config.get(
                    "career_goal",
                    "career"
                )
            ).strip("_").lower()

            completed = 0

            for index, item in enumerate(checklist_items):

                checked = st.checkbox(
                    item,
                    key=f"portfolio_{safe_goal}_{index}"
                )

                if checked:
                    completed += 1

            total_items = len(checklist_items)

            if total_items:

                progress = completed / total_items

                st.progress(progress)

                st.caption(
                    f"Portfolio Progress: "
                    f"{completed}/{total_items} tasks completed"
                )

            st.markdown(after_checklist)

        else:

            st.markdown(roadmap_text)

            st.warning(
                "The portfolio checklist heading was not found. "
                "The roadmap is still displayed normally."
            )

        # DOWNLOAD OPTIONS

        st.divider()

        st.subheader("📥 Download Your Roadmap")

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(
                "⬇️ Download Markdown",
                data=roadmap_text,
                file_name="Career_Roadmap.md",
                mime="text/markdown",
                use_container_width=True
            )

        with col2:

            try:

                pdf_file = generate_notes_pdf(
                    roadmap_text,
                    "Career Roadmap",
                    st.session_state.roadmap_config.get(
                        "level",
                        "Beginner"
                    ),
                    st.session_state.roadmap_config.get(
                        "career_goal",
                        "Career"
                    )
                )

                if pdf_file:

                    st.download_button(
                        "📄 Download PDF",
                        data=pdf_file,
                        file_name="Career_Roadmap.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

            except Exception as error:

                st.warning(f"PDF generation issue: {error}")


# =========================================
# CHAT TUTOR
# =========================================

def chat_tutor():

    back_to_home()

    st.title("💬 Chat Tutor")

    st.write(
        "Ask questions, understand concepts and learn step by step."
    )

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_prompt = st.chat_input(
        "Ask your study question..."
    )

    if user_prompt:

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_prompt
        })

        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    response = generate_chat_response(user_prompt)

                    if not isinstance(response, str):
                        response = str(response)

                    st.markdown(response)

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response
                    })

                except Exception as error:

                    error_message = (
                        f"Unable to generate a response: {error}"
                    )

                    st.error(error_message)

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": error_message
                    })

    if st.session_state.chat_history:

        if st.button("🗑️ Clear Chat", key="clear_chat"):

            st.session_state.chat_history = []

            st.rerun()


# =========================================
# ABOUT PAGE
# =========================================

def about_page():

    back_to_home()

    st.title("ℹ️ About StudyMate AI")

    st.markdown("""
    <div class="section-card">
        <h2>🎓 StudyMate AI</h2>
        <p>
            StudyMate AI is a learning assistant designed to help students
            understand concepts, create notes, practise quizzes and explore
            career opportunities.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("✨ Features")

    features = [
        "📖 Learning Studio – Learn and understand topics.",
        "📝 Notes Generator – Create structured study notes.",
        "📄 PDF Downloads – Save notes and roadmaps.",
        "🧠 Interactive Quiz – Test your knowledge.",
        "💬 Chat Tutor – Ask questions and get explanations.",
        "🚀 Career Roadmap – Plan your future career.",
        "🏆 Portfolio Checklist – Track completed career tasks.",
    ]

    for feature in features:
        st.markdown(f"- {feature}")

    st.divider()

    st.caption(
        "StudyMate AI | Learn smarter. Build better. Grow faster."
    )


# =========================================
# MAIN APP ROUTER
# =========================================

page = st.session_state.current_page

if page == "Dashboard":

    dashboard()

elif page == "Learning Studio":

    learning_studio()

elif page == "Career Roadmap":

    career_roadmap_page()

elif page == "Chat Tutor":

    chat_tutor()

elif page == "About":

    about_page()

else:

    st.session_state.current_page = "Dashboard"
    st.rerun()
