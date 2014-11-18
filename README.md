# README #

A python library to send application metrics using UDP.

[![Build Status](https://travis-ci.org/globocom/measure.svg?branch=master)](https://travis-ci.org/globocom/measure)

### How do I get set up? ###

* Summary of set up
	
	`mkvirtualenv measure`
	`pip install -r test_requirements.txt`

* Usage

	`from measure import Measure`
	`measure = Measure('myclient', ('localhost', 1984))`
	`measure.count('mymetric', dimensions={'name': 'john'})`

* How to run tests

	`make tests`

### Contribution guidelines ###

* Writing tests
* Code review

### Who do I talk to? ###

* Repo owner or admin

	busca@corp.globo.com
