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


# Test Plan
1. Verify xml schema vs given referenced xsd file.
2. Verify specific test cases mentioned in the task.
3. Verify that dataflow sends valid data
