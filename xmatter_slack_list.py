'''
Written by Erick Capote
'''
import os
import logging
import requests
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from slackclient import SlackClient


def setup_custom_logger(name):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    LOG_FILENAME = os.path.join(__location__, 'platops-ad.log')
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler(LOG_FILENAME, mode='a')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


SLACK_TOKEN = "XXXXXXXXXXXXX" # or a TEST token. Get one from https://api.slack.com/docs/oauth-test-tokens
slack_client = SlackClient(SLACK_TOKEN)
count = 0
base_URL = 'XMATTER_URL_API'
url = base_URL + '/groups/<XMATTER_GROUP_ID>/calendar'
my_channel = '#SLACKCHANNELNAME'

# Instantiate Logger
logger = setup_custom_logger('snow-niraj')

logger.info('**************START RUN**********************\n')

response = requests.get(url, auth=HTTPBasicAuth('erick.capote', 'Sp@rky2Bl0nd!3'))
json_response = response.json()

if (response.status_code == 200):
    json = response.json();
    for d in json['data']:
        for md in d['members']['data']:
            count += 1
            if count == 1:
                api_call = slack_client.api_call("chat.postMessage",
                  channel=my_channel,
                  text='PlatOps.AD call List for this week: Engineer # %s is: %s' % (count, md['member']['targetName']))
                logger.info(api_call)
            else:
                api_call = slack_client.api_call("chat.postMessage",
                                                 channel=my_channel,
                                                 text='Call List for this week: Escalation Engineers: %s' % (md['member']['targetName']))
                logger.info(api_call)

logger.info('**************END RUN**********************\n')


