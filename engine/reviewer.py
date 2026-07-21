import json
from engine.generator import Generator


class Reviewer:

    def __init__(self):
        self.generator = Generator()

    def review(self, question_json: str):

        prompt = f"""
You are a Senior Assessment Reviewer.

Review the following assessment question.

Verify ALL of the following:

1. Mathematics is correct.
2. Correct answer is correct.
3. Explanation matches the answer.
4. Topic matches the question.
5. Difficulty matches the question.
6. Company style is realistic.
7. Grammar is correct.
8. Exactly one option is correct.
9. Question is original.
10. JSON structure is valid.

Reject the question if ANY check fails.

Return ONLY ONE valid JSON object.

Return exactly this format:

{{
    "accepted": true,
    "overall_score": 96,
    "checks": {{
        "company_match": true,
        "topic_match": true,
        "difficulty_match": true,
        "mathematics_correct": true,
        "answer_correct": true,
        "explanation_correct": true,
        "grammar_correct": true,
        "single_correct_answer": true,
        "original": true
    }},
    "errors": []
}}

Question:

{question_json}
"""

        response = self.generator.generate(prompt)

        response = (
            response.replace("```json", "")
                    .replace("```", "")
                    .strip()
        )

        try:

            result = json.loads(response)

            if "accepted" not in result:
                raise ValueError()

            return result

        except Exception:

            return {
                "accepted": False,
                "overall_score": 0,
                "checks": {
                    "company_match": False,
                    "topic_match": False,
                    "difficulty_match": False,
                    "mathematics_correct": False,
                    "answer_correct": False,
                    "explanation_correct": False,
                    "grammar_correct": False,
                    "single_correct_answer": False,
                    "original": False
                },
                "errors": [
                    "Reviewer returned invalid JSON."
                ]
            }