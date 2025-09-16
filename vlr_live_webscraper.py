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
    liveElement = tree.xpath('//a[contains(@class, "match-item") and div[contains(@class, "match-item-eta")]/div/div/text()="LIVE"]')
    return len(liveElement) > 0

    # for element in liveElement[:10]:
    #     print(element.text_content().strip())

print("is live match?", is_live_match())