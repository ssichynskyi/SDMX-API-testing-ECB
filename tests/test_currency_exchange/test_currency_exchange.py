import datetime
import pytest
import requests

from utils.api_caller import get_currency_exchange_rates
from utils.api_resource_builder import CurrencyExchangeResource, SDMXSchemas
from utils.sdmx_respond_parser import parse_sdmx_response, sdmx_resp_scheme_valid


TEST_DATA_AND_EXP_RESULT = [
    (
        {
            'api resource': CurrencyExchangeResource('D', 'EUR', ['USD']),
            'startPeriod': '2021-05-06',
            'endPeriod': '2021-05-08'
        },
        {
            'observation titles': ['US dollar/Euro'],
            'observations': ['2021-05-06', '2021-05-07']
        }
    ),
    (
        {
            'api resource': CurrencyExchangeResource('D', 'EUR', ['USD', 'JPY']),
            'startPeriod': '2021-05-03',
            'endPeriod': '2021-05-07'
        },
        {
            'observation titles': ['US dollar/Euro', 'Japanese yen/Euro'],
            'observations': ['2021-05-03', '2021-05-04', '2021-05-05', '2021-05-06', '2021-05-07']
        }
    ),
    (
        {
            'api resource': CurrencyExchangeResource('M', 'EUR', ['JPY', 'USD', 'NOK']),
            'startPeriod': '2021-01',
            'endPeriod': '2021-04'
        },
        {
            'observation titles': ['US dollar/Euro', 'Norwegian krone/Euro', 'Japanese yen/Euro'],
            'observations': ['2021-01', '2021-02', '2021-03', '2021-04']
        }
    )
]


@pytest.mark.critical
def test_response_scheme_valid():
    # This test fails. Because of lack of time and poor documentation
    # it's hard to say if it is True positive or False positive result
    schema_resource = SDMXSchemas('ECB_EXR1')
    resp = requests.get(schema_resource)
    assert resp.status_code == 200
    xsd_str = resp.text
    data_resource = CurrencyExchangeResource('D', 'EUR', ['USD'])
    request_params = {
        'startPeriod': '2021-05-06',
        'endPeriod': '2021-05-08'
    }
    resp = get_currency_exchange_rates(data_resource, params=request_params)
    assert resp.status_code == 200
    assert sdmx_resp_scheme_valid(resp.text, xsd_str)


@pytest.mark.major
@pytest.mark.parametrize('test_input,expected', TEST_DATA_AND_EXP_RESULT)
def test_currency_exchange_stats(test_input, expected):
    # ToDo: add xsd validation    res = CurrencyExchangeResource('D', 'EUR', ['USD', 'JPY'])
    request_params = {
        'startPeriod': test_input['startPeriod'],
        'endPeriod': test_input['endPeriod']
    }
    resp = get_currency_exchange_rates(test_input['api resource'], params=request_params)
    assert resp.status_code == 200
    stats = parse_sdmx_response(resp.text)
    msg = 'Number of observation series does not correspond to request params'
    assert len(stats.keys()) == len(expected['observation titles']), msg
    for title in stats.keys():
        msg = f'Number of observations in series with title "{title}"'
        msg = f'{msg} does not correspond to request params: {expected["observations"]}'
        assert len(stats[title].keys()) == len(expected['observations']), msg
        for observation_date_time in stats[title].keys():
            msg_supplement = f'"{title}", observation: {observation_date_time}'
            msg = f'Unexpected observation date and time in series with title: {msg_supplement}'
            assert observation_date_time in expected['observations'], msg
            msg = f'Observation exchange rate format is not float in series with title: {msg_supplement}'
            try:
                float(stats[title][observation_date_time])
            except ValueError:
                assert False, msg


@pytest.mark.major
def test_http_routing():
    http_res = CurrencyExchangeResource('D', 'EUR', ['USD'], 'http')
    https_res = CurrencyExchangeResource('D', 'EUR', ['USD'], 'https')
    request_params = {
        'startPeriod': '2021-05-06',
        'endPeriod': '2021-05-08'
    }
    resp = get_currency_exchange_rates(http_res, params=request_params, allow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers['Location'].startswith(https_res)


@pytest.mark.major
def test_if_modified_since_header():
    # This functionality doesn't work on a server - API defect.
    # So, this test is expected to fail.
    # Response 304 is sent only in case timestamp in 'If-Modified-Since'
    # header fully matches with one from 'Last-Modified' header
    # In order to make sure set: datetime.timedelta(seconds=0)
    dt_format = '%a, %d %b %Y %H:%M:%S %Z'
    res = CurrencyExchangeResource('D', 'EUR', ['USD'])
    request_params = {
        'startPeriod': '2021-05-05',
        'endPeriod': '2021-05-08'
    }
    request_headers = {
        'If-Modified-Since': ''
    }
    resp = get_currency_exchange_rates(res, params=request_params)
    assert resp.status_code == 200
    resp_dt = datetime.datetime.strptime(resp.headers['Last-Modified'], dt_format)
    new_dt = resp_dt + datetime.timedelta(seconds=1)
    # Trick with timezone below done because of improper timezone handling
    # by python bug: https://bugs.python.org/issue22377
    request_headers['If-Modified-Since'] = f'{new_dt.strftime(dt_format)}GMT'
    resp = get_currency_exchange_rates(res, params=request_params, headers=request_headers)
    assert resp.status_code == 304
