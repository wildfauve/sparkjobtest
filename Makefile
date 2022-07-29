.PHONY: all

all: build

build:
	@echo "Create New Wheel"
	@poetry version patch
	@poetry build

