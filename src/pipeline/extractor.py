import logging
from datetime import datetime
from sqlalchemy.orm import Session, selectinload
from . import models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_records_to_update(db: Session, last_run_timestamp: datetime, batch_size: int):
    """
    Fetches a batch of records from the 'packages' table with related data.
    Since the schema does not have an updated_at column, we'll fetch records
    without time-based filtering.

    Args:
        db: The SQLAlchemy database session.
        last_run_timestamp: The timestamp of the last successful pipeline run.
        batch_size: The number of records to fetch in one batch.

    Returns:
        A list of Package objects with related data loaded.
    """
    logger.info(f"Fetching records from packages table with related data")

    # Use selectinload to efficiently load related data
    query = db.query(models.Package).options(
        selectinload(models.Package.moods),
        selectinload(models.Package.sub_moods),
        selectinload(models.Package.destinations),
        selectinload(models.Package.days),
        selectinload(models.Package.months),
        selectinload(models.Package.years),
        selectinload(models.Package.types),
        selectinload(models.Package.tour_plans),
        selectinload(models.Package.prices),
        selectinload(models.Package.meals),
        selectinload(models.Package.transportations),
        selectinload(models.Package.transport_upgrades)
    )

    records = query.limit(batch_size).all()

    logger.info(f"Found {len(records)} records to process in this batch.")
    return records
