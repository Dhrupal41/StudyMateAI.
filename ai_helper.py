
import os
import re

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_prompt_value(prompt, field):
    pattern = rf"^\s*{re.escape(field)}:\s*(.*?)\s*$"

    match = re.search(
        pattern,
        prompt,
        re.MULTILINE | re.IGNORECASE
    )

    return match.group(1).strip() if match else "Unknown"


def generate_mock_response(instructions, prompt):

    subject = get_prompt_value(prompt, "Subject")
    level = get_prompt_value(prompt, "Student Level")
    topic = get_prompt_value(prompt, "Topic")

    instruction_text = instructions.lower()

    heading = f"# {topic}\n\n"
    details = (
        f"**Subject:** {subject}\n\n"
        f"**Level:** {level}\n\n"
        "**Mode:** Free Mock Mode\n\n"
        "---\n\n"
    )

    if "quiz generator" in instruction_text:

        content = f"""
## Quiz: {topic}

Here are 5 sample questions for practice.

**1. What is {topic} mainly used for?**

A. Understanding and solving a relevant problem  
B. Making a computer heavier  
C. Increasing screen brightness  
D. Replacing the operating system  

**2. Which is the best way to learn {topic}?**

A. Avoid examples  
B. Practice with examples  
C. Skip the basics  
D. Memorize without understanding  

**3. What should a beginner understand first?**

A. Advanced techniques  
B. Basic concepts  
C. Complex projects only  
D. Nothing about the topic  

**4. Why is practical knowledge important?**

A. It helps apply concepts  
B. It removes all errors  
C. It replaces learning  
D. It stops development  

**5. What helps improve your understanding?**

A. Regular practice  
B. Avoiding questions  
C. Skipping revision  
D. Never testing code  

### Demo Answer Key

1. A
2. B
3. B
4. A
5. A

*These are general demonstration questions, not verified topic-specific quiz questions.*
"""

    elif "notes generator" in instruction_text:

        content = f"""
## 1. Introduction

{topic} is the topic you selected to study in {subject}.

## 2. Basic Understanding

Start by understanding the meaning and purpose of {topic}.

## 3. Important Concepts

- Learn the basic definition.
- Understand the main concepts.
- Study how the topic works.
- Explore practical examples.

## 4. Examples

Find or create a simple example related to {topic}.

## 5. Advantages

- Helps develop subject knowledge.
- Builds practical understanding.
- Supports further learning.

## 6. Quick Revision

Review the definition, key concepts, and examples of {topic}.

*These are demonstration notes, not verified topic-specific notes.*
"""

    else:

        content = f"""
## 1. Introduction

Welcome to your lesson about {topic}!

## 2. Basic Understanding

First, understand what {topic} means and why it is useful in {subject}.

## 3. Important Concepts

- Learn the basic definition of {topic}.
- Understand its purpose.
- Explore its main concepts.
- Practice using simple examples.

## 4. Practical Learning

Try a beginner-level exercise related to {topic}.

## 5. Summary

Review the key concepts and practice regularly.

*This is demonstration content, not a complete verified explanation of {topic}.*
"""

    return heading + details + content


def generate_response(instructions, prompt):

    mode = os.getenv("STUDYMATE_MODE", "mock").strip().lower()

    if mode == "mock":
        return generate_mock_response(instructions, prompt)

    elif mode == "live":

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OpenAI API key is missing.")

        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model="gpt-5.5",
            instructions=instructions,
            input=prompt
        )

        return response.output_text

    else:
        raise ValueError(
            "Invalid STUDYMATE_MODE. Use mock or live."
        )
