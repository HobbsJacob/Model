import json
import os


class Team:
    def __init__(self, n):
        self.name = n
        self.previousStats = {}         # Dict

    def printStats(self):
        out = ""
        for key,val in self.previousStats.items():
            out += str(val) + ","

        return out[:-1]

    def updateValues(self, data):

        if self.previousStats == {}:
            for stat in data:
                for key, val in stat["@attributes"].items():
                    if key != "points":
                        self.previousStats[key] = float(val)

            return

        for stat in data:
            for key,val in stat["@attributes"].items():
                if key != "points":
                    self.previousStats[key] = (self.previousStats[key] * 0.2) + (float(val) * 0.8)



    # def calc roll off?

    # def print?


# conceded, name, home/a

allTeams = {}
allTeams["Lions"] = Team("Lions")
allTeams["Highlanders"] = Team("Highlanders")
allTeams["Reds"] = Team("Reds")
allTeams["Bulls"] = Team("Bulls")
allTeams["Hurricanes"] = Team("Hurricanes")
allTeams["Chiefs"] = Team("Chiefs")
allTeams["Rebels"] = Team("Rebels")
allTeams["Jaguares"] = Team("Jaguares")
allTeams["Waratahs"] = Team("Waratahs")
allTeams["Stormers"] = Team("Stormers")
allTeams["Sharks"] = Team("Sharks")
allTeams["Blues"] = Team("Blues")
allTeams["Sunwolves"] = Team("Sunwolves")
allTeams["Crusaders"] = Team("Crusaders")
allTeams["Brumbies"] = Team("Brumbies")

def parse_file(name):
    with open(os.path.join("datas", name)) as file:

        text = file.read()

        text = text[:-1]
        text = text[11:]
        text = text.replace("NSW Waratahs", "Waratahs")
        if "Force" in text or "Cheetahs" in text or "Kings" in text:
            return


        j = json.loads(text)
        line = ""
        try:
            if allTeams[j["RRML"]["TeamDetail"]["Team"][0]["@attributes"]["team_name"]].previousStats == {}:
                allTeams[j["RRML"]["TeamDetail"]["Team"][0]["@attributes"]["team_name"]].updateValues(
                    j["RRML"]["TeamDetail"]["Team"][0]["TeamStats"]["TeamStat"])
            if allTeams[j["RRML"]["TeamDetail"]["Team"][1]["@attributes"]["team_name"]].previousStats == {}:
                allTeams[j["RRML"]["TeamDetail"]["Team"][1]["@attributes"]["team_name"]].updateValues(
                    j["RRML"]["TeamDetail"]["Team"][1]["TeamStats"]["TeamStat"])
        except:
            print(name)



        line += j["RRML"]["TeamDetail"]["Team"][0]["@attributes"]["team_name"] + ","
        line += j["RRML"]["TeamDetail"]["Team"][0]["@attributes"]["home_or_away"] + ","

        line += allTeams[j["RRML"]["TeamDetail"]["Team"][0]["@attributes"]["team_name"]].printStats() + ","
        line += allTeams[j["RRML"]["TeamDetail"]["Team"][1]["@attributes"]["team_name"]].printStats() + ","


        line += j["RRML"]["@attributes"]["venue"].replace(",", "") + ","
        try:
            for off in j["RRML"]["Officials"]["Official"]:
                if off["@attributes"]["role"] == "referee":
                    line += off["@attributes"]["country"].replace(",", "") + ","
        except:
            line += "?,"
            print(name)

        if j["RRML"]["TeamDetail"]["Team"][0]["@attributes"]["home_or_away"] == "home":
            line += j["RRML"]["@attributes"]["away_score"]
        else:
            line += j["RRML"]["@attributes"]["home_score"]

        outfile.write(line + "\n")
        line = ""

        line += j["RRML"]["TeamDetail"]["Team"][1]["@attributes"]["team_name"] + ","
        line += j["RRML"]["TeamDetail"]["Team"][1]["@attributes"]["home_or_away"] + ","

        line += allTeams[j["RRML"]["TeamDetail"]["Team"][1]["@attributes"]["team_name"]].printStats() + ","
        line += allTeams[j["RRML"]["TeamDetail"]["Team"][0]["@attributes"]["team_name"]].printStats() + ","

        line += j["RRML"]["@attributes"]["venue"].replace(",", "") + ","

        try:
            for off in j["RRML"]["Officials"]["Official"]:
                if off["@attributes"]["role"] == "referee":
                    line += off["@attributes"]["country"].replace(",", "") + ","
        except:
            line += "?,"
            print(name)

        if j["RRML"]["TeamDetail"]["Team"][0]["@attributes"]["home_or_away"] == "home":
            line += j["RRML"]["@attributes"]["away_score"]
        else:
            line += j["RRML"]["@attributes"]["home_score"]

        # if j["RRML"]["TeamDetail"]["Team"][1]["@attributes"]["home_or_away"] == "home":
        #     if j["RRML"]["@attributes"]["away_score"] >= j["RRML"]["@attributes"]["home_score"]:
        #         line += "LOSS"
        #     else:
        #         line += "WIN"
        # else:
        #     if j["RRML"]["@attributes"]["away_score"] <= j["RRML"]["@attributes"]["home_score"]:
        #         line += "LOSS"
        #     else:
        #         line += "WIN"

        outfile.write(line + "\n")

        allTeams[j["RRML"]["TeamDetail"]["Team"][0]["@attributes"]["team_name"]].updateValues(
            j["RRML"]["TeamDetail"]["Team"][0]["TeamStats"]["TeamStat"])

        allTeams[j["RRML"]["TeamDetail"]["Team"][1]["@attributes"]["team_name"]].updateValues(
            j["RRML"]["TeamDetail"]["Team"][1]["TeamStats"]["TeamStat"])

with open("out.csv", "w") as outfile:

    outfile.write("team_name,h/a,restart_opp_player_a,kick_oppn_collection_a,kicks_from_hand_a,free_kick_conceded_at_lineout_a,penalty_conceded_killing_ruck_a,penalty_conceded_own_half_a,kick_penalty_good_a,lineouts_won_a,scrums_success_a,rucks_won_a,metres_a,scrums_lost_reversed_a,tries_a,lineouts_infringe_opp_a,scrums_won_penalty_try_a,turnover_turnover_forward_pass_a,scrums_won_free_kick_a,scrums_won_pushover_try_a,turnover_own_half_a,missed_tackles_a,scrums_lost_outright_a,collection_loose_ball_a,restart_error_not_ten_a,scrums_lost_penalty_a,missed_conversion_goals_a,total_free_kicks_conceded_a,pc_kick_percent_a,lineouts_to_opp_player_a,rucks_total_a,restarts_lost_a,lineouts_infringe_own_a,missed_goals_a,lineout_won_steal_a,penalty_conceded_foul_play_a,penalty_goals_a,lineout_throw_lost_handling_error_a,free_kick_conceded_a,kick_penalty_bad_a,kick_percent_success_a,lineout_throw_won_clean_a,restart_opp_error_a,drop_goals_converted_a,kick_success_a,scrums_won_a,penalty_tries_a,free_kick_conceded_in_general_play_a,conversion_goals_a,clean_breaks_a,mauls_won_outright_a,collection_failed_a,kick_in_touch_a,carries_support_a,kick_possession_retained_a,scrums_lost_free_kick_a,id_a,penalty_conceded_dissent_a,defenders_beaten_a,penalty_conceded_lineout_offence_a,scrums_won_penalty_a,collection_from_kick_a,restart_own_player_a,penalty_conceded_collapsing_maul_a,lineout_success_a,penalty_conceded_offside_a,collection_success_a,kicking_competition_goals_a,drop_goal_missed_a,turnover_carried_in_touch_a,kick_from_hand_metres_a,restarts_success_a,rucks_lost_a,turnover_bad_pass_a,penalty_kick_for_touch_metres_a,mauls_won_try_a,penalty_conceded_collapsing_a,turnover_carried_over_a,lineout_throw_won_tap_a,scrums_won_outright_a,turnover_lost_in_ruck_or_maul_a,tackle_success_a,lineout_throw_not_straight_a,kick_out_of_play_a,kick_possession_lost_a,carries_not_made_gain_line_a,missed_penalty_goals_a,yellow_cards_a,offload_a,retained_kicks_a,passes_a,penalty_conceded_delib_knock_on_a,carries_crossed_gain_line_a,lineouts_to_own_player_a,team_id_a,penalty_conceded_opp_half_a,restart_halfway_a,lineouts_Lost_a,lineout_throw_lost_free_kick_a,mauls_won_a,penalty_conceded_other_a,turnover_forward_pass_a,penalty_conceded_scrum_offence_a,tackles_a,lineout_throw_lost_not_straight_a,free_kick_conceded_in_ruck_or_maul_a,try_kicks_a,turnovers_won_a,mauls_lost_turnover_a,penalties_conceded_a,mauls_won_penalty_a,scrums_lost_a,mauls_won_penalty_try_a,lineout_won_own_throw_a,total_kicks_a,scrums_reset_a,restart_22m_a,lineout_throw_lost_outright_a,mauls_lost_outright_a,mauls_lost_a,penalty_conceded_collapsing_offence_a,turnover_opp_half_a,turnover_knock_on_a,turnover_won_a,game_id_a,penalty_conceded_obstruction_a,penalty_conceded_stamping_a,turnover_kick_error_a,restart_error_out_of_play_a,set_piece_won_a,collection_interception_a,penalty_conceded_handling_in_ruck_a,try_assists_a,scrums_total_a,penalty_conceded_early_tackle_a,mauls_total_a,lineout_throw_lost_penalty_a,ruck_success_a,carries_metres_a,true_retained_kicks_a,kick_try_scored_a,turnovers_conceded_a,free_kick_conceded_at_scrum_a,red_card_second_yellow_a,red_cards_a,kick_touch_in_goal_a,kick_charged_down_a,penalty_conceded_wrong_side_a,lineout_throw_won_penalty_a,total_lineouts_a,total_kicks_succeeded_a,lineout_throw_won_free_kick_a,mauling_metres_a,restarts_won_a,runs_a,goals_a,penalty_conceded_high_tackle_a,possession_a,pc_possession_first_a,pc_possession_second_a,territory_a,pc_territory_first_a,pc_territory_second_a,ball_won_zone_a_a,ball_won_zone_b_a,ball_won_zone_c_a,ball_won_zone_d_a,attacking_events_zone_a_a,attacking_events_zone_b_a,attacking_events_zone_c_a,attacking_events_zone_d_a,ball_possession_last_10_mins_a,territory_last_10_mins_a,restart_opp_player_b,kick_oppn_collection_b,kicks_from_hand_b,free_kick_conceded_at_lineout_b,penalty_conceded_killing_ruck_b,penalty_conceded_own_half_b,kick_penalty_good_b,lineouts_won_b,scrums_success_b,rucks_won_b,metres_b,scrums_lost_reversed_b,tries_b,lineouts_infringe_opp_b,scrums_won_penalty_try_b,turnover_turnover_forward_pass_b,scrums_won_free_kick_b,scrums_won_pushover_try_b,turnover_own_half_b,missed_tackles_b,scrums_lost_outright_b,collection_loose_ball_b,restart_error_not_ten_b,scrums_lost_penalty_b,missed_conversion_goals_b,total_free_kicks_conceded_b,pc_kick_percent_b,lineouts_to_opp_player_b,rucks_total_b,restarts_lost_b,lineouts_infringe_own_b,missed_goals_b,lineout_won_steal_b,penalty_conceded_foul_play_b,penalty_goals_b,lineout_throw_lost_handling_error_b,free_kick_conceded_b,kick_penalty_bad_b,kick_percent_success_b,lineout_throw_won_clean_b,restart_opp_error_b,drop_goals_converted_b,kick_success_b,scrums_won_b,penalty_tries_b,free_kick_conceded_in_general_play_b,conversion_goals_b,clean_breaks_b,mauls_won_outright_b,collection_failed_b,kick_in_touch_b,carries_support_b,kick_possession_retained_b,scrums_lost_free_kick_b,id_b,penalty_conceded_dissent_b,defenders_beaten_b,penalty_conceded_lineout_offence_b,scrums_won_penalty_b,collection_from_kick_b,restart_own_player_b,penalty_conceded_collapsing_maul_b,lineout_success_b,penalty_conceded_offside_b,collection_success_b,kicking_competition_goals_b,drop_goal_missed_b,turnover_carried_in_touch_b,kick_from_hand_metres_b,restarts_success_b,rucks_lost_b,turnover_bad_pass_b,penalty_kick_for_touch_metres_b,mauls_won_try_b,penalty_conceded_collapsing_b,turnover_carried_over_b,lineout_throw_won_tap_b,scrums_won_outright_b,turnover_lost_in_ruck_or_maul_b,tackle_success_b,lineout_throw_not_straight_b,kick_out_of_play_b,kick_possession_lost_b,carries_not_made_gain_line_b,missed_penalty_goals_b,yellow_cards_b,offload_b,retained_kicks_b,passes_b,penalty_conceded_delib_knock_on_b,carries_crossed_gain_line_b,lineouts_to_own_player_b,team_id_b,penalty_conceded_opp_half_b,restart_halfway_b,lineouts_Lost_b,lineout_throw_lost_free_kick_b,mauls_won_b,penalty_conceded_other_b,turnover_forward_pass_b,penalty_conceded_scrum_offence_b,tackles_b,lineout_throw_lost_not_straight_b,free_kick_conceded_in_ruck_or_maul_b,try_kicks_b,turnovers_won_b,mauls_lost_turnover_b,penalties_conceded_b,mauls_won_penalty_b,scrums_lost_b,mauls_won_penalty_try_b,lineout_won_own_throw_b,total_kicks_b,scrums_reset_b,restart_22m_b,lineout_throw_lost_outright_b,mauls_lost_outright_b,mauls_lost_b,penalty_conceded_collapsing_offence_b,turnover_opp_half_b,turnover_knock_on_b,turnover_won_b,game_id_b,penalty_conceded_obstruction_b,penalty_conceded_stamping_b,turnover_kick_error_b,restart_error_out_of_play_b,set_piece_won_b,collection_interception_b,penalty_conceded_handling_in_ruck_b,try_assists_b,scrums_total_b,penalty_conceded_early_tackle_b,mauls_total_b,lineout_throw_lost_penalty_b,ruck_success_b,carries_metres_b,true_retained_kicks_b,kick_try_scored_b,turnovers_conceded_b,free_kick_conceded_at_scrum_b,red_card_second_yellow_b,red_cards_b,kick_touch_in_goal_b,kick_charged_down_b,penalty_conceded_wrong_side_b,lineout_throw_won_penalty_b,total_lineouts_b,total_kicks_succeeded_b,lineout_throw_won_free_kick_b,mauling_metres_b,restarts_won_b,runs_b,goals_b,penalty_conceded_high_tackle_b,possession_b,pc_possession_first_b,pc_possession_second_b,territory_b,pc_territory_first_b,pc_territory_second_b,ball_won_zone_a_b,ball_won_zone_b_b,ball_won_zone_c_b,ball_won_zone_d_b,attacking_events_zone_a_b,attacking_events_zone_b_b,attacking_events_zone_c_b,attacking_events_zone_d_b,ball_possession_last_10_mins_b,territory_last_10_mins_b,venue,ref,conceded")
    outfile.write("\n")

    for path in os.listdir("datas"):
        parse_file(path)








# for item in os.listdir("datas"):
#    with open(os.path.join("datas", item), "r"):
#




# RRML
#     Events
#         Event[]
#             @attributes
#                 minute
#                 period
#                 player_id
#                 second
#                 team_id
#                 type
#     Officials
#         Official[]
#             @value
#             @attributes
#                 id
#                 country
#                 official_name
#                 role
#     TeamDetail
#         Team[]     each team
#             Player[]        each player in the team
#                 PlayerStats{}
#                     PlayerStat[]        Their stats
#                         @value     blank
#                         @attributes
#                             "stat name":value
#                 @attributes
#                     id
#                     player_name
#                     position
#                     position_id
#             TeamStats
#                 TeamStat[]
#                     @value    blank
#                     @attributes
#                         "stat name":value
#             @attributes
#                 home_or_away
#                 team_id
#                 team_name
#     @attributes

#TEAM SPECIFIC

# restart_opp_player
# kick_oppn_collection
# kicks_from_hand
# free_kick_conceded_at_lineout
# penalty_conceded_killing_ruck
# penalty_conceded_own_half
# kick_penalty_good
# lineouts_won
# scrums_success
# rucks_won
# metres
# scrums_lost_reversed
# tries
# lineouts_infringe_opp
# scrums_won_penalty_try
# turnover_turnover_forward_pass
# scrums_won_free_kick
# scrums_won_pushover_try
# turnover_own_half
# missed_tackles
# scrums_lost_outright
# collection_loose_ball
# restart_error_not_ten
# scrums_lost_penalty
# missed_conversion_goals
# total_free_kicks_conceded
# pc_kick_percent
# lineouts_to_opp_player
# rucks_total
# restarts_lost
# lineouts_infringe_own
# missed_goals
# lineout_won_steal
# penalty_conceded_foul_play
# penalty_goals
# lineout_throw_lost_handling_error
# free_kick_conceded
# kick_penalty_bad
# kick_percent_success
# lineout_throw_won_clean
# restart_opp_error
# drop_goals_converted
# kick_success
# scrums_won
# penalty_tries
# free_kick_conceded_in_general_play
# conversion_goals
# points
# clean_breaks
# mauls_won_outright
# collection_failed
# kick_in_touch
# carries_support
# kick_possession_retained
# scrums_lost_free_kick
# id
# penalty_conceded_dissent
# defenders_beaten
# penalty_conceded_lineout_offence
# scrums_won_penalty
# collection_from_kick
# restart_own_player
# penalty_conceded_collapsing_maul
# lineout_success
# penalty_conceded_offside
# collection_success
# kicking_competition_goals
# drop_goal_missed
# turnover_carried_in_touch
# kick_from_hand_metres
# restarts_success
# rucks_lost
# turnover_bad_pass
# penalty_kick_for_touch_metres
# mauls_won_try
# penalty_conceded_collapsing
# turnover_carried_over
# lineout_throw_won_tap
# scrums_won_outright
# turnover_lost_in_ruck_or_maul
# tackle_success
# lineout_throw_not_straight
# kick_out_of_play
# kick_possession_lost
# carries_not_made_gain_line
# missed_penalty_goals
# yellow_cards
# offload
# retained_kicks
# passes
# penalty_conceded_delib_knock_on
# carries_crossed_gain_line
# lineouts_to_own_player
# team_id
# penalty_conceded_opp_half
# restart_halfway
# lineouts_Lost
# lineout_throw_lost_free_kick
# mauls_won
# penalty_conceded_other
# turnover_forward_pass
# penalty_conceded_scrum_offence
# tackles
# lineout_throw_lost_not_straight
# free_kick_conceded_in_ruck_or_maul
# try_kicks
# turnovers_won
# mauls_lost_turnover
# penalties_conceded
# mauls_won_penalty
# scrums_lost
# mauls_won_penalty_try
# lineout_won_own_throw
# total_kicks
# scrums_reset
# restart_22m
# lineout_throw_lost_outright
# mauls_lost_outright
# mauls_lost
# penalty_conceded_collapsing_offence
# turnover_opp_half
# turnover_knock_on
# turnover_won
# game_id
# penalty_conceded_obstruction
# penalty_conceded_stamping
# turnover_kick_error
# restart_error_out_of_play
# set_piece_won
# collection_interception
# penalty_conceded_handling_in_ruck
# try_assists
# scrums_total
# penalty_conceded_early_tackle
# mauls_total
# lineout_throw_lost_penalty
# ruck_success
# carries_metres
# true_retained_kicks
# kick_try_scored
# turnovers_conceded
# free_kick_conceded_at_scrum
# red_card_second_yellow
# red_cards
# kick_touch_in_goal
# kick_charged_down
# penalty_conceded_wrong_side
# lineout_throw_won_penalty
# total_lineouts
# total_kicks_succeeded
# lineout_throw_won_free_kick
# mauling_metres
# restarts_won
# runs
# goals
# penalty_conceded_high_tackle
# possession
# pc_possession_first
# pc_possession_second
# territory
# pc_territory_first
# pc_territory_second
# ball_won_zone_a
# ball_won_zone_b
# ball_won_zone_c
# ball_won_zone_d
# attacking_events_zone_a
# attacking_events_zone_b
# attacking_events_zone_c
# attacking_events_zone_d
# ball_possession_last_10_mins
# territory_last_10_mins