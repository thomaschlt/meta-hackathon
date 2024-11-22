from fastapi import Path
from openai import OpenAI

from contants import OPENAI_API_KEY

json_schema = {
    "name": "Content ranker",
    "schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["content_rankings"],
    "properties": {
        "content_rankings": {
            "type": "object",
            "additionalProperties": {"type": "integer", "minimum": 1},
            "minProperties": 1,
            "propertyNames": {"anyOf": [{"type": "integer"}, {"type": "integer"}]},
        }
    },
    "additionalProperties": False,
}


def classify_content(
    to_classify_content: list[dict[str, str | int]],
    classified_content: list[dict[str, str | bool]],
):
    """
    Classify content based on a list of content to classify and a list of classified content.

    Args:
    - to_classify_content (list[dict[str, str | int]]): List of content to classify.
    - classified_content (list[dict[str, str | bool]]): List of classified content.

    Returns:
    - list[dict[str, str | bool]]: List of classified content.
    """
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

    system_prompt = Path("system_prompt.md").read_text()

    def prompt_for_classification(to_classify_content, classified_content) -> str:
        return f"Please classify this content. The content to classify is {to_classify_content}. The classified content is: {classified_content}."

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": prompt_for_classification(
                    to_classify_content, classified_content
                ),
            },
        ],
        response_format={"type": "json_schema", "schema": json_schema},
    )
    classified_results = response.choices[0].message.content

    return classified_results
