from ai_helper import generate_response

def explain_topic(subject, topic, level):
    instruction = """
    You are StudyMate AI, an educational notes generator.

    Create accurate, organized study notes appropriate
    for the student's learning level.


    Include:
    1. Defination
    2. Important points
    3. key points
    4. Example
    5. Short revision summary
    """

    prompt = f"""
    subject: {subject}
    topic: {topic}
    level: {level}

    Generate useful revision notes for this topic.
    """

    return generate_response(instruction, prompt)