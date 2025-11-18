import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pipeline.database import SessionLocal
from pipeline import models

def test_connection():
    print("Testing database connection and counting records...")
    
    db = SessionLocal()
    try:
        # Count all records in the packages table
        record_count = db.query(models.Package).count()
        print(f"Total records in packages table: {record_count}")
        
        # Try to fetch first few records to see if they exist
        records = db.query(models.Package).limit(5).all()
        print(f"Number of records fetched: {len(records)}")
        
        if records:
            print("\nFirst record details:")
            first_record = records[0]
            print(f"ID: {first_record.id}")
            print(f"Name: {first_record.name}")
            print(f"Details: {first_record.tourDetail}")
        else:
            print("No records found in the packages table")
            
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()