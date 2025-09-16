import requests
from lxml import html
from functools import partial
from mac_notifications import client

match_url = 'https://www.vlr.gg/matches'

response = requests.get(match_url)
tree = html.fromstring(response.content)



# Extract 10 upcoming matches
# matches = tree.xpath('//a[contains(@class, "match-item")]/@href')
# matchesnode = tree.xpath('//a[contains(@class, "match-item")]//div/node()')

# for match in matches:
#     print(match.strip())


# Checks if there is a live match going on
def is_live_match():
    liveElement = tree.xpath('//div[contains(@class, "ml-status") and contains(text(), "LIVE")]')
    parentLiveElement = tree.xpath('..//div[contains(@class, "ml-status") and contains(text(), "LIVE")]')
    for element in liveElement:
        print(element.text_content().strip())

is_live_match()