import calendar
import requests
import os
import time
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

API_KEY = os.getenv("API_KEY")
QUEUE_IDS = [400, 420, 430, 440, 450, 700, 900, 1020, 1300] # normal draft, ranked solo/duo, normal blind, ranked flex, aram, clash, urf, one for all, nexus blitz
SEASON_START_TIME = { 'na1': calendar.timegm((2021, 1, 8, 12, 0, 0))*1000 }

class APIException(Exception):
    pass

def make_get_request(request_url, error_message):
    response = None

    while response == None or response.status_code == 429 or response.status_code // 100 == 5:
        response = requests.get(request_url)
        time.sleep(1.2) # rate limit
        if response.status_code == 200:
            continue
        elif response.status_code == 429:
            time.sleep(response.headers["Retry-After"])
        elif response.status_code // 100 == 5:
            continue
        else:
            raise APIException(error_message + ' | ' + str(response.status_code))

    return response

def get_api_domain(server):
    return 'https://' + server + '.api.riotgames.com'

def get_api_key_query():
    return '?api_key=' + API_KEY

def get_account_id_by_name(server, summoner_name):
    request_url = get_api_domain(server) + '/lol/summoner/v4/summoners/by-name/' + summoner_name + get_api_key_query()

    response = make_get_request(request_url, 'summoner_name: ' + summoner_name)

    return response.json()['accountId']

def get_match_by_id(server, match_id):
    request_url = get_api_domain(server) + '/lol/match/v4/matches/' + str(match_id) + get_api_key_query()

    response = make_get_request(request_url, 'match_id: ' + str(match_id))

    return response.json()

def get_matchlist_page_by_id(server, account_id, begin_index, end_index):
    queue_query = ''
    for queue_id in QUEUE_IDS:
        queue_query += '&queue=' + str(queue_id)

    begin_time_query = '&beginTime=' + str(SEASON_START_TIME[server])
    begin_index_query = '&beginIndex=' + str(begin_index)
    end_index_query = '&endIndex=' + str(end_index)
    request_url = get_api_domain(server) + '/lol/match/v4/matchlists/by-account/' + account_id + get_api_key_query() \
        + queue_query + begin_time_query + begin_index_query + end_index_query
    
    response = make_get_request(request_url, 'account_id: ' + account_id)

    return response.json()['matches']

def get_matchlist_full_by_id(server, account_id):
    matchlist = []
    matchlist_page = None
    page_index = 0

    while matchlist_page == None or len(matchlist_page) == 100:
        matchlist_page = get_matchlist_page_by_id(server, account_id, page_index*100, (page_index+1)*100)
        matchlist += matchlist_page
        page_index += 1
    
    return matchlist

def calculate_total_time(server, summoner_name):
    account_id = get_account_id_by_name(server, summoner_name)
    matchlist = get_matchlist_full_by_id(server, account_id)

    total_time = 0
    for i in tqdm(range(len(matchlist))):
        total_time += get_match_by_id('na1', matchlist[i]['gameId'])['gameDuration']

    return total_time

server = 'na1'
summoner_name = 'tacotrader11'
print(calculate_total_time(server, summoner_name))