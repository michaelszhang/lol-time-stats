import calendar
from multisummoner import MultiSummoner

server_ids = {
    'BR': 'br1',
    'EUNE': 'eun1',
    'EUW': 'euw1',
    'JP': 'jp1',
    'KR': 'kr',
    'LAN': 'la1',
    'LAS': 'la2',
    'NA': 'na1',
    'OCE': 'oc1',
    'TR': 'tr1',
    'RU': 'ru'}

server_name = input('Select server (BR, ENUE, EUW, JP, KR, LAN, LAS, NA, OCE, RU, TR): ')
summoner_name_string = input('Enter summoner names, separated by spaces: ')
summoner_name_list = summoner_name_string.split()

begin_time_date_string = input('Enter start date (MM-DD-YYYY): ')
begin_time_date = begin_time_date_string.split('-')
begin_time_time_string = input('Enter GMT start time (HH:MM:SS): ')
begin_time_time = begin_time_time_string.split(':')
begin_time = calendar.timegm((int(begin_time_date[2]), int(begin_time_date[0]), int(begin_time_date[1]), \
    int(begin_time_time[0]), int(begin_time_time[1]), int(begin_time_time[2])))*1000

multi_summoner = MultiSummoner(server_ids[server_name], summoner_name_list, begin_time)
multi_summoner.calculate()
print(multi_summoner)