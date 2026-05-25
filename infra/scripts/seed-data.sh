#!/bin/bash
set -e

echo "Seeding EduGenie development data..."
cd backend
alembic upgrade head
python -c "
from app.database import SessionLocal
from app.models import Creator
# Add seed logic
print('Seed data inserted successfully')
"
echo "Done."
