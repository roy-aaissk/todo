CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL,
    name VARCHAR(255),
    status_id INT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS task_status (
    id SERIAL,
    name VARCHAR(255),
    created_at TIMESTAMP,
    PRIMARY KEY (id)
);

-- task_statusテーブルにテストデータを挿入
INSERT INTO task_status (name) VALUES ('作業前');
INSERT INTO task_status (name) VALUES ('作業中');
INSERT INTO task_status (name) VALUES ('完了');

-- tasksテーブルにテストデータを挿入
INSERT INTO tasks (name, status_id) VALUES ('Task 1', 1);
INSERT INTO tasks (name, status_id) VALUES ('Task 2', 2);
INSERT INTO tasks (name, status_id) VALUES ('Task 3', 3);



