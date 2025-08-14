#!/bin/bash
set -e

source .test.env

execute_sql() {
  PGPASSWORD=$POSTGRES_PASSWORD psql \
    -h $DB_HOST \
    -U $POSTGRES_USER \
    -d $1 \
    -c "$2"
}

echo "Creating a test database $POSTGRES_DB..."
execute_sql "postgres" "CREATE DATABASE $POSTGRES_DB;"

export POSTGRES_DB=$POSTGRES_DB

echo "Applying migrations to the test database..."
alembic upgrade head

echo "We run the tests..."
pytest tests/
TEST_RESULT=$?

echo "Deleting the test database $POSTGRES_DB..."
execute_sql "postgres" "DROP DATABASE $POSTGRES_DB;"

if [ $TEST_RESULT -ne 0 ]; then
  echo "The tests failed with an error"
  exit $TEST_RESULT
else
  echo "The tests were successful"
  exit 0
fi
