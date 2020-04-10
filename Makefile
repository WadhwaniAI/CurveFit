# makefile for easy manage package
.PHONY: clean, tests

doc_phony:

gh-pages: doc_phony
	python3 docs/extract_md.py
	mkdocs build
	rm site/extract_md.py
	git checkout mkdocs.yml
	git checkout gh-pages
	rm -r extract_md
	cp -r site/* .

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

examples:
	python3 example/get_started.py
	python3 example/covariate.py
	python3 example/sizes_to_indices.py

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
