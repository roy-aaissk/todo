CREATE TABLE IF NOT EXISTS task_status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    status_id INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_status_id FOREIGN KEY(status_id) REFERENCES task_status(id)
);

-- Define the trigger function to update the updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger to call the function before updating any row in tasks
CREATE TRIGGER update_tasks_updated_at
BEFORE UPDATE ON tasks
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

-- task_statusテーブルにテストデータを挿入
INSERT INTO task_status (name) VALUES ('作業前');
INSERT INTO task_status (name) VALUES ('作業中');
INSERT INTO task_status (name) VALUES ('完了');

-- tasksテーブルにテストデータを挿入
INSERT INTO tasks (name, status_id) VALUES ('Task 1', 1);
INSERT INTO tasks (name, status_id) VALUES ('Task 2', 2);
INSERT INTO tasks (name, status_id) VALUES ('Task 3', 3);



