import xmlschema

from typing import Dict

from defusedxml import ElementTree


class XMLParsingError(Exception):
    def __init__(self, *args):
        self.msg_default = 'XML response is corrupt or has invalid structure. '
        super().__init__(self.msg_default, *args)


class NS:
    def __init__(self, url: str):
        """Class for shortening xml namespaces

        Args:
            url: url of the XML file used as a namespace

        Comment:
            implemented because the default way somehow didn't work:
            tree.findall('gen:Obs', namespaces)

        Usage:
            Works like a dictionary. To get the full variable name
            my_namespace = NS('http://path.to.xml')
            my_namespace['variable_name']

        """
        self._url = url

    def __getitem__(self, item):
        return f'{self._url}{str(item)}'


def parse_sdmx_response(xml_str: str) -> Dict:
    """Parses sdmx xml response

    Args:
        xml_str: xml file as a string

    Returns:
        dict
    """
    statistics = dict()
    if not xml_str:
        return statistics

    gen = NS("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}")

    try:
        tree = ElementTree.XML(xml_str)
    except ElementTree.ParseError as e:
        raise XMLParsingError from e

    observation_group = None
    for series in tree.iter(gen['Series']):
        for header in series.find(gen['Attributes']).findall(gen['Value']):
            if header.attrib['id'] == 'TITLE':
                observation_group = header.attrib['value']

        if not observation_group:
            msg = 'No observation group found.'
            raise XMLParsingError(msg)
        else:
            statistics[observation_group] = dict()

        for observation in series.findall(gen['Obs']):
            date_time = observation.find(gen['ObsDimension']).attrib['value']
            value_tag = observation.find(gen['ObsValue'])
            statistics[observation_group][date_time] = value_tag.attrib['value']
    return statistics


def sdmx_resp_scheme_valid(xml_str: str, xsd_str: str):
    """Validates a given xml vs given xml scheme (xsd)

    Args:
        xml_str: xml as string
        xsd_str: xsd as string

    Returns:
        True if scheme is valid, False in other case

    """
    scheme = xmlschema.XMLSchema(xsd_str)
    return scheme.is_valid(xml_str)
