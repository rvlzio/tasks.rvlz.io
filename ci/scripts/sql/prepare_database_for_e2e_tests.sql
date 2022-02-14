BEGIN;

--Clear tables
DELETE FROM api.tasks;
DELETE FROM api.users;

--Insert an API user
INSERT INTO api.users (identifier, username, email, password_hash)
VALUES (
    'T4krC5DA5FJO05hemDbBElraQCzN9a2kWOrLsW6A',
    'user',
    'user@gmail.com',
    'MzI3Njg=.OA==.MQ==.fWnMtvSVUHRsxJgXr92B0A==.20QCPyN+C2qU9giieyxgIFkyBZWOpV8rHI9u5daeVJe/6j48mh4J8TXB/KFlF4c0hj/NVFYABoa07YJRf9Qq2w=='
);

END;
