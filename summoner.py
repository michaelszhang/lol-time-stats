from mode import Mode
from stats import get_account_id_by_name, get_match_by_id, get_matchlist_full_by_id
from tqdm import tqdm

class Summoner:

    def __init__(self, server, summoner_name):
        self.server = server
        self.name = summoner_name
        self.account_id = get_account_id_by_name(server, summoner_name)
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
        s = '-'*36 + '\n'
        s += '{:<16s}{:>8s}{:>12s}'.format('Mode', 'Games', 'Seconds') + '\n'
        s += '-'*36 + '\n'
        for key in self.modes:
            s += str(self.modes[key]) + '\n'
        s += '-'*36 + '\n'
        s += '{:<16s}{:>8d}{:>12d}'.format(self.name, self.num_games, self.total_time) + '\n'
        s += '-'*36
        return s
    
    def calculate(self):
        matchlist = get_matchlist_full_by_id(self.server, self.account_id)
        for i in tqdm(range(len(matchlist))):
            match = get_match_by_id(self.server, matchlist[i]['gameId'])
            self.modes[match['queueId']].match_update(match)
        for key in self.modes:
            self.num_games += self.modes[key].num_games
            self.total_time += self.modes[key].total_time