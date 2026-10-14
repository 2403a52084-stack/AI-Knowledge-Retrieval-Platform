import os
import sqlite3
import json
from datetime import datetime


# Project root directory
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

# Separate analytics database
DB_PATH = os.path.join(BASE_DIR, "analytics.db")


def get_connection():
    """Create and return a SQLite database connection."""
    return sqlite3.connect(DB_PATH)


def initialize_database():
    """Create the analytics table if it does not already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS query_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            query TEXT NOT NULL,
            query_type TEXT,
            routing TEXT,
            status TEXT,
            confidence TEXT,
            confidence_score REAL,
            clarification_required INTEGER DEFAULT 0,
            response_time_ms REAL,
            domain TEXT,
            retrieved_sources TEXT,
            retrieved_count INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def save_query_analytics(
    query,
    query_type=None,
    routing=None,
    status=None,
    confidence=None,
    confidence_score=None,
    clarification_required=False,
    response_time_ms=None,
    domain=None,
    retrieved_sources=None
):
    """
    Save one query interaction into the analytics database.
    """

    initialize_database()

    if retrieved_sources is None:
        retrieved_sources = []

    # Convert list/dict data into JSON text for SQLite
    if not isinstance(retrieved_sources, str):
        retrieved_sources = json.dumps(retrieved_sources)

    # Count retrieved sources
    try:
        source_data = json.loads(retrieved_sources)
        retrieved_count = len(source_data) if isinstance(source_data, list) else 0
    except Exception:
        retrieved_count = 0

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO query_analytics (
            timestamp,
            query,
            query_type,
            routing,
            status,
            confidence,
            confidence_score,
            clarification_required,
            response_time_ms,
            domain,
            retrieved_sources,
            retrieved_count
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(timespec="seconds"),
        str(query),
        query_type,
        routing,
        status,
        confidence,
        confidence_score,
        1 if clarification_required else 0,
        response_time_ms,
        domain,
        retrieved_sources,
        retrieved_count
    ))

    conn.commit()
    conn.close()


def get_all_analytics():
    """Return all analytics records."""
    initialize_database()

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM query_analytics
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_query_count():
    """Return total number of tracked queries."""
    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM query_analytics
    """)

    count = cursor.fetchone()[0]
    conn.close()

    return count


def get_low_confidence_queries(threshold=0.50):
    """Return queries whose confidence score is below the threshold."""
    initialize_database()

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM query_analytics
        WHERE confidence_score IS NOT NULL
          AND confidence_score < ?
        ORDER BY id DESC
    """, (threshold,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_unanswered_queries():
    """Return queries that were not successfully resolved."""
    initialize_database()

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM query_analytics
        WHERE status IN (
            'low_confidence',
            'no_results',
            'clarification_required',
            'error'
        )
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_analytics_summary():
    """Return basic analytics statistics."""
    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM query_analytics")
    total_queries = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM query_analytics
        WHERE status = 'success'
    """)
    successful_queries = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM query_analytics
        WHERE status IN (
            'low_confidence',
            'no_results',
            'clarification_required',
            'error'
        )
    """)
    unresolved_queries = cursor.fetchone()[0]

    cursor.execute("""
        SELECT AVG(response_time_ms)
        FROM query_analytics
        WHERE response_time_ms IS NOT NULL
    """)
    avg_response_time = cursor.fetchone()[0]

    conn.close()

    return {
        "total_queries": total_queries,
        "successful_queries": successful_queries,
        "unresolved_queries": unresolved_queries,
        "average_response_time_ms": avg_response_time
    }


# Initialize database when this module is imported
initialize_database()


if __name__ == "__main__":
    print("Analytics database:", DB_PATH)
    print("Total queries:", get_query_count())