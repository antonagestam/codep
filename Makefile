format:
	sorti codep
	black codep

lint:
	sorti --check codep
	black --check codep
	flake8
	mypy codep

distribute:
	pip install --upgrade wheel twine
	python setup.py sdist bdist_wheel
	twine upload dist/*
