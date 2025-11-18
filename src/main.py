import logging
import time
from datetime import datetime, timedelta
from pipeline import database, extractor, transformer, loader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_last_run_timestamp(filepath="last_run.txt"):
    """Reads the timestamp of the last successful run."""
    try:
        with open(filepath, "r") as f:
            return datetime.fromisoformat(f.read().strip())
    except FileNotFoundError:
        # If the file doesn't exist, process records from the last 24 hours.
        return datetime.utcnow() - timedelta(days=1)

def set_last_run_timestamp(filepath="last_run.txt"):
    """Saves the timestamp of the current successful run."""
    with open(filepath, "w") as f:
        f.write(datetime.utcnow().isoformat())

def run_pipeline():
    """
    Executes the full ETL pipeline.
    """
    logger.info("Starting ETL pipeline run...")
    start_time = time.time()

    last_run_ts = get_last_run_timestamp()
    
    # Initialize components
    db_session_gen = database.get_db_session()
    db = next(db_session_gen)
    
    try:
        # Initialize transformer and loader
        embedding_transformer = transformer.Transformer()
        pinecone_loader = loader.Loader()

        while True:
            # 1. Extract
            records = extractor.get_records_to_update(db, last_run_ts, loader.BATCH_SIZE)
            if not records:
                logger.info("No new records to process. Pipeline run finished.")
                break

            # 2. Transform
            transformed_data = embedding_transformer.generate_embeddings(records)

            # 3. Load
            pinecone_loader.upsert_data(transformed_data)
            
            # Optional: Update a status field in the database for the processed records
            # This would require adding a 'status' field to the Package model
            # and updating it here.

    except Exception as e:
        logger.error(f"An error occurred during the pipeline run: {e}")
    finally:
        db.close()

    set_last_run_timestamp()
    end_time = time.time()
    logger.info(f"Pipeline run completed in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    run_pipeline()
