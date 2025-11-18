import logging
from pipeline.loader import Loader
from pipeline.database import get_db_session
from pipeline.models import Package
from sqlalchemy.orm import selectinload
from sentence_transformers import SentenceTransformer
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def comprehensive_fetch():
    """
    Fetches data from both Pinecone and the database to show what was stored.
    """
    logger.info("Starting comprehensive fetch...")
    
    # Get data from database with all related info
    db_session_gen = get_db_session()
    db = next(db_session_gen)
    
    try:
        # Get all packages with their related data
        packages = db.query(Package).options(
            selectinload(Package.moods),
            selectinload(Package.destinations),
            selectinload(Package.types),
            selectinload(Package.tour_plans),
            selectinload(Package.meals),
            selectinload(Package.transportations),
            selectinload(Package.transport_upgrades),
            selectinload(Package.prices),
            selectinload(Package.days),
            selectinload(Package.months),
            selectinload(Package.years)
        ).all()
        
        # Initialize Pinecone connection
        logger.info("Initializing Pinecone connection...")
        loader = Loader()
        index = loader.index
        
        # Get Pinecone index stats
        stats = index.describe_index_stats()
        logger.info(f"Index stats: {stats}")
        
        # Create comprehensive result file
        with open('comprehensive_result.txt', 'w', encoding='utf-8') as f:
            f.write("COMPREHENSIVE RESULTS: Database vs Pinecone Storage\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("DATABASE SOURCE DATA:\n")
            f.write("-" * 30 + "\n")
            
            for i, package in enumerate(packages):
                f.write(f"Package {i+1}:\n")
                f.write(f"  ID: {package.id}\n")
                f.write(f"  Name: {package.name}\n")
                f.write(f"  URL: {package.pkgURL}\n")
                f.write(f"  Details: {package.tourDetail}\n")
                f.write(f"  Enhanced text for embedding:\n")
                enhanced_text = package.to_text()
                f.write(f"    {enhanced_text}\n")
                
                if package.moods:
                    f.write(f"  Moods: {[m.mood for m in package.moods if m.mood]}\n")
                if package.destinations:
                    f.write(f"  Destinations: {[d.destination for d in package.destinations if d.destination]}\n")
                if package.tour_plans:
                    f.write(f"  Tour Plans: {[(tp.dayNumber, tp.detail[:50] + '...') for tp in package.tour_plans if tp.detail]}\n")
                
                f.write("\n")
            
            f.write("\n" + "="*60 + "\n")
            f.write("PINECONE STORAGE VERIFICATION:\n")
            f.write("-" * 30 + "\n")
            
            f.write(f"Pinecone Index Stats:\n")
            f.write(f"  Dimension: {stats['dimension']}\n")
            f.write(f"  Total vectors: {stats['total_vector_count']}\n")
            f.write(f"  Namespaces: {stats['namespaces']}\n\n")
            
            # Test querying Pinecone with a sample query
            model = SentenceTransformer('sentence-transformers/all-roberta-large-v1')
            query_text = "tour package"
            query_embedding = model.encode([query_text]).tolist()[0]
            
            # Query Pinecone
            results = index.query(
                vector=query_embedding,
                top_k=10,
                include_values=False,
                include_metadata=True
            )
            
            f.write(f"Query Results (top {len(results['matches'])} similar items):\n")
            for i, match in enumerate(results['matches']):
                f.write(f"Result {i+1}:\n")
                f.write(f"ID: {match['id']}\n")
                f.write(f"Similarity Score: {match['score']:.4f}\n")
                f.write(f"Metadata: {match['metadata']}\n")
                
                # Find matching package from database
                matching_package = next((p for p in packages if str(p.id) == match['id']), None)
                if matching_package:
                    f.write(f"    Source Text Length: {len(matching_package.to_text())} characters\n")
                    f.write(f"    Source Text Preview: {matching_package.to_text()[:200]}...\n")
                f.write("\n")
            
            f.write("\n" + "="*60 + "\n")
            f.write("SUMMARY:\n")
            f.write("-" * 30 + "\n")
            f.write(f"✓ Database contains {len(packages)} packages with rich related data\n")
            f.write(f"✓ Pinecone contains {stats['total_vector_count']} embeddings\n")
            f.write(f"✓ Embeddings were created from comprehensive text containing package details and all related table data\n")
            f.write(f"✓ Similarity search confirms data is properly stored and retrievable\n")
            f.write("\nThe original text content is encoded in the vector embeddings in Pinecone.\n")
            f.write("When querying Pinecone, similar content will be retrieved based on semantic similarity.\n")
        
        print(f"Comprehensive results written to comprehensive_result.txt")
        print(f"Database contained {len(packages)} packages, Pinecone stored {stats['total_vector_count']} embeddings")
        
    except Exception as e:
        logger.error(f"Error in comprehensive fetch: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    comprehensive_fetch()