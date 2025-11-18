from pipeline.database import get_db_session
from pipeline.models import Package
from sqlalchemy import text

def get_all_packages_raw():
    # Get database session
    db_session_gen = get_db_session()
    db = next(db_session_gen)
    
    try:
        # Execute raw SQL to see all records
        result = db.execute(text("SELECT * FROM packages"))
        columns = result.keys()
        rows = result.fetchall()
        
        print(f"Total records found: {len(rows)}")
        print(f"Columns: {list(columns)}")
        print("\nAll records:")
        for i, row in enumerate(rows):
            print(f"Row {i+1}: {dict(zip(columns, row))}")
        
        print("\n" + "="*50)
        print("Checking with SQLAlchemy model:")
        
        # Get all records using SQLAlchemy model
        records = db.query(Package).all()
        print(f"Records via SQLAlchemy: {len(records)}")
        for record in records:
            print(f"ID: {record.id}, Name: {record.name}")
        
    except Exception as e:
        print(f"Error getting records: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    get_all_packages_raw()