from pipeline.database import get_db_session
from pipeline.models import Package
from pipeline.transformer import Transformer
from pipeline.loader import Loader
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_single_record():
    # Get a single record from database
    db_session_gen = get_db_session()
    db = next(db_session_gen)
    
    try:
        # Get one record
        record = db.query(Package).first()
        if record:
            print(f"Processing record ID: {record.id}")
            print(f"Record text: {record.to_text()[:200]}...")
            
            # Test the transformer
            print("\nTesting transformer...")
            transformer = Transformer()
            transformed_data = transformer.generate_embeddings([record])
            
            print(f"Generated embedding with {len(transformed_data[0]['embedding'])} dimensions")
            
            # Test saving to Pinecone
            print("\nTesting Pinecone loader...")
            loader = Loader()
            loader.upsert_data(transformed_data)
            
            print("Successfully processed and stored the record!")
        else:
            print("No records found in the database")
            
    except Exception as e:
        print(f"Error in test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_single_record()