from fastapi import FastAPI

import pandas as pd
import numpy as np
import spacy
from sentence_transformers import SentenceTransformer, util

import functions


embeddings = pd.read_csv("../data/Embeddings.csv", sep=";")
faq = pd.read_csv("../data/FAQ_example.csv", sep=";")

embed_model = SentenceTransformer("../models/embed_model")
nlp_model = spacy.load("../models/nlp_model")

app = FastAPI()


@app.get("/")
def home():
    return {"Status": "ok"}


@app.get("/get_similarities/{text}")
def get_similarities(text: str):
    if text:
        text_preprocessed = functions.get_clean_text(nlp_model, text)
        similarities = functions.get_similarity(embed_model, embeddings, text_preprocessed)

        response = faq.copy()
        response["Similarity"] = similarities.values
        response.sort_values(by="Similarity", ascending=False, inplace=True)
        response.index = [i for i in range(response.shape[0])]

        return response
    