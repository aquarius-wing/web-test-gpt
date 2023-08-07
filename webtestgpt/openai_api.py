import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def ask_openai(prompt: str, model="gpt-4-0613"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000,
        temperature=0
    )
    try:
        content = response['choices'][0]['message']['content']
        return content
    except Exception as e:
        print(e)
