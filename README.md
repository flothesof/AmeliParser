Build and coverage status using Travis-CI and coveralls.io:
[![Build Status](https://travis-ci.org/flothesof/AmeliParser.svg?branch=master)](https://travis-ci.org/flothesof/AmeliParser)
[![Coverage Status](https://coveralls.io/repos/flothesof/AmeliParser/badge.svg?branch=master&service=github)](https://coveralls.io/github/flothesof/AmeliParser?branch=master)

# Description

This is a scraping program that can be used to fetch result pages from a database search on [http://ameli-direct.ameli.fr/](http://ameli-direct.ameli.fr/), the French social security website for listing health professionals. 

# Usage

You can use the program in an interactive fashion by copying its source to your working directory and do the following:

```
import new_parser
df = new_parser.make_single_query('ophtalmologiste', '59000')
```
This returns the query results as a pandas DataFrame object, which is handy for all sorts of further manipulation.

Queries over multiple locations are also available. The result is a concatenated pandas DataFrame.

```
import new_parser
df = new_parser.make_multiple_query('ophtalmologiste', ["59910", "59166", "59560", "59170", "59510"])
```

This code is under BSD license.

# Repository notes

A good article on CI and testing: [http://www.deloittedigital.com/eu/blog/untested-code-is-broken-code-test-automation-in-enterprise-software-deliver](http://www.deloittedigital.com/eu/blog/untested-code-is-broken-code-test-automation-in-enterprise-software-deliver).

## Configuring Travis-CI

- [http://conda.pydata.org/docs/travis.html](http://conda.pydata.org/docs/travis.html)
- a great Gist that got me pointed in the right direction [https://gist.github.com/dan-blanchard/7045057](https://gist.github.com/dan-blanchard/7045057)

## Configuring coverage

- [http://levibostian.com/python-code-coverage-and-coveralls-io/](http://levibostian.com/python-code-coverage-and-coveralls-io/)