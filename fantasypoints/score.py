def score(pp):
    score = 0

    # Passing
    score += pp.passing_yds * 0.04
    score += pp.passing_tds * 4
    score += pp.passing_int * -2
    score += pp.passing_twoptm * 2

    # Rushing
    score += pp.rushing_yds * 0.1
    score += pp.rushing_tds * 6
    score += pp.rushing_twoptm * 2

    # Receiving
    score += pp.receiving_yds * 0.1
    score += pp.receiving_tds * 6
    score += pp.receiving_twoptm * 2

    # Miscellaneous
    score += pp.kickret_tds * 6
    score += pp.puntret_tds * 6
    score += pp.fumbles_rec_tds * 6
    score += pp.fumbles_lost * -2
    score += pp.defense_int_tds * 6
    score += pp.kicking_rec_tds * 6
    score += pp.defense_misc_tds * 6
    # 2pt Return (2PTRET)	2
    # 1pt Safety (1PSF)

    return score
