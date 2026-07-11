import json
import pandas as pd

from engine.company_loader import CompanyLoader
from engine.prompt_builder import PromptBuilder
from engine.generator import Generator
from engine.validator import Validator
from engine.exporter import Exporter


MAX_ATTEMPTS = 5
QUESTIONS_PER_TOPIC = 1

# Change only this line
COMPANY = "Google"


def get_existing_count(exporter, section_name, topic):

    section = section_name.lower()

    if "quantitative" in section:
        filename = "quantitative.csv"

    elif "logical" in section:
        filename = "logical.csv"

    elif "verbal" in section:
        filename = "verbal.csv"

    else:
        return 0

    file = f"{exporter.output_root}/{filename}"

    try:
        df = pd.read_csv(file)

        return len(
            df[df["Topic"] == topic]
        )

    except:
        return 0


def generate_section(
    section_name,
    topics,
    builder,
    generator,
    validator,
    exporter,
):

    print("\n" + "=" * 100)
    print(f"SECTION : {section_name}")
    print("=" * 100)

    total_saved = 0

    for _, row in topics.iterrows():

        topic = row["topic"]
        difficulty = row["difficulty"]

        print("\n" + "-" * 80)
        print(f"TOPIC : {topic}")
        print(f"DIFFICULTY : {difficulty}")
        print("-" * 80)

        saved = get_existing_count(
            exporter,
            section_name,
            topic
        )

        if saved >= QUESTIONS_PER_TOPIC:

            print(
                f"✅ {topic} already has "
                f"{saved} questions. Skipping..."
            )

            total_saved += saved
            continue

        while saved < QUESTIONS_PER_TOPIC:

            print(
                f"\nGenerating Question "
                f"{saved + 1}/{QUESTIONS_PER_TOPIC}"
            )

            accepted = False
            attempt = 1

            while (
                not accepted and
                attempt <= MAX_ATTEMPTS
            ):

                print(f"Attempt : {attempt}")

                prompt = builder.build_prompt(
                    section=section_name,
                    topic=topic,
                    difficulty=difficulty
                )

                try:

                    response = generator.generate(prompt)

                    clean_response = (
                        response.replace("```json", "")
                        .replace("```", "")
                        .strip()
                    )

                    question = json.loads(
                        clean_response
                    )

                except Exception as e:

                    print("❌ Invalid JSON")
                    print(e)

                    attempt += 1
                    continue

                valid, errors = (
                    validator.validate(question)
                )

                print(
                    "\n========== VALIDATION =========="
                )

                if valid:
                    print("✅ Validation Passed")
                else:
                    print("❌ Validation Failed")
                    print(errors)

                accepted = valid

                if accepted:

                    exporter.save(question)

                    saved += 1
                    total_saved += 1

                    print(
                        f"✅ Saved "
                        f"({saved}/{QUESTIONS_PER_TOPIC})"
                    )

                else:
                    print("❌ Rejected")

                attempt += 1

            if not accepted:
                print(f"⚠ Skipping {topic}")
                break

    return total_saved


def main():

    print(
        "\n========== CODEHIRING AI DATASET ENGINE ==========\n"
    )

    print(f"COMPANY : {COMPANY}\n")

    loader = CompanyLoader(
        f"knowledge/{COMPANY}"
    )

    data = loader.load_all()

    print(
        "✅ Company Loaded Successfully\n"
    )

    builder = PromptBuilder(
        data["profile"],
        data["pattern"]
    )

    generator = Generator()
    validator = Validator()
    exporter = Exporter(COMPANY)

    grand_total = 0

    grand_total += generate_section(
        "Quantitative Aptitude",
        data["aptitude"],
        builder,
        generator,
        validator,
        exporter
    )

    grand_total += generate_section(
        "Logical Reasoning",
        data["logical"],
        builder,
        generator,
        validator,
        exporter
    )

    grand_total += generate_section(
        "Verbal Ability",
        data["verbal"],
        builder,
        generator,
        validator,
        exporter
    )

    print("\n========================================")
    print("DATASET GENERATION COMPLETED")
    print(f"COMPANY : {COMPANY}")
    print(f"TOTAL QUESTIONS : {grand_total}")
    print("========================================")


if __name__ == "__main__":
    main()  