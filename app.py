from multisummoner import MultiSummoner

server = 'na1'
summoner_name_string = input('Enter summoner names, separated by spaces: ')
summoner_name_list = summoner_name_string.split()

multi_summoner = MultiSummoner(server, summoner_name_list)
multi_summoner.calculate()
print(multi_summoner)