from summoner import Summoner

server = 'na1'
summoner_name = 'tacotrader11'

summoner = Summoner(server, summoner_name)
summoner.calculate()
print(summoner)