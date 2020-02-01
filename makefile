.PHONY: compile lint test postgres clean install venv


compile:
	python -m compileall handler.py
	python -m compileall txtmap
	python -m compileall tests


lint:
	flake8 --show-source handler.py txtmap/**.py tests/**.py


venv:
	python -m venv venv --clear


install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt


test:
	python -m unittest discover -vb tests


postgres:
	docker run --rm --name test_pgdb -p 5432:5432 -d postgres
	until pg_isready -h localhost -p 5432; do sleep 1; done
	psql -h localhost -p 5432 -U postgres -f schema.sql -a


clean:
	docker kill test_pgdb
