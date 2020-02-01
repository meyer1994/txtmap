.PHONY: compile lint test postgres clean


compile:
	python -m compileall handler.py
	python -m compileall txtmap
	python -m compileall tests


lint:
	python -m flake8 --statistics --show-source handler.py
	python -m flake8 --statistics --show-source txtmap/**.py
	python -m flake8 --statistics --show-source tests/**.py


test: postgres
	python -m unittest discover -vb tests


postgres:
	docker run --rm --name test_pgdb -p 5432:5432 -d postgres
	@until pg_isready -h localhost -p 5432; do sleep 1; done
	psql -h localhost -p 5432 -U postgres -f schema.sql


clean:
	docker kill test_pgdb
