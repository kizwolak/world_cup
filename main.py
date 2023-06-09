import matplotlib.pyplot as plt
import csv


def goal_extractor(string):
    if string[0] == '(':
        home_penal = string[1]
        home_goles = string[4]
        away_goles = string[6]
        away_penal = string[9]
        return {'home_penal': int(home_penal), 'home_goles': int(home_goles),
                'away_goles': int(away_goles), 'away_penal': int(away_penal)}
    else:
        home_goles = string[0]
        away_goles = string[2]
        return {'home_goles': int(home_goles), 'away_goles': int((away_goles))}


def add_group(archive, processed_countries, country_name):
    with open(archive, 'r', encoding='utf-8') as data:
        lines = data.readlines()
        column_names = lines[0].strip().split(',')
        group_index = column_names.index('group')
        for line in lines:
            new_row_values = line.strip().split(',')
            if country_name in line:
                processed_countries[country_name]['group'] = new_row_values[group_index]


def calculate_ranks(lines, processed_countries):
    playoff_teams = []
    final_teams = []
    for line in lines[0:2]:
        new_row_values = line.strip().split(',')
        first_country_name = new_row_values[3]
        second_country_name = new_row_values[4]
        goals = goal_extractor(new_row_values[7])
        if new_row_values[3] == first_country_name:
            if goals['home_goles'] > goals['away_goles']:
                final_teams.append(first_country_name)
                playoff_teams.append(second_country_name)
            elif goals['away_goles'] > goals['home_goles']:
                final_teams.append(second_country_name)
                playoff_teams.append(first_country_name)
            else:
                if goals['home_penal'] > goals['away_penal']:
                    final_teams.append(first_country_name)
                    playoff_teams.append(second_country_name)
                else:
                    final_teams.append(second_country_name)
                    playoff_teams.append(first_country_name)
        if new_row_values[4] == first_country_name:
            if goals['away_goles'] > goals['home_goles']:
                final_teams.append(first_country_name)
                playoff_teams.append(second_country_name)
            elif goals['home_goles'] > goals['away_goles']:
                final_teams.append(second_country_name)
                playoff_teams.append(first_country_name)
            else:
                if goals['away_penal'] > goals['home_penal']:
                    final_teams.append(first_country_name)
                    playoff_teams.append(second_country_name)
                else:
                    final_teams.append(second_country_name)
                    playoff_teams.append(first_country_name)

    for line in lines:
        if playoff_teams[0] in line and playoff_teams[1] in line:
            new_row_values = line.strip().split(',')
            goals = goal_extractor(new_row_values[7])
            if playoff_teams[0] == new_row_values[3]:
                if goals['home_goles'] > goals['away_goles']:
                    processed_countries[playoff_teams[0]]['rank'] = 3
                    processed_countries[playoff_teams[1]]['rank'] = 4
                elif goals['away_goles'] > goals['home_goles']:
                    processed_countries[playoff_teams[0]]['rank'] = 4
                    processed_countries[playoff_teams[1]]['rank'] = 3
                else:
                    if home_penal > away_penal:
                        processed_countries[playoff_teams[0]
                                            ]['rank'] = 3
                        processed_countries[playoff_teams[1]
                                            ]['rank'] = 4
                    else:
                        processed_countries[playoff_teams[0]
                                            ]['rank'] = 4
                        processed_countries[playoff_teams[1]
                                            ]['rank'] = 3
            if playoff_teams[0] == new_row_values[4]:
                if goals['away_goles'] > goals['home_goles']:
                    processed_countries[playoff_teams[0]]['rank'] = 3
                    processed_countries[playoff_teams[1]]['rank'] = 4
                elif goals['home_goles'] > goals['away_goles']:
                    processed_countries[playoff_teams[0]]['rank'] = 4
                    processed_countries[playoff_teams[1]]['rank'] = 3
                else:
                    if goals['away_penal'] > goals['home_penal']:
                        processed_countries[playoff_teams[0]
                                            ]['rank'] = 3
                        processed_countries[playoff_teams[1]
                                            ]['rank'] = 4
                    else:
                        processed_countries[playoff_teams[0]
                                            ]['rank'] = 4
                        processed_countries[playoff_teams[1]
                                            ]['rank'] = 3

    for line in lines:
        if final_teams[0] in line and final_teams[1] in line:
            new_row_values = line.strip().split(',')
            goals = goal_extractor(new_row_values[7])
            if final_teams[0] == new_row_values[3]:
                if goals['home_goles'] > goals['away_goles']:
                    processed_countries[final_teams[0]]['rank'] = 1
                    processed_countries[final_teams[1]]['rank'] = 2
                elif goals['away_goles'] > goals['home_goles']:
                    processed_countries[final_teams[0]]['rank'] = 2
                    processed_countries[final_teams[1]]['rank'] = 1
                else:
                    if goals['home_penal'] > goals['away_penal']:
                        processed_countries[final_teams[0]
                                            ]['rank'] = 1
                        processed_countries[final_teams[1]
                                            ]['rank'] = 2
                    else:
                        processed_countries[final_teams[0]
                                            ]['rank'] = 2
                        processed_countries[final_teams[1]
                                            ]['rank'] = 1
            if final_teams[0] == new_row_values[4]:
                if goals['away_goles'] > goals['home_goles']:
                    processed_countries[final_teams[0]]['rank'] = 1
                    processed_countries[final_teams[1]]['rank'] = 2
                elif goals['home_goles'] > goals['away_goles']:
                    processed_countries[final_teams[0]]['rank'] = 2
                    processed_countries[final_teams[1]]['rank'] = 1
                else:
                    if away_penal > home_penal:
                        processed_countries[final_teams[0]
                                            ]['rank'] = 1
                        processed_countries[final_teams[1]
                                            ]['rank'] = 2
                    else:
                        processed_countries[final_teams[0]
                                            ]['rank'] = 2
                        processed_countries[final_teams[1]
                                            ]['rank'] = 1


def sort_item(item):
    return item[1]


def create_goal_ranking(dictionary):
    country_list = []
    goal_list = []
    for key in dictionary:
        country_list.append(key)
        goal_list.append(dictionary[key]['goals'])
    combined_list = sorted(zip(country_list, goal_list))
    combined_list.sort(key=sort_item, reverse=True)
    return combined_list


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
                if country_name not in new_row_values or line_counter == 3:
                    continue
                else:
                    line_counter += 1
                    goals = goal_extractor(new_row_values[7])
                    if new_row_values[3] == country_name:
                        stats_processed['goals'] += goals['home_goles']
                    if new_row_values[4] == country_name:
                        stats_processed['goals'] += goals['away_goles']

                    if int(match_time[6]) == 2:
                        if int(match_time[9]) > 3 or int(match_time[8]) >= 1:
                            continue
                        else:
                            if new_row_values[3] == country_name:
                                if goals['home_goles'] > goals['away_goles']:
                                    stats_processed['points'][line_counter] += (
                                        stats_processed['points'][line_counter - 1] + 3)
                                if goals['home_goles'] == goals['away_goles']:
                                    stats_processed['points'][line_counter] += (
                                        stats_processed['points'][line_counter - 1] + 1)
                                if goals['home_goles'] < goals['away_goles']:
                                    stats_processed['points'][line_counter] += (
                                        stats_processed['points'][line_counter - 1] + 0)
                            elif new_row_values[4] == country_name:
                                if goals['away_goles'] > goals['home_goles']:
                                    stats_processed['points'][line_counter] += (
                                        stats_processed['points'][line_counter - 1] + 3)
                                if goals['home_goles'] == goals['away_goles']:
                                    stats_processed['points'][line_counter] += (
                                        stats_processed['points'][line_counter - 1] + 1)
                                if goals['home_goles'] < goals['away_goles']:
                                    stats_processed['points'][line_counter] += (
                                        stats_processed['points'][line_counter - 1] + 0)
                    else:
                        if new_row_values[3] == country_name:
                            if goals['home_goles'] > goals['away_goles']:
                                stats_processed['points'][line_counter] += (
                                    stats_processed['points'][line_counter - 1] + 3)
                            if goals['home_goles'] == goals['away_goles']:
                                stats_processed['points'][line_counter] += (
                                    stats_processed['points'][line_counter - 1] + 1)
                            if goals['home_goles'] < goals['away_goles']:
                                stats_processed['points'][line_counter] += (
                                    stats_processed['points'][line_counter - 1] + 0)
                        elif new_row_values[4] == country_name:
                            if goals['away_goles'] > goals['home_goles']:
                                stats_processed['points'][line_counter] += (
                                    stats_processed['points'][line_counter - 1] + 3)
                            if goals['away_goles'] == goals['home_goles']:
                                stats_processed['points'][line_counter] += (
                                    stats_processed['points'][line_counter - 1] + 1)
                            if goals['away_goles'] < goals['home_goles']:
                                stats_processed['points'][line_counter] += (
                                    stats_processed['points'][line_counter - 1] + 0)

            processed_countries[country_name] = stats_processed
            add_group('group_stats.csv', processed_countries, country_name)
        calculated_ranks = calculate_ranks(lines[61:], processed_countries)
        goal_ranking = create_goal_ranking(processed_countries)
        return [calculated_ranks, goal_ranking, processed_countries]


def goals_graph(ranking):
    country_names, goals = zip(*ranking)

    fig = plt.figure(figsize=(15, 10))
    plt.bar(country_names[::-1], goals[::-1], color='blue', width=0.4)

    plt.xlabel("Countries")
    plt.ylabel("Goals scored")
    plt.title(
        "The amount of goals scored by each participant of the 2022 World Cup.")
    plt.xticks(rotation=90)
    plt.show()


def group_graph(ranking, group):
    teams_in_group = []
    matches = [0, 1, 2, 3]
    for key in ranking:
        if ranking[key]['group'] == str(group):
            teams_in_group.append([key, [ranking[key]['points']]])
        if len(teams_in_group) == 4:
            break
    for index, team in enumerate(teams_in_group):
        plt.plot(teams_in_group[index][1][0],
                 label=teams_in_group[index][0], marker='o')
    plt.legend()
    plt.xticks(matches)
    plt.title('Group point results by match')
    plt.xlabel('Match #')
    plt.ylabel('Points')
    plt.show()


def create_archive(dictionary):
    with open('processed_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['teams', 'goals', 'group', 'score1',
                        'score2', 'score3', 'rank'])
        for key in dictionary:
            print(dictionary[key]['group'])
            writer.writerow([key, dictionary[key]['goals'], dictionary[key]['group'], dictionary[key]['points']
                            [0], dictionary[key]['points'][1], dictionary[key]['points'][2], dictionary[key]['rank']])


dictionary = create_dictionary('data.csv')
create_archive(dictionary[2])
# group_graph(dictionary[2], 2)
# goals_graphic(dictionary[1])
