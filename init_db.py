#!/usr/bin/env python3
"""
Database initializer and seed script.
Creates all tables and seeds default users for development.
Run: python3 init_db.py

Default development accounts:
  admin@eris.local        / Admin@eris2026
  dispatcher@eris.local   / Dispatch@2026
  viewer@eris.local       / Viewer@2026
"""
import asyncio
import sys
import os

# Ensure backend/app is on path
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import create_tables, AsyncSessionLocal
from app.services.auth_service import create_user, get_user_by_email

SEED_USERS = [
    {
        "name": "System Administrator",
        "email": "admin@eris.local",
        "password": "Admin@eris2026",
        "role": "admin",
        "organization": "ERIS Operations",
    },
    {
        "name": "Dispatch Controller",
        "email": "dispatcher@eris.local",
        "password": "Dispatch@2026",
        "role": "dispatcher",
        "organization": "BBMP Emergency Dispatch",
    },
    {
        "name": "Ambulance Operator A07",
        "email": "ambulance@eris.local",
        "password": "Ambulance@2026",
        "role": "ambulance_operator",
        "organization": "BBMP Emergency Services",
    },
    {
        "name": "Hospital Operator – Manipal",
        "email": "hospital@eris.local",
        "password": "Hospital@2026",
        "role": "hospital_operator",
        "organization": "Manipal Hospitals",
    },
    {
        "name": "Read-Only Viewer",
        "email": "viewer@eris.local",
        "password": "Viewer@2026",
        "role": "viewer",
        "organization": "ERIS Monitoring",
    },
]


async def main():
    print("Creating database tables...")
    await create_tables()
    print("Tables created.")

    async with AsyncSessionLocal() as db:
        for user_data in SEED_USERS:
            existing = await get_user_by_email(db, user_data["email"])
            if existing:
                print(f"  [SKIP] {user_data['email']} already exists")
                continue
            user = await create_user(
                db,
                name=user_data["name"],
                email=user_data["email"],
                password=user_data["password"],
                role=user_data["role"],
                organization=user_data["organization"],
            )
            await db.commit()
            print(f"  [OK]   Created {user_data['role']}: {user_data['email']}")

    print("\nSeed complete. Development credentials:")
    for u in SEED_USERS:
        print(f"  {u['role']:25s} | {u['email']:30s} | {u['password']}")

    print("\nNever use these credentials in production.")


if __name__ == "__main__":
    asyncio.run(main())
