SELECT
	player.full_name,
	CAST(player.position as varchar),
	player.team,
	COUNT(DISTINCT game) games_played,
	CAST(
		SUM(passing_yds)      * (.4) +
		SUM(passing_tds)      * ( 4) +
		SUM(passing_int)      * (-2) +
		SUM(passing_twoptm)   * ( 2) +
		SUM(rushing_yds)      * (.1) +
		SUM(rushing_tds)      * ( 6) +
		SUM(rushing_twoptm)   * ( 2) +
		SUM(receiving_yds)    * (.1) +
		SUM(receiving_tds)    * ( 6) +
		SUM(receiving_twoptm) * ( 2) +
		SUM(kickret_tds)      * ( 6) +
		SUM(puntret_tds)      * ( 6) +
		SUM(fumbles_rec_tds)  * ( 6) +
		SUM(fumbles_lost)     * (-2) +
		SUM(defense_int_tds)  * ( 6) +
		SUM(kicking_rec_tds)  * ( 6) +
		SUM(defense_misc_tds) * ( 6)
	as float) fantasy_points,
	COUNT(play_player) plays,
	SUM(passing_tds) + SUM(receiving_tds) + SUM(rushing_tds) touchdowns,
	SUM(passing_yds) + SUM(receiving_yds) + SUM(rushing_yds) yards,
	SUM(passing_yds) passing_yards,
	SUM(passing_att) passing_attempts,
	SUM(receiving_yds) receiving_yards,
	SUM(receiving_tar) receiving_targets,
	SUM(rushing_yds) rushing_yards,
	SUM(rushing_att) rushing_attempts
FROM play_player
LEFT JOIN player
ON play_player.player_id = player.player_id
LEFT JOIN game
ON play_player.gsis_id = game.gsis_id
WHERE game.season_year = 2018
	AND game.season_type = 'Regular'
	AND player.position in ('QB', 'RB', 'WR', 'TE')
GROUP BY player.player_id, player.full_name, player.team, player.position
