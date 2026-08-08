from typing import List, Optional

from sentence_transformers import SentenceTransformer

from app.core.config import settings



class EmbeddingService:


    def __init__(self):

        self.model_name = (
            settings.EMBEDDING_MODEL_NAME
        )

        self.dimension = (
            settings.EMBEDDING_DIMENSION
        )


        self.model = SentenceTransformer(
            self.model_name
        )



    def generate_embedding(
        self,
        text: str
    ) -> Optional[List[float]]:

        """
        Generate vector embedding
        """

        if not text:

            return None


        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )


        vector = embedding.tolist()


        if len(vector) != self.dimension:

            raise ValueError(
                f"Embedding dimension mismatch. "
                f"Expected {self.dimension}, "
                f"Got {len(vector)}"
            )


        return vector



embedding_service = EmbeddingService()