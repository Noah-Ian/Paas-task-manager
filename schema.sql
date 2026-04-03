-- Database Schema for TaskFlow App
-- PostgreSQL

CREATE TABLE IF NOT EXISTS tasks (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(200) NOT NULL,
    description TEXT,
    completed   BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample Data
INSERT INTO tasks (title, description, completed) VALUES
  ('Set up Railway account', 'Create account at railway.app and connect GitHub', TRUE),
  ('Deploy Flask app', 'Push code to GitHub and link to Railway project', FALSE),
  ('Configure environment variables', 'Set DATABASE_URL in Railway dashboard', FALSE),
  ('Test CRUD operations', 'Create, read, update and delete tasks via the UI', FALSE),
  ('Write assignment report', 'Document deployment process and Railway vs Heroku comparison', FALSE);