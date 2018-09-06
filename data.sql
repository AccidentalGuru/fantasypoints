SELECT
	player.player_id,
	player.full_name,
	player.position,
	player.team,
	COUNT(DISTINCT game) games_played,
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
		SUM(defense_misc_tds) * ( 6) fantasy_points,
	COUNT(play_player) plays,
	SUM(passing_tds) + SUM(receiving_tds) + SUM(rushing_tds) touchdowns,
	SUM(passing_yds) + SUM(receiving_yds) + SUM(rushing_yds) yards,
	SUM(passing_yds) passing_yards,
	SUM(passing_att) passing_attempts,
	CAST(SUM(passing_yds) as float) / nullif(SUM(passing_att), 0) passing_yards_per_attempt,
	SUM(receiving_yds) receiving_yards,
	SUM(receiving_tar) receiving_targets,
	CAST(SUM(receiving_yds) as float) / nullif(SUM(receiving_tar), 0) receiving_yards_per_target,
	SUM(rushing_yds) rushing_yards,
	SUM(rushing_att) rushing_attempts,
	CAST(SUM(rushing_yds) as float) / nullif(SUM(rushing_att), 0) rushing_yards_per_attempt
FROM play_player
LEFT JOIN player
ON play_player.player_id = player.player_id
LEFT JOIN game
ON play_player.gsis_id = game.gsis_id
WHERE game.season_year = 2017
	AND game.season_type = 'Regular'
GROUP BY player.player_id, player.full_name, player.team, player.position

