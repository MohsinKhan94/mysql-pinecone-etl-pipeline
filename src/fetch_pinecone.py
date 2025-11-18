import logging
from pipeline.loader import Loader
from pipeline.config import PINECONE_INDEX_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_from_pinecone():
    """
    Fetches records from Pinecone and stores details in result.txt.
    """
    logger.info("Initializing Pinecone connection...")
    
    # Initialize the loader (which connects to Pinecone)
    loader = Loader()
    
    # Get the index
    index = loader.index
    
    # Fetch all IDs from the index (using a simple query approach)
    # For this test, we'll try to fetch records by ID if we know them
    # Otherwise, we'll demonstrate how to query with a vector
    
    logger.info(f"Fetching index stats for '{PINECONE_INDEX_NAME}'...")
    stats = index.describe_index_stats()
    print(f"Index stats: {stats}")
    
    # Try to fetch up to 10 records using the list method if available
    # Since Pinecone doesn't have a direct "list all vectors" method, 
    # we'll try to query with a random vector and see what we get
    import numpy as np
    from sentence_transformers import SentenceTransformer
    
    # Use the same model to generate a test embedding
    model = SentenceTransformer('sentence-transformers/all-roberta-large-v1')
    
    # Generate a simple query vector
    query_text = "tour package"
    query_embedding = model.encode([query_text]).tolist()[0]
    
    logger.info("Performing similarity search in Pinecone...")
    try:
        # Query Pinecone for similar vectors
        results = index.query(
            vector=query_embedding,
            top_k=10,  # Get up to 10 most similar records
            include_values=False,  # Don't include the full embedding values to save space
            include_metadata=True  # Include the metadata we stored
        )
        
        logger.info(f"Found {len(results['matches'])} results from Pinecone")
        
        # Write results to file
        with open('result.txt', 'w', encoding='utf-8') as f:
            f.write("Results from Pinecone Query\n")
            f.write("=" * 50 + "\n\n")
            
            for i, match in enumerate(results['matches']):
                f.write(f"Result {i+1}:\n")
                f.write(f"  ID: {match['id']}\n")
                f.write(f"  Score (similarity): {match['score']:.4f}\n")
                f.write(f"  Metadata: {match['metadata']}\n")
                f.write("-" * 30 + "\n")
                
                # Print to console as well
                print(f"Result {i+1}:")
                print(f"  ID: {match['id']}")
                print(f"  Score (similarity): {match['score']:.4f}")
                print(f"  Metadata: {match['metadata']}")
                print("-" * 30)
        
        logger.info("Results written to result.txt")
        
    except Exception as e:
        logger.error(f"Error querying Pinecone: {e}")
        import traceback
        traceback.print_exc()
        
        # Write error to result file
        with open('result.txt', 'w', encoding='utf-8') as f:
            f.write("Error occurred while querying Pinecone\n")
            f.write("=" * 50 + "\n")
            f.write(f"Error: {e}\n")
            f.write("Traceback:\n")
            f.write(traceback.format_exc())

if __name__ == "__main__":
    fetch_from_pinecone()