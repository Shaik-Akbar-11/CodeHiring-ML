import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class Generator:

    def generate(self, prompt: str):

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert placement assessment generator. "
                        "Always follow the user's instructions exactly. "
                        "Return ONLY valid JSON when JSON is requested. "
                        "Never use markdown. "
                        "Never wrap JSON inside ```json."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2,
            top_p=0.9,
            max_completion_tokens=1200
        )

        return response.choices[0].message.content