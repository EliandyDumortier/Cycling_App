import sqlite3
import random

def populate_database(db_path="cycling.db"):
    """Populate the database with new users, athletes, and performance data."""

    # Ensure proper database connection
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Insert 19 new athletes and 1 new coach into the user table
        new_users = [
            (f"Athlete {i}", f"athlete{i}@mail.com", "$2b$12$dummyhash", "athlete") for i in range(2, 21)
        ] + [("Coach2", "coach2@mail.com", "$2b$12$dummyhash", "coach")]

        cursor.executemany("INSERT INTO user (name, email, password, role) VALUES (?, ?, ?, ?)", new_users)
        conn.commit()

        # Retrieve all athlete users (excluding coaches) to insert into the athlete table
        cursor.execute("SELECT user_id, name FROM user WHERE role = 'athlete'")
        athlete_users = cursor.fetchall()

        # Insert all athletes into the athlete table
        new_athletes = [
            (name, random.choice(["male", "female"]), random.randint(18, 40),
             round(random.uniform(50, 90), 2), round(random.uniform(1.50, 2.00), 2), user_id)
            for user_id, name in athlete_users
        ]

        cursor.executemany("INSERT INTO athlete (name, gender, age, weight, height, user_id) VALUES (?, ?, ?, ?, ?, ?)", new_athletes)
        conn.commit()

        # Retrieve all athlete IDs
        cursor.execute("SELECT athlete_id FROM athlete")
        athlete_ids = [row[0] for row in cursor.fetchall()]

        # Function to generate random performance data
        def generate_performance_data(athlete_id):
            return (
                round(random.uniform(45, 65), 2),  # vo2max
                random.randint(160, 200),  # hr_max
                random.randint(80, 110),  # cadence_max
                random.randint(280, 400),  # ppo
                random.randint(180, 300),  # p1
                random.randint(160, 280),  # p2
                random.randint(140, 260),  # p3
                athlete_id
            )

        # Insert a variable number of performance records (0 to 5) per athlete
        performance_data = []
        for athlete_id in athlete_ids:
            num_performances = random.randint(0, 5)  # Randomly assign 0 to 5 performances per athlete
            for _ in range(num_performances):
                performance_data.append(generate_performance_data(athlete_id))

        # Insert performance data into the performance table
        cursor.executemany(
            "INSERT INTO performance (vo2max, hr_max, cadence_max, ppo, p1, p2, p3, athlete_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            performance_data
        )

        conn.commit()

    return len(new_users), len(new_athletes), len(performance_data)

# Run the function
populate_database()
