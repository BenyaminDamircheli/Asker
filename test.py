from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def chat_with_openai():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        messages=[{"role": "system", "content": "You are a helpful assistant."}],
        model="gpt-3.5-turbo"
    )

    print(response.choices[0].message.content)

chat_with_openai()
