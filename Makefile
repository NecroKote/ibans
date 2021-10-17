.PHONY: docker run test

run:
	poetry run python ibans

docker:
	docker build -t ibans .

test:
	poetry run pytest --cov --cov-report=html
