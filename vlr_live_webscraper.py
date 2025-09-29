import requests
from lxml import html
from functools import partial
from mac_notifications import client
import pync
import time




# Extract 10 upcoming matches
# matches = tree.xpath('//a[contains(@class, "match-item")]/@href')
# matchesnode = tree.xpath('//a[contains(@class, "match-item")]//div/node()')

# for match in matches:
#     print(match.strip())


# Checks if there is a live match going on
def get_live_match(tree):
    liveElement = tree.xpath('//a[contains(@class, "match-item") and div[contains(@class, "match-item-eta")]/div/div/text()="LIVE"]')

    # Currently looks for "upcoming" for testing, change to "LIVE" when needed
    href = tree.xpath('//a[contains(@class, "match-item") and div[contains(@class, "match-item-eta")]/div/div/text()="LIVE"]/@href')
    for link in href:
        print("Live match link:", link)

    # if not href:
    #     client.send_notification("No live matches currently.", "VLR.gg Live Match Notifier", sound="Ping")

    return href[0] if href else None


def get_score(link, isLive):
    match_url = 'https://www.vlr.gg' + link
    # Test different matches
    # match_url = 'https://www.vlr.gg/418817/detonation-focusme-vs-paper-rex-valorant-radiant-asia-invitational-gf'
    live_match_response = requests.get(match_url)
    live_match_tree = html.fromstring(live_match_response.content)

    match_score = live_match_tree.xpath('//div[contains(@class, "match-header-vs")]//text()')
   
    match_score_content = []
    for content in match_score:
        if content.strip() != "":
            match_score_content.append(content.strip())
    
    first_team = match_score_content[0]
    second_team = match_score_content[7]
    first_team_score = match_score_content[2]
    second_team_score = match_score_content[4]

    print(f"{first_team} {first_team_score} - {second_team_score} {second_team}")
    score = f"{first_team} {first_team_score} - {second_team_score} {second_team}"

    match_rounds = live_match_tree.xpath('//div[@class="vm-stats-game-header"]//div[contains(@class, "score")]//text()')
    maps_played = live_match_tree.xpath('//div[@class="vm-stats-game-header"]//div[@class="map"]//span/text()')
    
    # counter used to determine 
    counter = 0
    map_score = []
    all_map_scores = []
    for round_score in match_rounds:
        map_score.append(round_score)                        
        counter += 1
        
        if counter == 2:
            all_map_scores.append(map_score.copy())
            map_score.clear()
            counter = 0
        
                                            
    print(all_map_scores)

    
    maps = []
    for map in maps_played:
        if map.strip() != "" and map.strip() != "PICK":
            maps.append(map.strip())
    print(maps)

    return score, all_map_scores, maps


def get_match():
    match_url = 'https://www.vlr.gg/matches'

    response = requests.get(match_url)
    tree = html.fromstring(response.content)

    live_score = ""
    live_map_scores = []
    live_maps = []
    link = get_live_match(tree)
    if link:
        # If match is live, it automatically goes to currently played map
        live_score, live_map_scores, live_maps = get_score(link, True)

        live_text = live_score + '\n' + ", ".join(str(x) for x in live_maps) + '\n' + ", ".join(str(x) for x in live_map_scores)
        pync.notify(
            live_text,
            title='🔴 LIVE Match 🔴',
            sender="org.sidhantdash.VlrLiveWebscraper12")
        time.sleep(10)
        
        # match_rounds = live_match_tree.xpath('//div[contains(@class, "vm-stats-game mod-active")]//text()')
        # match_rounds = live_match_tree.xpath('//div[@class="vm-stats-game mod-active"]//text()')
        # for content in match_rounds:
        #     if content.strip() != "":
        #         print(content.strip())
    else:
        print("No live matches currently.")
    def get_past_match(match_index):
        results_url = 'https://www.vlr.gg/matches/results'
        results_response = requests.get(results_url)
        results_tree = html.fromstring(results_response.content)
        recent_match = results_tree.xpath('//a[contains(@class, "match-item")]/@href')
        past_score, past_map_scores, past_maps = get_score(recent_match[match_index], False)
        past_text = past_score + '\n' + ", ".join(str(x) for x in past_maps) + '\n' + ", ".join(str(x) for x in past_map_scores)
        pync.notify(
            past_text,
            title='🟦 Past Match 🟦',
            sender="org.sidhantdash.VlrLiveWebscraper12")
        time.sleep(5)
    get_past_match(0)
    get_past_match(1)

if __name__ == "__main__":
    get_match()
    # client.create_notification(title="Meeting starts now!", subtitle="Team Standup")
    # if live_score != "":

    #     live_text = live_score + '\n'
    #     pync.notify(
    #         live_score,
    #         title='🔴 LIVE Match 🔴',
    #         sender="org.sidhantdash.VlrLiveWebscraper12")
    
    