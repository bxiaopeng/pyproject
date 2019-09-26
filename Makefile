.PHONY: test clean

# mypackage 改成你自己的包名
PACKAGENAME := mypackage

PY = $(shell find $(PACKAGENAME) -type f -name "*.py")

lint:
	isort --check -rc $(PACKAGENAME)
	black --check $(PACKAGENAME)
	flake8 $(PACKAGENAME)
	mypy $(PY)

fmt format:
	isort -rc $(PACKAGENAME)/*.py tests/*.py
	black $(PACKAGENAME)/*.py tests/*.py

# 创建虚拟环境
env venv:
	pip install pipenv --upgrade
	export PIPENV_VENV_IN_PROJECT=true && pipenv --three
	pipenv shell

install:
	pipenv install --skip-lock
	pipenv install --dev --skip-lock

upload-local: test
	python setup.py sdist bdist_wheel
	twine upload dist/* -r local
	rm -fr build dist .egg $(PACKAGENAME).egg-info .pytest_cache

test:
	pytest

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	rm -fr build dist .egg sabah.egg-info .pytest_cache

ci:
	pipenv run py.test -n 8 --boxed --junitxml=report.xml

coverage:
	pipenv run py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=$(PACKAGENAME) tests

#publish:
