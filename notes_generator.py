from ai_helper import generate_response


def generate_notes(subject, level, topic):
    instructions = """
You are StudyMate AI Notes Generator.
Create clear, organized, accurate and useful study notes.
Use headings, bullet points, definitions and examples.
"""

    prompt = f"""
Subject: {subject}
Student Level: {level}
Topic: {topic}

Generate study notes containing:
1. Topic introduction
2. Important definitions
3. Key points
4. Examples
5. Advantages and disadvantages, if relevant
6. Short revision summary
"""

    return generate_response(instructions, prompt)
