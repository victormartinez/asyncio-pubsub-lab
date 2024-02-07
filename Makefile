.PHONY:default
default: help

.PHONY: help
help:
	@echo "All Commands:"
	@echo "	clean - Remove temp files"
	@echo "	 "
	@echo "	pubsub_build - Build pubsub emulator image"
	@echo "	pubsub_up - Start pubsub container"
	@echo "	pubsub_create_topic - Create topic"
	@echo "	pubsub_create_subscription - Create subscription"
	@echo "	pubsub_producer - Produce message"
	@echo "	pubsub_consumer - Consume messages"
	@echo "	 "
	@echo "	db_connect - Connect to database"
	@echo "	db_generate_revision - Generate alembic revision"
	@echo "	db_upgrade - Database upgrade"
	@echo "	db_downgrade - Database downgrade"
	@echo "	db_drop - Database drop"
	@echo "	db_up - Database up"
	@echo "	db_down - Database down"
	@echo "	 "
	@echo "	run_command - Run command"
	@echo "	run_query - Run query"
	@echo "	run_task - Run task"


.PHONY: clean
clean:
	- @find . -name "*.pyc" -exec rm -rf {} \;
	- @find . -name "__pycache__" -delete
	- @find . -name "*.pytest_cache" -exec rm -rf {} \;
	- @find . -name "*.mypy_cache" -exec rm -rf {} \;

.PHONY: pubsub_build
pubsub_build:
	docker build --build-arg INSTALL_COMPONENTS="google-cloud-sdk-pubsub-emulator" -t pubsub-emulator:latest -f DockerfilePubsub .

.PHONY: pubsub_up
pubsub_up:
	docker run --name pubsub-emulator -p 8085:8085 -p 8043:8043 -p 8042:8042 --rm pubsub-emulator:latest

.PHONY: pubsub_create_topic
pubsub_create_topic:
	PUBSUB_EMULATOR_HOST=127.0.0.1:8085 python -m src.pubsub_emulator.create_topic

.PHONY: pubsub_create_subscription
pubsub_create_subscription:
	PUBSUB_EMULATOR_HOST=127.0.0.1:8085 python -m src.pubsub_emulator.create_subscription

.PHONY: pubsub_producer
pubsub_producer:
	PUBSUB_EMULATOR_HOST=127.0.0.1:8085 python -m src.pubsub_emulator.producer

.PHONY: pubsub_consumer
pubsub_consumer:
	PUBSUB_EMULATOR_HOST=127.0.0.1:8085 python -m src.pubsub_emulator.consumer

.PHONY: db_connect
db_connect:
	PGPASSWORD=postgres psql -d postgres -h 127.0.0.1 -U postgres

.PHONY: db_generate_revision
db_generate_revision:
	alembic revision --autogenerate

.PHONY: db_upgrade
db_upgrade:
	alembic upgrade head

.PHONY: db_downgrade
db_downgrade:
	alembic downgrade -1

.PHONY: db_drop
db_drop:
	rm -rf volumes/
	docker container ls -a | grep asyncio_pubsub_lab_db | awk '{print $$1}' | xargs docker container stop | xargs docker container rm

.PHONY: db_up
db_up:
	docker compose -f docker-compose.yaml up

.PHONY: db_down
db_down:
	docker compose -f docker-compose.yaml down --remove-orphans

.PHONY: run_command
run_command:
	python -m src -module command

.PHONY: run_query
run_query:
	python -m src -module query


.PHONY: run_task
run_task:
	PUBSUB_EMULATOR_HOST=127.0.0.1:8085 python -m src.workers.consumer
