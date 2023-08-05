import pandas as pd
import numpy as np
import torch
import spacy
from sentence_transformers import SentenceTransformer, util


def get_similarity(model, embeddings, text):
    text_embed = model.encode(text)
    similarities = []

    for column in embeddings.columns:
        similarity = util.cos_sim(text_embed, embeddings[column].values.astype(np.float32))
        similarities.append(similarity)
    

    return pd.Series(similarities).astype(float)


def remove_stop_words(model, text:str):
    text_tokens = model(text)

    words_without_stopwords = []

    for token in text_tokens:
        if not token.is_stop:
            words_without_stopwords.append(token.text)
    
    text_without_stopwords = " ".join(words_without_stopwords)

    return text_without_stopwords
