# Data Directory

This directory is used for storing the SQLite database file.

## Files

- `customers.db` - SQLite database file (automatically created on first run)

## Notes

- The database file is not committed to git (excluded in .gitignore)
- The database is automatically initialized with sample data on first run
- For Cloud Run deployment, the database is ephemeral and will be recreated on each container restart
- For persistent storage in production, consider using Cloud SQL or mounting a persistent volume
