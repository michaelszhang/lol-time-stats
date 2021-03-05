from multisummoner import MultiSummoner

server_list = 'na1'
summoner_name_list = ['tacotrader11', '16815514924', 'phoenixthecat']

multi_summoner = MultiSummoner(server_list, summoner_name_list)
multi_summoner.calculate()
print(multi_summoner)