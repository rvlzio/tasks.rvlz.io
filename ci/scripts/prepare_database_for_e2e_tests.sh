#!/bin/sh

PGPASSWORD=${DATABASE_ADMIN_PASSWORD} \
psql -h localhost -d api_test -U ${DATABASE_ADMIN_USERNAME} \
-f "$(pwd)/ci/scripts/sql/prepare_database_for_e2e_tests.sql"
