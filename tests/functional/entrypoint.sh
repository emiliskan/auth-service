#!/bin/sh

/app/tests/functional/wait-for postgres_auth:9200 && echo "es started"
/app/tests/functional/wait-for redis_auth:6379 && echo "redis started"
/app/tests/functional/wait-for backend_auth:8000 && echo "backend_api started"

pytest tests/functional/src

sleep infinity
