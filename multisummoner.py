from mode import Mode
from stats import get_name_by_summoner_id
from summoner import Summoner

class MultiSummoner:

    def __init__(self, server, summoner_name_list):
        self.server = server
        self.summoner_list = [Summoner(server, summoner_name_list[i]) for i in range(len(summoner_name_list))]
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
        self.played_with = {}
        self.played_with_list = []
    
    def __str__(self):
        s = ""
        for summoner in self.summoner_list:
            s += str(summoner) + '\n'
        rows = len(self.modes) + 6
        colsep = ' | '
        col1 = ['-'*36, '{:<16s}{:>8s}{:>12s}'.format('Mode', 'Games', 'Seconds'), '-'*36]
        for key in self.modes:
            col1.append(str(self.modes[key]))
        col1 += ['-'*36, '{:<16s}{:>8d}{:>12d}'.format('total (' + str(len(self.summoner_list)) + ' accts)', self.num_games, self.total_time), '-'*36]
        col2 = ['-'*36, '{:<16s}{:>8s}{:>12s}'.format('Played With', 'Games', 'Seconds'), '-'*36]
        for i in range(rows-4):
            if i >= len(self.played_with_list):
                col2.append("")
            else:
                col2.append('{:<16s}{:>8d}{:>12d}'.format(get_name_by_summoner_id(self.server, self.played_with_list[i][2]), self.played_with_list[i][0], self.played_with_list[i][1]))
        col2.append('-'*36)
        for i in range(rows):
            s += col1[i] + colsep + col2[i]
            if i != rows - 1:
                s += '\n'
        return s

    def summoner_update(self, summoner):
        self.num_games += summoner.num_games
        self.total_time += summoner.total_time
        for key in self.modes:
            self.modes[key].num_games += summoner.modes[key].num_games
            self.modes[key].total_time += summoner.modes[key].total_time
        for summoner_id in summoner.played_with:
            if summoner_id not in self.played_with:
                self.played_with[summoner_id] = [0, 0]
            self.played_with[summoner_id][0] += summoner.played_with[summoner_id][0]
            self.played_with[summoner_id][1] += summoner.played_with[summoner_id][1]

    def calculate(self):
        for summoner in self.summoner_list:
            summoner.calculate()
            self.summoner_update(summoner)
        for key in self.played_with:
            self.played_with_list.append((self.played_with[key][0], self.played_with[key][1], key))
            self.played_with_list.sort(reverse=True)