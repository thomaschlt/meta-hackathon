from fastapi import FastAPI, HTTPException
import uvicorn
import torch
from executorch import load_model
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


# Initialisation globale du modèle
MODEL_PATH = "path/to/your/llm.pte"
llm_model = None

try:
    llm_model = load_executorch_model(MODEL_PATH)
    print("Modèle LLM chargé avec succès")
except Exception as e:
    print(f"Erreur de chargement du modèle: {e}")


@app.get("/")
def read_root():
    return {"Hello": "World"}


# Charger et optimiser le modèle (à adapter selon votre modèle)
def load_executorch_model(path_model: str):
    model = load_model(path_model)
    return model


@app.get("/get_content")
def get_content():
    return example_to_classify_content


@app.get("/classify_content")
def classify_content(to_classify_content, classified_content):
    return ranking_service.classify_content(
        example_to_classify_content, example_classified_content
    )


@app.post("/generate")
async def generate_text(query: QueryInput):
    if llm_model is None:
        raise HTTPException(status_code=500, detail="Modèle LLM non initialisé")

    try:
        # Adapter le traitement selon votre modèle spécifique
        input_text = query.text
        # Convertir le texte en tenseurs selon les besoins de votre modèle
        with torch.no_grad():
            output = llm_model(input_text)
            return {"generated_text": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'inférence: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
