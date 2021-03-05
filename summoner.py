from mode import Mode
from stats import get_account_id_by_name, get_summoner_id_by_name, get_name_by_summoner_id, get_match_by_id, get_matchlist_full_by_id
from tqdm import tqdm

class Summoner:

    def __init__(self, server, summoner_name):
        self.server = server
        self.name = summoner_name
        self.account_id = get_account_id_by_name(server, summoner_name)
        self.summoner_id = get_summoner_id_by_name(server, summoner_name)
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
        rows = len(self.modes) + 6
        colsep = ' | '
        col1 = ['-'*36, '{:<16s}{:>8s}{:>12s}'.format('Mode', 'Games', 'Seconds'), '-'*36]
        for key in self.modes:
            col1.append(str(self.modes[key]))
        col1 += ['-'*36, '{:<16s}{:>8d}{:>12d}'.format(self.name, self.num_games, self.total_time), '-'*36]
        col2 = ['-'*36, '{:<16s}{:>8s}{:>12s}'.format('Played With', 'Games', 'Seconds'), '-'*36]
        for i in range(rows-4):
            if i >= len(self.played_with_list):
                col2.append("")
            else:
                col2.append('{:<16s}{:>8d}{:>12d}'.format(get_name_by_summoner_id(self.server, self.played_with_list[i][2]), self.played_with_list[i][0], self.played_with_list[i][1]))
        col2.append('-'*36)
        s = ""
        for i in range(rows):
            s += col1[i] + colsep + col2[i]
            if i != rows - 1:
                s += '\n'
        return s
    
    def match_update(self, match):
        self.modes[match['queueId']].match_update(match)
        self.num_games += 1
        self.total_time += match['gameDuration']
        part_id_to_summ_id = {participant_identity['participantId']: participant_identity['player']['summonerId'] for participant_identity in match['participantIdentities']}
        summ_id_to_side = {part_id_to_summ_id[participant['participantId']]: participant['teamId'] for participant in match['participants']}
        for summoner_id in summ_id_to_side:
            if summoner_id != self.summoner_id and summ_id_to_side[summoner_id] == summ_id_to_side[self.summoner_id]:
                if summoner_id not in self.played_with:
                    self.played_with[summoner_id] = [0, 0]
                self.played_with[summoner_id][0] += 1
                self.played_with[summoner_id][1] += match['gameDuration']
    
    def calculate(self):
        matchlist = get_matchlist_full_by_id(self.server, self.account_id)
        for i in tqdm(range(len(matchlist))):
            match = get_match_by_id(self.server, matchlist[i]['gameId'])
            self.match_update(match)
        for key in self.played_with:
            self.played_with_list.append((self.played_with[key][0], self.played_with[key][1], key))
            self.played_with_list.sort(reverse=True)