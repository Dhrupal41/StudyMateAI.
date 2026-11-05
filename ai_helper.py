
import os
import re

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


# -----------------------------------------
# 1. GET VALUES FROM THE PROMPT
# -----------------------------------------

def get_prompt_value(prompt, field):

    pattern = rf"^\s*{re.escape(field)}:\s*(.*?)\s*$"

    match = re.search(
        pattern,
        prompt,
        re.MULTILINE | re.IGNORECASE
    )

    return match.group(1).strip() if match else "Not provided"


# -----------------------------------------
# 2. FREE MOCK MODE
# -----------------------------------------

def generate_mock_response(instructions, prompt):

    subject = get_prompt_value(prompt, "Subject")
    level = get_prompt_value(prompt, "Student Level")
    topic = get_prompt_value(prompt, "Topic")

    instruction_text = instructions.lower()
    topic_lower = topic.lower()

    heading = f"# {topic}\n\n"

    details = (
        f"**Subject:** {subject}\n\n"
        f"**Level:** {level}\n\n"
        "**Mode:** Free Mock Mode\n\n"
        "> Demonstration content for learning and testing.\n\n"
    )

    # -----------------------------------------
    # PYTHON FUNCTIONS TOPIC
    # -----------------------------------------

    if "function" in topic_lower and "python" in subject.lower():

        # QUIZ GENERATOR

        if "quiz generator" in instruction_text:

            content = """
## Python Functions — Practice Quiz

**1. Which keyword is used to define a function in Python?**

A. function
B. def
C. create
D. fun

**Answer: B — def**

**2. What is a function?**

A. A reusable block of code
B. A variable
C. A loop
D. A data type

**Answer: A — A reusable block of code**

**3. Which symbol is used after a function name?**

A. ;
B. ,
C. ()
D. []

**Answer: C — ()**

**4. What does `return` do?**

A. Stops the computer
B. Sends a result back from a function
C. Creates a loop
D. Prints a variable

**Answer: B — Sends a result back**

**5. What is a parameter?**

A. An input variable in a function definition
B. A Python error
C. A comment
D. A loop condition

**Answer: A — An input variable**

**6. What is the output of this code?**

```python
def add(a, b):
    return a + b

print(add(5, 3))
```

A. 53
B. 8
C. 5
D. Error

**Answer: B — 8**

**7. Which function displays output?**

A. input()
B. print()
C. return()
D. def()

**Answer: B — print()**

**8. Can a function be called multiple times?**

A. Yes
B. No
C. Only twice
D. Only once

**Answer: A — Yes**

**9. What happens if a function has no return statement?**

A. It returns None by default
B. It always gives an error
C. It returns zero
D. It stops Python

**Answer: A — It returns None**

**10. Which is the correct function call?**

A. call greet
B. greet[]
C. greet()
D. def greet

**Answer: C — greet()**
"""

        # NOTES GENERATOR

        elif "notes generator" in instruction_text:

            content = """
## 1. Introduction

A function is a reusable block of Python code
that performs a particular task.

## 2. Important Definitions

- **Function:** A reusable block of code.
- **Parameter:** A variable written in a function definition.
- **Argument:** The actual value passed when calling a function.
- **Return:** Sends a result back from a function.

## 3. Syntax

```python
def function_name():
    # code
    pass
```

## 4. Example

```python
def greet():
    print("Hello, Student!")

greet()
```

Output:

```text
Hello, Student!
```

## 5. Function With Parameters

```python
def add(a, b):
    return a + b

result = add(10, 20)
print(result)
```

Output: `30`

## 6. Advantages

- Reuses code.
- Makes programs organized.
- Reduces repeated code.
- Makes debugging easier.

## 7. Quick Revision

- `def` defines a function.
- `()` is used for parameters and function calls.
- `return` sends a result back.
- A function runs when it is called.
"""

        # EXPLAIN TOPIC

        else:

            content = """
## 1. Introduction

Python functions allow you to write reusable
blocks of code.

## 2. Simple Explanation

Imagine you have to perform the same calculation
many times.

Instead of writing the same code repeatedly,
you can create a function and call it whenever needed.

## 3. Creating a Function

```python
def greet():
    print("Hello, Student!")

greet()
```

Output:

```text
Hello, Student!
```

## 4. Function With Inputs

```python
def add(a, b):
    return a + b

print(add(10, 20))
```

Output: `30`

Here:

- `def` creates the function.
- `a` and `b` are parameters.
- `return` sends back the answer.
- `add(10, 20)` calls the function.

## 5. Real-Life Example

A calculator has different operations.

You can create separate functions for addition,
subtraction, multiplication and division.

## 6. Summary

Functions make Python programs reusable,
organized and easier to maintain.
"""

    # -----------------------------------------
    # OTHER TOPICS
    # -----------------------------------------

    else:

        content = f"""
## Introduction

This is a basic demonstration for **{topic}**.

## What to Learn

- Understand the meaning of {topic}.
- Learn its important concepts.
- Study examples related to {subject}.
- Practice writing small programs.

## Practice

Try finding one real-world example of {topic}.

## Summary

This is a general mock template.
Topic-specific explanations are currently available
for Python Functions.
"""

    return heading + details + content


# -----------------------------------------
# 3. GENERATE RESPONSE
# -----------------------------------------

def generate_response(instructions, prompt):

    mode = os.getenv("STUDYMATE_MODE", "mock").strip().lower()

    # FREE MOCK MODE

    if mode == "mock":

        return generate_mock_response(
            instructions,
            prompt
        )

    # LIVE AI MODE

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
            "Choose mock or live mode in .env"
        )
