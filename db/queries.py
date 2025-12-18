CREATE_TASKS = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task  TEXT NOT NULL,
        completed INTEGER DEFAULT 0
    )
"""


INSERT_TASKS = "INSERT INTO tasks (task) VALUES (?)"

SELECT_TASKS = 'SELECT id, task,completed FROM tasks'

SELECT_TASKS_COMLETED = 'SELECT id, task,completed FROM tasks WHERE completed = 1'

SELECT_TASKS_UNCOMLETED = 'SELECT id, task,completed FROM tasks WHERE completed = 0'

UPDATE_TASKS = 'UPDATE tasks SET task = ? WHERE id = ?'

DELETED_TASKS = "DELETE FROM tasks WHERE id = ?"
