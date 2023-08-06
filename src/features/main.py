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
    text_without_stop_words = functions.remove_stop_words(nlp_model, text)
    similarities = functions.get_similarity(embed_model, embeddings, text_without_stop_words)

    response = faq.copy()
    response["Similarity"] = similarities.values

    return response
    