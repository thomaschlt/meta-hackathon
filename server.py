from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

from ranking import ranking_service

app = FastAPI()

example_to_classify_content = [
    {"tldr": "Ethical implications of machine learning", "content_id": 10},
    {"tldr": "Latest Hollywood drama", "content_id": 11},
    {"tldr": "Technological research innovations", "content_id": 12},
]
example_classified_content = [
    {"tldr": "AI ethics in technology", "passed": True},
    {"tldr": "Celebrity gossip", "passed": False},
]


class QueryInput(BaseModel):
    text: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/content")
def get_content():
    return example_to_classify_content


@app.get("/classify_content")
def classify_content():
    return ranking_service.classify_content(
        example_to_classify_content, example_classified_content
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
