from sentence_transformers import SentenceTransformer
import pandas as pd
from app.utils.logger import Logger

class SemanticEngine:
    def __init__(self, model_name: str):
        try:
            Logger.info(f"Initializing SemanticEngine with model: {model_name}")
            self.model = SentenceTransformer(model_name)

            Logger.info(f"Getting vector size of model: {model_name}")
            self.vector_size = self.model.encode("Hello, World!").shape[0]
            Logger.info(f"Vector size of model: {model_name} is {self.vector_size}")

            Logger.info(f"SemanticEngine initialized successfully with model: {model_name}")
        except Exception as e:
            Logger.error(f"Error initializing SemanticEngine with model {model_name}: {str(e)}")
            raise e

    def embed_text(self, text: str) -> list[float]:
        try:
            Logger.debug(f"Embedding text: {text[:50]}..." if len(text) > 50 else f"Embedding text: {text}")
            result = self.model.encode(text).tolist()
            Logger.debug("Text embedding completed successfully")
            return result
        except Exception as e:
            Logger.error(f"Error embedding text: {str(e)}")
            raise e

    def embed_dataframe_column(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        try:
            Logger.info(f"Embedding dataframe column: {column} with {len(df)} rows")
            df["embedding"] = df[column].apply(self.embed_text)
            Logger.info(f"Successfully embedded {len(df)} rows in column: {column}")
            return df
        except Exception as e:
            Logger.error(f"Error embedding dataframe column {column}: {str(e)}")
            raise e
