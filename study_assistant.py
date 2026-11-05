from ai_helper import generate_response


def explain_topic(subject, level, topic):
    instructions = """
You are StudyMate AI, a friendly educational assistant.
Explain concepts in simple language suitable for the student's level.
Use accurate information, examples, and step-by-step explanations.
"""

    prompt = f"""
Subject: {subject}
Student Level: {level}
Topic: {topic}

Explain this topic in an easy-to-understand way.
Include:
1. Introduction
2. Simple explanation
3. Important concepts
4. Real-life or practical examples
5. Summary
"""

    return generate_response(instructions, prompt)
