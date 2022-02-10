BEGIN;

CREATE TABLE IF NOT EXISTS api.tasks (
    _pk BIGSERIAL PRIMARY KEY,
    identifier VARCHAR(100) UNIQUE NOT NULL,
    subject TEXT NOT NULL,
    description TEXT NOT NULL,
    completed BOOLEAN NOT NULL
);

GRANT SELECT, INSERT, DELETE, UPDATE ON api.tasks TO api;
GRANT USAGE, SELECT ON SEQUENCE api.tasks__pk_seq TO api;

END;
