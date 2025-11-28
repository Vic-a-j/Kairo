# Constants
DC := docker-compose
APP_NAME := kairo


# Commands
.PHONY: ps
ps:
	$(DC) ps


.PHONY: build
build:
	$(DC) build


.PHONY: build-clean
build-clean:
	$(DC) build --no-cache


.PHONY: exec
exec:
	$(DC) exec $(APP_NAME) bash


.PHONY: up
up:
	$(DC) up


.PHONY: up-test
up:
	$(DC) up test


.PHONY: down
down:
	$(DC) down


.PHONY: clean
clean:
	$(DC) down