.PHONY: all
all: confusables.txt confusables.py

confusables.txt:
	@wget https://www.unicode.org/Public/security/15.1.0/confusables.txt	

.PHONY: test
test:
	@pylint *.py # --disable=line-too-long
	@flake8 *.py # --ignore=E501
	@black --check *.py
