DROP TABLE IF EXISTS todos;

CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    text TEXT NOT NULL CHECK(length(text) <= 1000),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster lookups by user_id
CREATE INDEX IF NOT EXISTS idx_todos_user_id ON todos(user_id);

-- Index for sorting by creation time
CREATE INDEX IF NOT EXISTS idx_todos_created_at ON todos(created_at);

-- Index for sorting by update time
CREATE INDEX IF NOT EXISTS idx_todos_updated_at ON todos(updated_at);

-- Compound index for user_id and created_at (useful for getting user's todos sorted by date)
CREATE INDEX IF NOT EXISTS idx_todos_user_created ON todos(user_id, created_at);

INSERT INTO todos (user_id, text, created_at, updated_at) 
VALUES (1, 'Complete FastAPI tutorial', '2024-02-13 09:00:00', '2024-02-13 09:00:00');

INSERT INTO todos (user_id, text, created_at, updated_at) 
VALUES (1, 'Review pull requests', '2024-02-13 10:30:00', '2024-02-13 11:45:00');

INSERT INTO todos (user_id, text, created_at, updated_at) 
VALUES (1, 'Setup database indices', '2024-02-13 14:15:00', '2024-02-13 14:15:00');

-- User 2's todos
INSERT INTO todos (user_id, text, created_at, updated_at) 
VALUES (2, 'Update documentation', '2024-02-13 08:45:00', '2024-02-13 09:30:00');

INSERT INTO todos (user_id, text, created_at, updated_at) 
VALUES (2, 'Test new features', '2024-02-13 11:00:00', '2024-02-13 11:00:00');

INSERT INTO todos (user_id, text, created_at, updated_at) 
VALUES (2, 'Schedule team meeting', '2024-02-13 13:20:00', '2024-02-13 15:45:00');