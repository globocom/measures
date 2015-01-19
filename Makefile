.PHONY: deps-test clean unit acceptance tests upload

deps-test:
	@pip install -r test_requirements.txt

clean:
	@echo "Cleaning up build and *.pyc files..."
	@find . -name "*.pyc" -delete
	@rm -rf .coverage
	@rm -rf ./build
	@rm -rf ./dist
	@rm -rf ./cover
	@rm -rf ./MANIFEST
	@echo "Done!"

unit: clean deps-test
	@coverage run --branch `which nosetests` -vv --with-yanc -s tests/unit/
	@coverage report -m --fail-under=80

acceptance: clean deps-test
	@nosetests -vv --with-yanc -s tests/acceptance/

tests: deps-test
	nosetests -s --cover-branches --cover-erase --with-coverage --cover-inclusive --cover-package=src --with-xunit --with-yanc

focus: deps-test
	nosetests -s --cover-branches --cover-erase --with-coverage --cover-inclusive --cover-package=src --with-xunit --with-yanc --with-focus

upload:
	@python ./setup.py sdist upload -r pypi