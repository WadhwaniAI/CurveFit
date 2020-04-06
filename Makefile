# makefile for easy manage package
.PHONY: clean, tests

build: setup.py
	python3 setup.py build

# make install with optional prefix=directory on command line
install: setup.py
ifdef prefix
	python3 setup.py install --prefix=$(prefix)
else
	python3 setup.py install
endif

sdist: setup.py
	python3 setup.py sdist

tests:
	pytest tests
	python3 example/get_started.py

clean:
	find . -name "*.so*" | xargs rm -rf
	find . -name "*.pyc" | xargs rm -rf
	find . -name "__pycache__" | xargs rm -rf
	find . -name "build" | xargs rm -rf
	find . -name "dist" | xargs rm -rf
	find . -name "MANIFEST" | xargs rm -rf
	find . -name "*.egg-info" | xargs rm -rf
	find . -name ".pytest_cache" | xargs rm -rf

uninstall:
	find $(CONDA_PREFIX)/lib/ -name "*curvefit*" | xargs rm -rf
