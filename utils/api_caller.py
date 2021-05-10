import requests

from typing import Optional, Dict


class HttpErrorResponseStructureCorrupted(BaseException):
    pass


def get_currency_exchange_rates(
        resource: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str]] = None,
        **kwargs
) -> requests.Response:
    request_headers = {
        'Accept': 'application/vnd.sdmx.genericdata+xml; version=2.1',
        'If-Modified-Since': ''
    }
    request_params = {
        'startPeriod': '',
        'endPeriod': '',
        'detail': 'full'
    }
    if headers:
        request_headers.update(headers)
    if params:
        request_params.update(params)
    return requests.get(resource, params=request_params, headers=request_headers, **kwargs)
