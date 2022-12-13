dev:
	poetry run flask --app page_analyzer:app run
PORT ?= 5000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
lint:
	poetry run flake8
install:
	poetry install
check:
	poetry check
debug:
	poetry run flask --app page_analyzer:app --debug run
