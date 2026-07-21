class PromptBuilder:

    def __init__(self, profile, pattern):

        self.profile = profile
        self.pattern = pattern

    def _map_difficulty(self, difficulty):

        if difficulty in self.pattern["difficulty"]:
            return difficulty

        mapping = {
            "Easy-Medium": "Medium",
            "Medium-Hard": "Hard",
            "Easy-Hard": "Hard",
            "Very Easy": "Easy",
            "Very Hard": "Hard"
        }

        return mapping.get(
            difficulty,
            "Medium"
        )

    def build_prompt(
        self,
        section,
        topic,
        difficulty
    ):

        company = self.profile["company"]
        role = self.profile["role"]

        question_style = self.pattern["question_style"]
        language = self.pattern["language"]
        real_world = self.pattern["real_world_context"]
        reasoning = self.pattern["multi_step_reasoning"]
        calculator = self.pattern["calculator_allowed"]

        difficulty_key = self._map_difficulty(
            difficulty
        )

        diff = self.pattern["difficulty"][
            difficulty_key
        ]

        steps = diff["steps"]
        time = diff["time"]

        rules = "\n".join(
            f"- {rule}"
            for rule in self.pattern["rules"]
        )

        prompt = f"""
You are a Senior Assessment Architect.

Your job is to generate ONE HIGH QUALITY assessment question.

The question must be indistinguishable from an actual Online Assessment conducted by {company}.

==================================================
COMPANY INFORMATION
==================================================

Company : {company}

Role : {role}

Section : {section}

Topic : {topic}

Difficulty : {difficulty}

==================================================
QUESTION STYLE
==================================================

Question Style : {question_style}

Language : {language}

Real World Context : {real_world}

Multi Step Reasoning : {reasoning}

Calculator Allowed : {calculator}

Expected Reasoning Steps : {steps}

Expected Solving Time : {time}

==================================================
STRICT RULES
==================================================

{rules}

==================================================
QUESTION REQUIREMENTS
==================================================

The question must

• be original

• never copy questions from internet

• never copy LeetCode

• never copy previous Amazon OA questions

• use realistic values

• contain exactly ONE correct answer

• contain FOUR options

• explanation must perfectly match the answer

• mathematics must be correct

• grammar must be correct

• topic must exactly match

• difficulty must exactly match

• resemble an actual company assessment

• not contain ambiguity

• not require external assumptions

• be suitable for fresh graduates

==================================================
QUALITY CHECK
==================================================

Before returning your answer verify internally

1 Mathematics correct

2 Answer correct

3 Explanation correct

4 Grammar correct

5 JSON valid

6 Topic correct

7 Difficulty correct

8 Only one option correct

9 Original question

10 Company style matched

If any check fails,

generate another question.

==================================================
OUTPUT FORMAT
==================================================

Return ONLY ONE valid JSON object.

Do not return markdown.

Do not use ```json.

Do not explain anything.

Return ONLY JSON.

The JSON must be parseable using Python json.loads().

Return EXACTLY

{{
    "company":"{company}",
    "role":"{role}",
    "section":"{section}",
    "topic":"{topic}",
    "difficulty":"{difficulty}",
    "question":"",
    "options":
    {{
        "A":"",
        "B":"",
        "C":"",
        "D":""
    }},
    "answer":"A",
    "explanation":""
}}

Return nothing except JSON.
"""

        return prompt.strip()