# This was a testing task for testing ECB SDMX API
It received a very good feedback from task originators and brought me to the next stage.

## Task
Here's a task description as it was given:

### General description
The challenge is to create a testing plan for a Rest API. The one used for this challenge will be the European Central Bank
(https://sdw-wsrest.ecb.europa.e/help/)
You are expected to define tests for different functionalities, how to test them, and how to automate them.
You can use any appropriate software. Please write the tests in the relevant language, and send them to us with instructions on how to run them
(with documentation if any manual step is involved and how to evaluate the answers if not obvious from the result).

### Tests
Please implement two tests to validate that the ECB Rest API works correctly. They should test basic functionality and behavior of the ECB Rest
API (not all the functionalities and behavior but some important and relevant ones)
Your tests should cover at least the following functionalities:
- The key operator correctly implements the OR operator
  (e.g. retrieve the exchange rates against the euro for both the US dollar and the Japanese Yen)

- Using the If-Modified-Since header with a date past the last update returns an HTTP 304 response code

- Protocol is https only, and browser calls to http protocol are redirected to https

### Expectations
You should spend about 2-4 hours working on the topic
Find relevant tests for the functionality and behavior that correspond to what the Rest API aims to deliver
Documentation is about the tests, what and how they validate, not about the tools you are using

## Solution
### Test Plan
- verify xml scheme vs given referenced xsd file.
- verify specific test cases mentioned in the task.

#### Details on tests
##### test_response_scheme_valid
- Get the xml scheme using ECB API which provides schemas
- Get some basic Currency Exchange response
- Validate response vs xml scheme

For more info see comments to this test

##### test_currency_exchange_stats
- Call Currency Exchange API using parametrized test data
- Evaluate response vs expected data

##### test_http_routing
- Call Currency Exchange API using http scheme/protocol and allow_redirects=False
- Evaluate that response code == 304 and Location header pointing into correct place

##### test_if_modified_since_header
- Call Currency Exchange API using
- parse time and date of the last update (header "Last-Modified")
- increase response date by 1 second and feed this to 'If-Modified-Since' header
- Evaluate that response code is 304
For more info see comments to this test

#### Out of scope
- ISTQB-like specification of Test Cases in this document (summary, priority, precondition, Actions, Expected results... etc in order to keep file smaller)

- full test coverage

- corner cases in specified use-cases

- reporting (can be done on-top of it via e.g. Allure without changes)

### Setup and run instruction:
Here and below: console snippets are relevant for latest Ubuntu versions
1. Install latest Python3 version with pip
```console
sudo apt update
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.9
sudo apt install python3.9-distutils
```
2. Install pipenv. Depending on your envvars and previous Python2 and Python3 installations:
```console
pip3 install --upgrade pip
pip3 install pipenv
```
or
```console
python3.9 -m pip install --upgrade pip
python3.9 -m pip install pipenv
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
Optionally you can use all applicable pytest options of your choice:
https://docs.pytest.org/en/6.2.x/usage.html
