import logging
from sentence_transformers import SentenceTransformer
from . import models
from .config import EMBEDDING_MODEL_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Transformer:
    """
    A class to handle the transformation of text data into embeddings.
    """
    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME):
        """
        Initializes the Transformer by loading the sentence-transformer model.
        """
        logger.info(f"Loading embedding model: {model_name}")
        try:
            self.model = SentenceTransformer(model_name)
            logger.info("Embedding model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise

    def generate_embeddings(self, records: list[models.Package]) -> list[dict]:
        """
        Generates embeddings for a list of Package records.

        Args:
            records: A list of Package objects.

        Returns:
            A list of dictionaries, where each dictionary contains the record id,
            the generated embedding, and the model version.
        """
        if not records:
            return []

        logger.info(f"Generating embeddings for {len(records)} records.")
        
        # Get the text to be embedded from each record
        texts_to_embed = [record.to_text() for record in records]
        
        # Generate embeddings
        embeddings = self.model.encode(texts_to_embed, show_progress_bar=True)
        
        # Prepare the data for the loader
        transformed_data = []
        for i, record in enumerate(records):
            transformed_data.append({
                "id": str(record.id),
                "embedding": embeddings[i].tolist(),
                "model_version": EMBEDDING_MODEL_NAME
            })
            
        logger.info("Embeddings generated successfully.")
        return transformed_data
