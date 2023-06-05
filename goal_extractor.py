def goal_extractor(string):
    if string[0] == '(':
        home_penal = string[1]
        home_goles = string[4]
        away_goles = string[6]
        away_penal = string[9]
        return int(home_penal), int(home_goles), int(away_goles), int(away_penal)
    else:
        home_goles = string[0]
        away_goles = string[2]
        return int(home_goles), int((away_goles))
