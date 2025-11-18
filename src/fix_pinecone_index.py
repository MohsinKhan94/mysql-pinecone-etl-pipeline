import logging
from pinecone import Pinecone
from pipeline.config import PINECONE_API_KEY, PINECONE_INDEX_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_pinecone_index():
    """
    Fixes the Pinecone index by deleting the existing one with wrong dimension
    and letting the pipeline recreate it with the correct dimension.
    """
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY must be set.")

    logger.info("Initializing Pinecone connection...")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    index_name = PINECONE_INDEX_NAME
    
    if index_name in pc.list_indexes().names():
        logger.info(f"Deleting existing index '{index_name}' with potentially wrong dimension...")
        pc.delete_index(index_name)
        logger.info(f"Index '{index_name}' deleted successfully.")
    else:
        logger.info(f"Index '{index_name}' does not exist, it will be created with correct dimension on next pipeline run.")
    
if __name__ == "__main__":
    fix_pinecone_index()