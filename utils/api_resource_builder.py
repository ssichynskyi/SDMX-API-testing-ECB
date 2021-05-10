from typing import Optional, List
from urllib.parse import urlparse, urlunparse

from utils.env_config import config


class Key:
    def __new__(
            cls,
            freq: str,
            curr_reference: str,
            curr_measured: Optional[List[str]] = None,
            exchange_rate_type: str = 'SP00',
            variation: str = 'A'
    ) -> str:
        """Key resource constructor

        References:
            https://sdw-wsrest.ecb.europa.eu/help/#tabOverview

        Args:
            freq: one-char string as specified in:
                https://sdmx.org/wp-content/uploads/CL_FREQ_v2.0_update_April_2015.doc
            curr_measured: list of three-char string as specified in:
                https://sdmx.org/wp-content/uploads/CL_CURRENCY_1.0_2009.doc
            curr_reference: three-char string as specified in:
                https://sdmx.org/wp-content/uploads/CL_CURRENCY_1.0_2009.doc
            exchange_rate_type: 'SP00' is currently the only known supported
            variation: 'A' is currently the only known supported

        Return:
            string of the defined format e.g. D.USD+JPY.EUR.SP00.A

        Note: no arguments validity check is performed.
            Assumed only used by qualified developer (and lack of time)
        """
        if curr_measured:
            curr_measured = '+'.join(curr_measured)
        else:
            curr_measured = ''
        return '.'.join((freq, curr_measured, curr_reference, exchange_rate_type, variation))


class SDMXResource:
    def __new__(
        cls,
        ws_entry_point: str,
        resource: str,
        flow_id: List[str],
        key_str: str,
        scheme: str = 'https'
    ) -> str:
        """Constructs the full SDMX URL from given params

        Args:
            ws_entry_point: basic url with or without scheme. Given scheme is ignored.
            resource: specific resource e.g. '/data/' with or without '/'
            flow_id: tuple of 1-3 params - (AGENCY_ID, FLOW_ID, VERSION)
                all but FLOW_ID could be omitted
            key_str: specially formatted string, use Key class to construct
            scheme: scheme or protocol e.g. https

        Returns:
            url as string
        """
        flow_id = f'{",".join(flow_id)}/'
        uri = urlparse(ws_entry_point)
        path = '/'.join((uri.path, resource, flow_id, key_str)).replace('//', '/')
        return urlunparse((scheme, uri.netloc, path, None, None, None))


class CurrencyExchangeResource(SDMXResource):
    def __new__(
            cls,
            freq: str,
            currency: str,
            currencies: List[str],
            scheme: str = 'https'
    ) -> str:
        """Creates url resource for currency exchange

        Args:
            freq: one-char string as specified in:
                https://sdmx.org/wp-content/uploads/CL_FREQ_v2.0_update_April_2015.doc
            currency: three-char string as specified in:
                https://sdmx.org/wp-content/uploads/CL_CURRENCY_1.0_2009.doc
            currencies: a list of three-char string as specified in:
                https://sdmx.org/wp-content/uploads/CL_CURRENCY_1.0_2009.doc
            scheme: 'http' or 'https'

        Returns:
            string representing ready API resource to call

        """
        key = Key(freq, currency, currencies)
        return super().__new__(
            cls,
            config['ECB_HOST']['prod']['url'],
            config['ECB_HOST']['prod']['services']['data']['name'],
            config['ECB_HOST']['prod']['services']['data']['currency exchange flow'],
            key,
            scheme
        )


class SDMXSchemas:
    def __new__(cls, structure_id):
        path = '/'.join(config['ECB_HOST']['prod']['services']['schemas'])
        path = '/'.join((config['ECB_HOST']['prod']['url'], path, structure_id))
        return path
