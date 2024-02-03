.PHONY:default
default: help

.PHONY: help
help:
	@echo "All Commands:"
	@echo "		clean - Remove temp files"
	@echo "     pubsub_setup - Build image, create topic and subscription"
	@echo "		pubsub_build - Build pubsub emulator image"
	@echo "		pubsub_up - Start pubsub container"
	@echo "     pubsub_create_topic - Create topic"
	@echo "     pubsub_create_subscription - Create subscription"
	@echo "     pubsub_produce - Produce message"
	@echo "     pubsub_consume - Consume messages"

.PHONY: clean
clean:
	- @find . -name "*.pyc" -exec rm -rf {} \;
	- @find . -name "__pycache__" -delete
	- @find . -name "*.pytest_cache" -exec rm -rf {} \;
	- @find . -name "*.mypy_cache" -exec rm -rf {} \;

.PHONY: pubsub_setup
pubsub_setup: pubsub_build pubsub_up pubsub_create_topic pubsub_create_subscription

.PHONY: pubsub_build
pubsub_build:
	docker build --build-arg INSTALL_COMPONENTS="google-cloud-sdk-pubsub-emulator" -t pubsub-emulator:latest -f DockerfilePubsub .

.PHONY: pubsub_up
pubsub_up:
	docker run --name pubsub-emulator -p 8085:8085 -p 8043:8043 -p 8042:8042 --rm pubsub-emulator:latest

.PHONY: pubsub_create_topic
pubsub_create_topic:
	PUBSUB_EMULATOR_HOST=127.0.0.1:8085 python -m pubsub_emulator.create_topic

.PHONY: pubsub_create_subscription
create_subscription:
	PUBSUB_EMULATOR_HOST=127.0.0.1:8085 python -m pubsub_emulator.create_subscription

.PHONY: pubsub_produce
produce:
	PUBSUB_EMULATOR_HOST=127.0.0.1:8085 python -m pubsub_emulator.produce

.PHONY: pubsub_consume
consume:
	PUBSUB_EMULATOR_HOST=127.0.0.1:8085 python -m pubsub_emulator.consume