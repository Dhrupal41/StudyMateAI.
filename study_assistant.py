from ai_helper import generate_response

def explain_topic(subject, topic, level):
    instruction = """"
    You are StudyMate AI, a fridenly educational tutor.

    Explain topic accurately using language suitable
    for the student's learning level.


    Include:
    1.A simple defination
    2.A step-by-step explanation
    3.A practical example
    4.A short summary
    """

    prompt = f"""
    subject: {subject}
    topic: {topic}
    level: {level}

    Explain this topic so the student can understand it easily.
    """

    return generate_response(instruction, prompt)    