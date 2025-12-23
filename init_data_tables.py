import asyncio
import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL connection settings
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "2006")
DB_NAME = os.getenv("DB_NAME", "tripsxing_chatbot")

async def init_data_tables():
    print(f"Connecting to database {DB_NAME}...")
    try:
        conn = await asyncpg.connect(
             host=DB_HOST,
             port=DB_PORT,
             user=DB_USER,
             password=DB_PASSWORD,
             database=DB_NAME
        )
        
        # Create Users Table
        print("Creating users table...")
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create Bookings Table
        print("Creating bookings table...")
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                destination TEXT NOT NULL,
                trip_date DATE NOT NULL,
                status TEXT DEFAULT 'Confirmed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Insert Sample Data for 'Niresh'
        print("Inserting sample data...")
        
        # Check if Niresh exists
        niresh = await conn.fetchrow("SELECT id FROM users WHERE name = $1", "Niresh")
        
        if not niresh:
            # Create Niresh
            user_id = await conn.fetchval("""
                INSERT INTO users (name, email, phone) 
                VALUES ($1, $2, $3) 
                RETURNING id
            """, "Niresh", "niresh@example.com", "+919876543210")
            print(f"✅ Created User: Niresh (ID: {user_id})")
            
            # Create Bookings for Niresh
            await conn.execute("""
                INSERT INTO bookings (user_id, destination, trip_date, status)
                VALUES 
                ($1, 'Goa Beach Resort', '2025-01-15', 'Confirmed'),
                ($1, 'Manali Mountain Trek', '2025-02-20', 'Pending')
            """, user_id)
            print("✅ Created 2 bookings for Niresh")
        else:
            print("User Niresh already exists. Skipping data insertion.")

        await conn.close()
        print("✅ Data tables initialization complete!")

    except Exception as e:
        print(f"❌ Error initializing data tables: {e}")

if __name__ == "__main__":
    asyncio.run(init_data_tables())
