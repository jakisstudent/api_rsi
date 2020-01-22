import random


def chose_move_recogniction(param):
    if param == 2:
        rpsdict = {'rr': {'r': 0, 'p': 0, 's': 0}, 'rp': {'r': 0, 'p': 0, 's': 0}, 'rs': {'r': 0, 'p': 0, 's': 0},
                   'pr': {'r': 0, 'p': 0, 's': 0}, 'pp': {'r': 0, 'p': 0, 's': 0}, 'ps': {'r': 0, 'p': 0, 's': 0},
                   'sr': {'r': 0, 'p': 0, 's': 0}, 'sp': {'r': 0, 'p': 0, 's': 0}, 'ss': {'r': 0, 'p': 0, 's': 0}}
    else:
        rpsdict = {'rrr': {'r': 0, 'p': 0, 's': 0}, 'rpr': {'r': 0, 'p': 0, 's': 0}, 'rsr': {'r': 0, 'p': 0, 's': 0},
                   'prr': {'r': 0, 'p': 0, 's': 0}, 'ppr': {'r': 0, 'p': 0, 's': 0}, 'psr': {'r': 0, 'p': 0, 's': 0},
                   'srr': {'r': 0, 'p': 0, 's': 0}, 'spr': {'r': 0, 'p': 0, 's': 0}, 'ssr': {'r': 0, 'p': 0, 's': 0},
                   'rrp': {'r': 0, 'p': 0, 's': 0}, 'rpp': {'r': 0, 'p': 0, 's': 0}, 'rsp': {'r': 0, 'p': 0, 's': 0},
                   'prp': {'r': 0, 'p': 0, 's': 0}, 'ppp': {'r': 0, 'p': 0, 's': 0}, 'psp': {'r': 0, 'p': 0, 's': 0},
                   'srp': {'r': 0, 'p': 0, 's': 0}, 'spp': {'r': 0, 'p': 0, 's': 0}, 'ssp': {'r': 0, 'p': 0, 's': 0},
                   'rrs': {'r': 0, 'p': 0, 's': 0}, 'rps': {'r': 0, 'p': 0, 's': 0}, 'rss': {'r': 0, 'p': 0, 's': 0},
                   'prs': {'r': 0, 'p': 0, 's': 0}, 'pps': {'r': 0, 'p': 0, 's': 0}, 'pss': {'r': 0, 'p': 0, 's': 0},
                   'srs': {'r': 0, 'p': 0, 's': 0}, 'sps': {'r': 0, 'p': 0, 's': 0}, 'sss': {'r': 0, 'p': 0, 's': 0}}
    return rpsdict


def who_win(player_move, ai_move):
    if player_move == ai_move:
        return 'remis'
    else:
        if player_move == 'r':
            if ai_move == 's':
                return 'player'
            elif ai_move == 'p':
                return 'ai'
            else:
                return 'error'
        elif player_move == 's':
            if ai_move == 'p':
                return 'player'
            elif ai_move == 'r':
                return 'ai'
            else:
                return 'error'
        elif player_move == 'p':
            if ai_move == 'r':
                return 'player'
            elif ai_move == 's':
                return 'ai'
            else:
                return 'error'
        else:
            return 'error'


class PlaySession:
    session_id = ''
    player_score = 0
    ai_score = 0
    markov_table_chain = {}
    playermoves = ''
    time_to_learn = 0
    param = 2
    move = {'r': 'rock', 'p': 'paper', 's': 'scissors'}
    chaos_counter = 0
    learning_rate = 0

    def __init__(self, session_id, ai_param):
        self.session_id = session_id
        self.param = ai_param
        self.markov_table_chain = chose_move_recogniction(ai_param)

    def play_round(self, player_decision):

        if player_decision in ['r', 'p', 's']:
            if self.time_to_learn < self.param:
                ai_decision = random.choice(['r', 'p', 's'])
                self.playermoves += player_decision
            else:
                # read markov chains and make the best decision
                the_best_move = self.markov_table_chain[self.playermoves]
                r_posibility = the_best_move['r']
                p_posibility = the_best_move['p']
                s_posibility = the_best_move['s']
                if r_posibility == p_posibility == s_posibility:
                    ai_decision = random.choice(['r', 'p', 's'])
                elif r_posibility == max([r_posibility, p_posibility, s_posibility]):
                    ai_decision = 'p'
                elif p_posibility == max([r_posibility, p_posibility, s_posibility]):
                    ai_decision = 's'
                elif s_posibility == max([r_posibility, p_posibility, s_posibility]):
                    ai_decision = 'r'

                # chaos for the every 5th move from start
                self.chaos_counter += 1
                if self.chaos_counter == 5:
                    self.chaos_counter = 0
                    ai_decision = random.choice(['r', 'p', 's'])

                # learning time and upgrade markov chains
                if player_decision == 'r':
                    r_posibility += 1
                    self.markov_table_chain[self.playermoves][player_decision] = r_posibility
                elif player_decision == 'p':
                    p_posibility += 1
                    self.markov_table_chain[self.playermoves][player_decision] = p_posibility
                elif player_decision == 's':
                    s_posibility += 1
                    self.markov_table_chain[self.playermoves][player_decision] = s_posibility

                # move the player move chain
                playermoves = self.playermoves[1:self.param] + player_decision

                # check the same moves in player moves
                the_same_moves = 0
                for i in range(len(playermoves)):
                    if i != 0:
                        if playermoves[i - 1] == playermoves[i]:
                            the_same_moves += 1

                # change the markovs chain if player makes the same moves
                if the_same_moves == self.param:
                    self.markov_table_chain[playermoves]['r'] = 0
                    self.markov_table_chain[playermoves]['s'] = 0
                    self.markov_table_chain[playermoves]['p'] = 0
                    self.markov_table_chain[playermoves][playermoves[playermoves.len - 1]] += 1

                # add 50 learning rate with rand

                steps_to_learn = 50
                if self.learning_rate != steps_to_learn:
                    self.learning_rate += 1
                    value = random.randint(0, steps_to_learn)
                    if steps_to_learn - value > self.learning_rate:
                        ai_decision = random.choice(['r', 'p', 's'])

            self.time_to_learn += 1
            return who_win(player_decision, ai_decision)
