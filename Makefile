.PHONY: tests

tests:
	nosetests -s --cover-branches --cover-erase --with-coverage --cover-inclusive --cover-package=measure --with-xunit
