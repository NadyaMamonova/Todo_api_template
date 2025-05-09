from yoyo import step

steps = [
    step(
        """
        CREATE TABLE tasks (
            id UUID PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            due_date TIMESTAMP,
            status TEXT NOT NULL
        )
        """,
        "DROP TABLE tasks"
    )
]