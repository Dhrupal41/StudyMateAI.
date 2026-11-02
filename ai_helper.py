import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def generate_response(instruction, prompt):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "YOUR_OPENAI_API_KEY":
        raise ValueError("API key not found.Please check yout .env file.")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-5.5",
        instructions=instruction,
        inputs=prompt,
    )
    return response.output_text