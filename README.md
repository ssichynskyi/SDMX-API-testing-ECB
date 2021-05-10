# Testing task provided by Polytech for testing ECB SDMX API

## Task

### Context
The challenge is to create a testing plan for a Rest API. The one used for this challenge will be the European Central Bank (https://sdw-wsrest.
ecb.europa.eu/help/ )
You are expected to define tests for different functionalities, how to test them, and how to automate them.
You can use any appropriate software. Please write the tests in the relevant language, and send them to us with instructions on how to run them
(with documentation if any manual step is involved and how to evaluate the answers if not obvious from the result).

### Tests
Please implement two tests to validate that the ECB Rest API works correctly. They should test basic functionality and behavior of the ECB Rest
API (not all the functionalities and behavior but some important and relevant ones)
Your tests should cover at least the following functionalities:
- The key operator correctly implements the OR operator (e.g., retrieve the exchange rates against the euro for both the US dollar and the
Japanese Yen)
- Using the If-Modified-Since header with a date past the last update returns an HTTP 304 response code
- Protocol is https only, and browser calls to http protocol are redirected to https

### Expectations
You should spend about 2-4 hours working on the topic
Find relevant tests for the functionality and behavior that correspond to what the Rest API aims to deliver
Documentation is about the tests, what and how they validate, not about the tools you are using


## Test Plan
- verify xml scheme vs given referenced xsd file.
- verify specific test cases mentioned in the task.

### Out of scope
- full test coverage
- corner cases in specified use-cases
- reporting (can be done on-top of it via e.g. Allure without changes)

### Setup and run instruction:
Here and below: console snippets are relevant for debian-based system
1. Install latest Python3 version with pip
```console
sudo apt install python3.8
```
2. Install pipenv. Depending on your envvars and previous Python2 installations:
```console
pip install pipenv
```
or
```console
pip3 install pipenv
```
3. Clone/unpack this project and enter project root
```console
cd tt_polytech_ecb_api
```
4. Create virtual environment
```console
pipenv shell
pipenv install
```
5. Run tests
```console
pytest
```
or
```console
python3 -m pytest
```
Optionally you can use all applicable pytest options by your choice:
https://docs.pytest.org/en/6.2.x/usage.html
