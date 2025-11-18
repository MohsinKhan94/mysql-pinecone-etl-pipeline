from pipeline import extractor
from pipeline.database import get_db_session
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_records():
    # Get database session
    db_session_gen = get_db_session()
    db = next(db_session_gen)
    
    try:
        # Get records from the last 24 hours (or since last run)
        last_run_ts = datetime.utcnow() - timedelta(days=1)
        records = extractor.get_records_to_update(db, last_run_ts, 10)
        
        print(f'Found {len(records)} records to process since {last_run_ts}')
        
        if records:
            print("\nFirst few records:")
            for i, record in enumerate(records[:3]):
                text_preview = record.to_text()[:100] + "..." if len(record.to_text()) > 100 else record.to_text()
                print(f'Record {i+1}: ID: {record.id}, Text preview: {text_preview}')
        else:
            print("No records to process - might explain why the pipeline appears to be stuck")
        
        return len(records)
        
    except Exception as e:
        print(f"Error checking records: {e}")
        return 0
    finally:
        db.close()

if __name__ == "__main__":
    check_records()