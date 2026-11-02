from ai_helper import generate_response

def explain_topic(subject, topic, level):
    instruction = """
    You are StudyMate AI, a quiz generator.

    Create five multiple - choice questions about the topic.

    Each question must have:
    - Four anser options: A, B, C, and D
    - One correct answer
    - A short explanation of the correct answer
    """

    prompt = f"""
    subject: {subject}
    topic: {topic}
    level: {level}

    Generate five practice questions for this topic.
    """

    return generate_response(instruction, prompt)