def goal_extractor(string):
    if string[0] == '(':
        home_penal = string[1]
        home_goles = string[4]
        away_goles = string[6]
        away_penal = string[9]
        return [int(home_penal), int(home_goles), int(away_goles), int(away_penal)]
    else:
        home_goles = string[0]
        away_goles = string[2]
        return [int(home_goles), int((away_goles))]


def create_dictionary(archive):
    with open(archive, 'r', encoding='utf-8') as data:
        lines = data.readlines()
        column_names = lines[0].strip().split(',')
        time_index = column_names.index('match_time')
        country_name_index = column_names.index('home_team')
        processed_countries = {}

        for line in lines[1:]:
            row_values = line.strip().split(',')
            country_name = row_values[country_name_index]
            if country_name in processed_countries:
                continue
            match_time = row_values[time_index]
            line_counter = 0
            stats_processed = {
                'goals': 0, 'points': [0, 0, 0, 0], 'rank': 0}

            for line in lines[1:]:
                new_row_values = line.strip().split(',')
                if country_name not in new_row_values:
                    continue
                else:
                    line_counter += 1
                    goals = goal_extractor(new_row_values[7])
                    if new_row_values[3] == country_name:
                        stats_processed['goals'] += goals[0]
                    if new_row_values[4] == country_name:
                        stats_processed['goals'] += goals[1]

                    if int(match_time[6]) == 2:
                        if int(match_time[9]) > 3 or int(match_time[8]) >= 1:
                            continue
                        else:
                            if new_row_values[3] == country_name:
                                if goals[0] > goals[1]:
                                    if line_counter == 1:
                                        stats_processed['points'][line_counter] += 3
                                    if line_counter == 2:
                                        stats_processed['points'][line_counter] += (
                                            stats_processed['points'][line_counter - 1] + 3)
                                    if line_counter == 3:
                                        stats_processed['points'][line_counter] += (
                                            stats_processed['points'][line_counter - 1] + 3)
                                if goals[0] == goals[1]:
                                    if line_counter == 1:
                                        stats_processed['points'][line_counter] += 1
                                    if line_counter == 2:
                                        stats_processed['points'][line_counter] += (
                                            sstats_processed['points'][line_counter - 1] + 1)
                                    if line_counter == 3:
                                        stats_processed['points'][line_counter] += (
                                            stats_processed['points'][line_counter - 1] + 1)
                                if goals[0] < goals[1]:
                                    if line_counter == 1:
                                        stats_processed['points'][line_counter] += 0
                                    if line_counter == 2:
                                        stats_processed['points'][line_counter] += (
                                            stats_processed['points'][line_counter - 1] + 0)
                                    if line_counter == 3:
                                        stats_processed['points'][line_counter] += (
                                            stats_processed['points'][line_counter - 1] + 0)
                            elif new_row_values[4] == country_name:
                                if goals[0] < goals[1]:
                                    if line_counter == 1:
                                        stats_processed['points'][line_counter] += 3
                                    if line_counter == 2:
                                        stats_processed['points'][line_counter] += (
                                            stats_processed['points'][line_counter - 1] + 3)
                                    if line_counter == 3:
                                        stats_processed['points'][line_counter] += (
                                            stats_processed['points'][line_counter - 1] + 3)
                                if goals[0] == goals[1]:
                                    if line_counter == 1:
                                        stats_processed['points'][line_counter] += 1
                                    if line_counter == 2:
                                        stats_processed['points'][line_counter] += (
                                            stats_processed['points'][line_counter - 1] + 1)
                                    if line_counter == 3:
                                        stats_processed['points'][line_counter] += (
                                            stats_processed['points'][line_counter - 1] + 1)
                                if goals[0] > goals[1]:
                                    if line_counter == 1:
                                        stats_processed['points'][line_counter] += 0
                                    if line_counter == 2:
                                        stats_processed['points'][line_counter] += (
                                            stats_processed['points'][line_counter - 1] + 0)
                                    if line_counter == 3:
                                        stats_processed['points'][line_counter] += (
                                            stats_processed['points'][line_counter - 1] + 0)
                    else:
                        if new_row_values[3] == country_name:
                            if goals[0] > goals[1]:
                                if line_counter == 1:
                                    stats_processed['points'][line_counter] += 3
                                if line_counter == 2:
                                    stats_processed['points'][line_counter] += (
                                        stats_processed['points'][line_counter - 1] + 3)
                                if line_counter == 3:
                                    stats_processed['points'][line_counter] += (
                                        stats_processed['points'][line_counter - 1] + 3)
                            if goals[0] == goals[1]:
                                if line_counter == 1:
                                    stats_processed['points'][line_counter] += 1
                                if line_counter == 2:
                                    stats_processed['points'][line_counter] += (
                                        stats_processed['points'][line_counter - 1] + 1)
                                if line_counter == 3:
                                    stats_processed['points'][line_counter] += (
                                        stats_processed['points'][line_counter - 1] + 1)
                            if goals[0] < goals[1]:
                                if line_counter == 1:
                                    stats_processed['points'][line_counter] += 0
                                if line_counter == 2:
                                    stats_processed['points'][line_counter] += (
                                        stats_processed['points'][line_counter - 1] + 0)
                                if line_counter == 3:
                                    stats_processed['points'][line_counter] += (
                                        stats_processed['points'][line_counter - 1] + 0)
                        elif new_row_values[4] == country_name:
                            if goals[0] < goals[1]:
                                if line_counter == 1:
                                    stats_processed['points'][line_counter] += 3
                                if line_counter == 2:
                                    stats_processed['points'][line_counter] += (
                                        stats_processed['points'][line_counter - 1] + 3)
                                if line_counter == 3:
                                    stats_processed['points'][line_counter] += (
                                        stats_processed['points'][line_counter - 1] + 3)
                            if goals[0] == goals[1]:
                                if line_counter == 1:
                                    stats_processed['points'][line_counter] += 1
                                if line_counter == 2:
                                    stats_processed['points'][line_counter] += (
                                        stats_processed['points'][line_counter - 1] + 1)
                                if line_counter == 3:
                                    stats_processed['points'][line_counter] += (
                                        stats_processed['points'][line_counter - 1] + 1)
                            if goals[0] > goals[1]:
                                if line_counter == 1:
                                    stats_processed['points'][line_counter] += 0
                                if line_counter == 2:
                                    stats_processed['points'][line_counter] += (
                                        stats_processed['points'][line_counter - 1] + 0)
                                if line_counter == 3:
                                    stats_processed['points'][line_counter] += (
                                        stats_processed['points'][line_counter - 1] + 0)
            processed_countries[country_name] = stats_processed
        return processed_countries


print(create_dictionary('data.csv'))
