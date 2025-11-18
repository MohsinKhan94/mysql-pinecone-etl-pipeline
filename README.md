# MySQL to Pinecone ETL Pipeline

This project implements an ETL (Extract, Transform, Load) pipeline that syncs data from a MySQL database to Pinecone vector database, with enhanced schema support for tour package data.

## Features

- Extracts data from MySQL database (packages table and related tables)
- Transforms package information and related data into vector embeddings
- Loads embeddings into Pinecone for semantic search
- Supports multiple related tables: moods, destinations, tour plans, meals, transportation, etc.
- Batch processing for efficient data handling

## Architecture

The system consists of:
- **Extractor**: Fetches records from MySQL with related data
- **Transformer**: Converts package data and related information to embeddings using sentence-transformers
- **Loader**: Stores embeddings in Pinecone vector database

## Database Schema

The pipeline works with a comprehensive tour package schema including:
- packages (main table)
- packageMood, subMood
- destinations
- pkgDays, pkgMonths, pkgYears
- pkgType
- tourPlan
- numberTravelerPrice
- mealSummary
- transportation
- transportationUpgrade

## Usage

### Setup
1. Configure your MySQL and Pinecone credentials in `.env` file
2. Install dependencies: `pip install -r requirements.txt`
3. Run the pipeline: `python src/main.py`

The pipeline will process records from the last run timestamp and store enriched embeddings in Pinecone.

## Configuration

Environment variables in `.env`:
- Database connection settings
- Pinecone API key and settings
- Embedding model configuration

## Files

- `src/main.py`: Main pipeline entry point
- `src/pipeline/`: Core ETL components
- `src/schema.txt`: Database schema definition
- `src/comprehensive_result.txt`: Verification output