


release:
	pandoc -s README.md -o README.rst
	python3 setup.py check register sdist upload
