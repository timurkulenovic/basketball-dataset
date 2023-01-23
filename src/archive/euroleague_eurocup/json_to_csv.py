



#     # Gather all the data
#     game_row = [
#         season, season_part, rnd,
#         date_string, time, venue,
#         attendance, ref1, ref2, ref3,
#         h_name, a_name, h_code, a_code,
#         h_score, a_score, *h_quarters,
#         *a_quarters, *h_stats, *a_stats
#     ]
#     print(game_row)
#     games_data.append(game_row)
#
# # Save data
# df_euroleague = pd.DataFrame(data=games_data, columns=col_names)
# df_euroleague.to_csv("../../data/euroleague_new/euroleague_games.csv", index=False)