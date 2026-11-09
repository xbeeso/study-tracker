#!/usr/bin/env bash
# backup.sh: save a dated copy of the database, and keep only the newest 7.

# Stop at the first error.
set -e

# Go to the project folder (where this script lives).
cd "$(dirname "$0")"

# Backups live OUTSIDE the project, so git never sees them.
BACKUP_DIR="$HOME/backups/study-tracker"
mkdir -p "$BACKUP_DIR"
# 700 = only you can enter this folder. Backups contain password hashes.
chmod 700 "$BACKUP_DIR"

# Date and time in the file name, e.g. db-2026-11-08_14-30.sqlite3
STAMP=$(date +%Y-%m-%d_%H-%M)
FILE="$BACKUP_DIR/db-$STAMP.sqlite3"

# .backup copies safely, even while the site is writing to the database.
sqlite3 db.sqlite3 ".backup '$FILE'"
# 600 = only you can read the backup file.
chmod 600 "$FILE"

# Keep the newest 7 backups, delete the rest:
# ls -1t lists newest first, tail -n +8 skips the first 7, xargs -r rm deletes what's left.
ls -1t "$BACKUP_DIR"/db-*.sqlite3 | tail -n +8 | xargs -r rm --

echo "$(date '+%Y-%m-%d %H:%M') backup saved: $FILE"
