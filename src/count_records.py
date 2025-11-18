from pipeline.database import get_db_session
from pipeline.models import Package

def count_all_records():
    # Get database session
    db_session_gen = get_db_session()
    db = next(db_session_gen)
    
    try:
        # Count all records
        total_count = db.query(Package).count()
        print(f"Total records in packages table: {total_count}")
        
        # Show all records
        records = db.query(Package).all()
        print("\nAll records in the database:")
        for record in records:
            text_preview = record.to_text()[:100] + "..." if len(record.to_text()) > 100 else record.to_text()
            print(f"ID: {record.id}, Text preview: {text_preview}")
        
    except Exception as e:
        print(f"Error counting records: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    count_all_records()