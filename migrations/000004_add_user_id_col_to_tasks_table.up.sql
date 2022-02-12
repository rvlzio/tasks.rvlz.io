BEGIN;

ALTER TABLE api.tasks ADD COLUMN _user_pk BIGINT REFERENCES api.users (_pk);

END;

