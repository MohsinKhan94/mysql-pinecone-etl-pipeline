from pipeline.database import get_db_session
from pipeline.models import Package
from sqlalchemy.orm import selectinload

def test_enhanced_record():
    # Get database session
    db_session_gen = get_db_session()
    db = next(db_session_gen)
    
    try:
        # Get record with all related data loaded
        record = db.query(Package).options(
            selectinload(Package.moods),
            selectinload(Package.sub_moods),
            selectinload(Package.destinations),
            selectinload(Package.days),
            selectinload(Package.months),
            selectinload(Package.years),
            selectinload(Package.types),
            selectinload(Package.tour_plans),
            selectinload(Package.prices),
            selectinload(Package.meals),
            selectinload(Package.transportations),
            selectinload(Package.transport_upgrades)
        ).first()
        
        if record:
            print(f"Processing record ID: {record.id}")
            print(f"Package Name: {record.name}")
            print("\nEnhanced text for embedding:")
            print("="*50)
            enhanced_text = record.to_text()
            print(enhanced_text)
            print("="*50)
            
            print(f"\nTotal length of text: {len(enhanced_text)} characters")
            
            # Show related data counts
            print(f"\nRelated data counts:")
            print(f"- Moods: {len(record.moods)}")
            print(f"- Sub-moods: {len(record.sub_moods)}")
            print(f"- Destinations: {len(record.destinations)}")
            print(f"- Days: {len(record.days)}")
            print(f"- Months: {len(record.months)}")
            print(f"- Years: {len(record.years)}")
            print(f"- Types: {len(record.types)}")
            print(f"- Tour Plans: {len(record.tour_plans)}")
            print(f"- Prices: {len(record.prices)}")
            print(f"- Meals: {len(record.meals)}")
            print(f"- Transportations: {len(record.transportations)}")
            print(f"- Transport Upgrades: {len(record.transport_upgrades)}")
        else:
            print("No records found in the database")
            
    except Exception as e:
        print(f"Error in test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_enhanced_record()