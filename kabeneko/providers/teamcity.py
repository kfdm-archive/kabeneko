import logging
import requests
import xml.etree.cElementTree as ET

logger = logging.getLogger(__name__)


class TeamCity(object):
    def __init__(self, host):
        self.host = host

    def poll(self):
        successes = []
        investigation = []
        failures = []

        try:
            req = requests.get(self.host)

            if req.status_code is not 200:
                raise requests.ConnectionError("Error loading feed")

            content = """<?xml version="1.0" encoding="UTF-8"?><root>%s</root>""" % req.text.replace('&', '&amp;')
            doc = ET.fromstring(content)

            # Loop through each project
            for table in doc.findall('table'):

                group = None
                for a in table.findall('tr/td/div/a'):
                    if a.attrib.get('class') == 'buildTypeName':
                        group = a.text
                for tr in table.findall('tr'):
                    entry = {
                        'project': None,
                        'build': None,
                        'status': None,
                        'group': group
                    }

                    # loop through each build config
                    for td in tr.findall('td'):
                        # Get success status
                        if td.attrib.get('class') == 'buildConfigurationName':
                            entry['project'] = td.find('a').text
                            entry['status'] = td.find('img').attrib['title']
                        if td.attrib.get('class') == 'buildNumberDate':
                            entry['build'] = td.find('div/a').text

                    # Skip project rows
                    if entry['status'] is None:
                        continue

                    if 'success' in entry['status']:
                        successes.append(entry)
                    elif 'investigating' in entry['status']:
                        investigation.append(entry)
                    else:
                        failures.append(entry)

        except requests.ConnectionError:
            logger.exception("Error polling site")
            investigation.append({
                'project': 'TeamCity',
                'build': '?',
                'group': '?'
                })
        except Exception, e:
            logger.exception('Exception found while loading feeds')
            failures.append({
                'project': '?',
                'build': e,
                'group': '?',
                })

        for success in successes:
            logger.info('Success: %(group)15s : %(project)-30s %(build)s' % success)
        for warning in investigation:
            logger.warning('Investigation: %(group)15s : %(project)-30s %(build)s' % warning)
        for failure in failures:
            logger.error('Failure: %(group)15s : %(project)-30s %(build)s' % failure)

        return successes, investigation, failures
