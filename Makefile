format:
	sorti codep examples
	black codep examples

lint:
	sorti --check codep examples
	black --check codep examples
	flake8
	mypy codep examples

distribute:
	pip install --upgrade wheel twine
	python setup.py sdist bdist_wheel
	twine upload dist/*
