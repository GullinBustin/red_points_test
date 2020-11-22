install-req:
	pip install -r requirements/dev.txt

run:
	cd source && python main.py

run-test:
	python -m pytest
