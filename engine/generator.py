import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class Generator:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found.")

        self.client = Groq(api_key=api_key)

        self.model = "llama-3.3-70b-versatile"

    def generate(self, prompt: str):

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a Senior Placement Assessment Architect.\n"
                        "Generate professional company assessment questions.\n"
                        "Always follow every instruction exactly.\n"
                        "Return ONLY ONE valid JSON object.\n"
                        "Never use markdown.\n"
                        "Never wrap the output inside ```json.\n"
                        "Never explain anything.\n"
                        "Every string must be valid JSON.\n"
                        "The response must be parseable using Python json.loads()."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3,
            top_p=0.9,
            max_completion_tokens=1200
        )

        return response.choices[0].message.content.strip()