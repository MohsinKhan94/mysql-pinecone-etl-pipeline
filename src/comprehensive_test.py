from pipeline.database import get_db_session
from pipeline.models import Package, PackageMood, SubMood, Destination, PkgDay, PkgMonth, PkgYear, PkgType, TourPlan, NumberTravelerPrice, MealSummary, Transportation, TransportationUpgrade
from sqlalchemy.orm import selectinload

def test_all_related_data():
    # Get database session
    db_session_gen = get_db_session()
    db = next(db_session_gen)
    
    try:
        # Test each related table individually to see what data exists
        print("Checking each table individually:")
        
        # Check packages table
        package_count = db.query(Package).count()
        print(f"Packages table: {package_count} records")
        
        # Check each related table for records connected to package ID 1
        related_tables = [
            ("PackageMood", PackageMood),
            ("SubMood", SubMood),
            ("Destination", Destination),
            ("PkgDay", PkgDay),
            ("PkgMonth", PkgMonth),
            ("PkgYear", PkgYear),
            ("PkgType", PkgType),
            ("TourPlan", TourPlan),
            ("NumberTravelerPrice", NumberTravelerPrice),
            ("MealSummary", MealSummary),
            ("Transportation", Transportation),
            ("TransportationUpgrade", TransportationUpgrade)
        ]
        
        for table_name, model in related_tables:
            count = db.query(model).filter(model.package_id == 1).count()
            print(f"{table_name}: {count} records for package_id=1")
            if count > 0:
                records = db.query(model).filter(model.package_id == 1).all()
                print(f"  Sample records: {[getattr(r, 'mood', getattr(r, 'destination', getattr(r, 'upgradeType', getattr(r, 'detail', getattr(r, 'type', 'N/A'))))) for r in records[:2]]}")
        
        print("\n" + "="*50)
        print("Checking with joined query (as the pipeline does):")
        
        # Get record with all related data loaded (like the pipeline does)
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
            print(f"Package ID: {record.id}, Name: {record.name}")
            
            # Show detailed information about each relationship
            print("\nDetailed relationship data:")
            print(f"- Moods: {[(m.mood, m.id) for m in record.moods]}")
            print(f"- Destinations: {[(d.destination, d.id) for d in record.destinations]}")
            print(f"- Tour Plans: {[(tp.dayNumber, tp.detail[:50] + '...' if len(tp.detail) > 50 else tp.detail) for tp in record.tour_plans]}")
            print(f"- Meals: {[(m.mealType, m.detail[:50] + '...' if len(m.detail) > 50 else m.detail) for m in record.meals]}")
            print(f"- Transportations: {[(t.mode, t.detail[:50] + '...' if len(t.detail) > 50 else t.detail) for t in record.transportations]}")
            print(f"- Transport Upgrades: {[(tu.upgradeType, tu.detail[:50] + '...' if len(tu.detail) > 50 else tu.detail) for tu in record.transport_upgrades]}")
        
    except Exception as e:
        print(f"Error in test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_all_related_data()