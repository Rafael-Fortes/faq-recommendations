from sentence_transformers import SentenceTransformer
import pandas as pd

class SemanticEngine:
    def __init__(self, model_name: str):
        try:
            self.model = SentenceTransformer(model_name)
        except Exception as e:
            print(e)
            raise e

    def embed_text(self, text: str) -> list[float]:
        try:
            return self.model.encode(text).tolist()
        except Exception as e:
            print(e)
            raise e

    def embed_dataframe_column(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        try:
            df["embedding"] = df[column].apply(self.embed_text)
            return df
        except Exception as e:
            print(e)
            raise e
