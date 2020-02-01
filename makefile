.PHONY: compile lint


compile:
	python -m compileall handler.py
	python -m compileall txtmap
	python -m compileall tests


lint:
	python -m flake8 --statistics --show-source handler.py
	python -m flake8 --statistics --show-source txtmap/**.py
	python -m flake8 --statistics --show-source tests/**.py


test:
	python -m unittest discover -vb tests
