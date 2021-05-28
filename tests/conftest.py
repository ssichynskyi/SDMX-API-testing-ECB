import pytest


@pytest.fixture(scope="package", autouse=True)
def example():
    """This is an example fixture to use across all tests"""
