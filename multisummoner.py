from mode import Mode
from summoner import Summoner

class MultiSummoner:

    def __init__(self, server_list, summoner_name_list):
        assert(len(server_list) == len(summoner_name_list))
        self.summoner_list = [Summoner(server_list[i], summoner_name_list[i]) for i in range(len(summoner_name_list))]
        self.num_games = 0
        self.total_time = 0
        self.modes = {
            400: Mode('Normal Draft'),
            420: Mode('Ranked Solo/Duo'),
            430: Mode('Normal Blind'),
            440: Mode('Ranked Flex'),
            450: Mode('ARAM'),
            700: Mode('Clash'),
            900: Mode('URF'),
            1020: Mode('One For All'),
            1300: Mode('Nexus Blitz')
        }
    
    def __str__(self):
        s = ""
        for summoner in self.summoner_list:
            s += str(summoner) + '\n'
        s += '-'*36 + '\n'
        s += '{:<16s}{:>8s}{:>12s}'.format('Mode', 'Games', 'Seconds') + '\n'
        s += '-'*36 + '\n'
        for key in self.modes:
            s += str(self.modes[key]) + '\n'
        s += '-'*36 + '\n'
        s += '{:<16s}{:>8d}{:>12d}'.format('total ('+str(len(self.summoner_list))+' accts)', self.num_games, self.total_time) + '\n'
        s += '-'*36
        return s

    def summoner_update(self, summoner):
        self.num_games += summoner.num_games
        self.total_time += summoner.total_time
        for key in self.modes:
            self.modes[key].num_games += summoner.modes[key].num_games
            self.modes[key].total_time += summoner.modes[key].total_time

    def calculate(self):
        for summoner in self.summoner_list:
            summoner.calculate()
            self.summoner_update(summoner)