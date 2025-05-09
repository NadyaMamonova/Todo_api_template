from yoyo import step

steps = [
    step(
        """
        CREATE TABLE tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT NOW(),
            due_date TIMESTAMP,
            status VARCHAR(50) DEFAULT 'todo'
        )
        """,
        "DROP TABLE tasks"
    )
]