import logging
from pinecone import Pinecone, ServerlessSpec
from .config import PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME, BATCH_SIZE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Loader:
    """
    A class to handle loading data into a Pinecone index.
    """
    def __init__(self):
        """
        Initializes the Loader by connecting to Pinecone.
        """
        if not PINECONE_API_KEY or not PINECONE_ENVIRONMENT:
            raise ValueError("PINECONE_API_KEY and PINECONE_ENVIRONMENT must be set.")
            
        logger.info("Initializing Pinecone connection...")
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        
        self.index_name = PINECONE_INDEX_NAME
        self.index = self._get_or_create_index()

    def _get_or_create_index(self):
        """
        Gets the Pinecone index, creating it if it doesn't exist.
        """
        if self.index_name not in self.pc.list_indexes().names():
            logger.info(f"Index '{self.index_name}' not found. Creating it...")
            # Note: The dimension must match the output of the embedding model.
            # 'all-roberta-large-v1' has a dimension of 1024.
            self.pc.create_index(
                name=self.index_name,
                dimension=1024,
                metric='cosine',
                spec=ServerlessSpec(cloud='aws', region=PINECONE_ENVIRONMENT)
            )
            logger.info(f"Index '{self.index_name}' created successfully.")
        else:
            logger.info(f"Found existing index '{self.index_name}'.")
            
        return self.pc.Index(self.index_name)

    def upsert_data(self, transformed_data: list[dict]):
        """
        Upserts a batch of transformed data into the Pinecone index.

        Args:
            transformed_data: A list of dictionaries, where each dictionary contains
                              the id, embedding, and metadata.
        """
        if not transformed_data:
            return

        logger.info(f"Upserting {len(transformed_data)} records to Pinecone.")
        
        # Format data for Pinecone upsert
        vectors_to_upsert = []
        for item in transformed_data:
            vectors_to_upsert.append({
                "id": item["id"],
                "values": item["embedding"],
                "metadata": {"model_version": item["model_version"]}
            })

        # Upsert in batches
        for i in range(0, len(vectors_to_upsert), BATCH_SIZE):
            batch = vectors_to_upsert[i:i + BATCH_SIZE]
            try:
                self.index.upsert(vectors=batch)
                logger.info(f"Successfully upserted batch of {len(batch)} records.")
            except Exception as e:
                logger.error(f"Failed to upsert batch: {e}")
                # Optionally, add more robust error handling here (e.g., retries)

        logger.info("Upsert operation completed.")
