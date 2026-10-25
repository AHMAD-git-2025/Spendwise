#!/usr/bin/env python3
"""Database initialization script for Render build/deploy and Aiven MySQL setup."""
import sys
from db import init_db

if __name__ == "__main__":
    try:
        init_db()
        print("SpendWise: Database tables verified and ready.")
    except Exception as exc:
        print("Warning: Database initialization notice:", exc)
        # Avoid failing the Render build if the database is configured in the web service environment
        sys.exit(0)
