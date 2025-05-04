import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class DataLoader:
    def __init__(self):  # Tworzymy klasę DataLoader, która ma na celu wgrywanie plików
        self.data = None

    def load_data(self, file_csv):
        try:
            self.data = pd.read_csv(file_csv, encoding='ISO-8859-1')
        except FileNotFoundError:
            print("Plik nie istnieje")  # Obiekt "load_data" służy do ładowania danych z pliku CSV. Po załadowaniu,
            # dane są przypisane do "self.data"

    def get_data(self):
        return self.data  # Służy do zwracania danych przypisanych do "self.data"

class DataAnalyzer:  # Tworzymy klasę DataAnalyzer która ma na celu przedstawienie statystyk drużyny
    def __init__(self, data_loader):
        self.data_loader = data_loader  # wartość argumentu data_loader jest przypisywana do atrybutu instancji
        # self.data_loader.

    def print_unique_team_names(self):
        data = self.data_loader.get_data()
        if data is not None:
            unique_teams = data['Team Name'].str.lower().unique()
            print(", ".join(unique_teams))
        else:
            print("Dane nie zostały załadowane")

    def get_main_metrics(self, team_name):
        data = self.data_loader.get_data()
        if data is not None:
            team_data = data[data['Team Name'].str.lower() == team_name.lower()].copy()
            if not team_data.empty:
                number_of_matches = np.sum(team_data[['Wins', 'Draws', 'Loses']].values)
                team_data['Average points per game'] = np.round(team_data['Points'].values / number_of_matches, 2)

                columns_to_display = ['Team Name', 'Team Code', 'Wins', 'Draws', 'Loses', 'Points',
                                      'Average points per game', 'Qualified', 'Group', 'Country Code']
                team_data = team_data[columns_to_display]

                # Oblicz średnie wartości dla wszystkich drużyn
                print("\n ---> OVERVIEW: \n")
                avg_metrics = {
                    'Wins': data['Wins'].mean().round(2),
                    'Draws': data['Draws'].mean().round(2),
                    'Loses': data['Loses'].mean().round(2),
                    'Points': data['Points'].mean().round(2),
                    'Average points per game': (data['Points'] / (data['Wins'] + data['Draws'] + data['Loses'])).mean().round(2)
                }

                for metric in ['Wins', 'Draws', 'Loses', 'Points', 'Average points per game']:
                    team_value = team_data[metric].values[0]
                    avg_value = avg_metrics[metric]
                    difference = (team_value - avg_value).round(2)
                    print(f"{metric}: {team_value} (Średnia: {avg_value}, Różnica: {difference})")

            else:
                print(f"Nie znaleziono danych dla drużyny: {team_name}")
        else:
            print("Dane nie zostały załadowane")

    def plot_team_history(self, team_name):
        data = self.data_loader.get_data()
        if data is not None:
            team_data = data[data['Team Name'].str.lower() == team_name.lower()].copy()
            if not team_data.empty:
                seasons = ['2011/12', '2012/13', '2013/14', '2014/15', '2015/16', '2016/17', '2017/18', '2018/19',
                           '2019/20', '2020/21']  # Wyciągnięcie kolumn z nazwami sezonów
                team_history = team_data[
                    seasons].values.flatten().tolist()

                team_history = [x if pd.notnull(x) else 'No qualifications' for x in team_history]

                all_stages = ['No qualifications', 'Second qualifying round', 'Third qualifying round', 'Play-offs',
                              'Group stage', 'Round of 16', 'Quarter-finals', 'Semi-finals', 'Final']
                stage_dict = {stage: i for i, stage in enumerate(all_stages)}
                y_values = [stage_dict[x] for x in team_history]

                plt.figure(figsize=(10, 6))
                plt.plot(seasons, y_values, marker='o', linestyle='-', color='b')
                plt.title(f'History of the stage the {team_name} has reached in a given season')
                plt.xlabel('Season')
                plt.ylabel('Stage')
                plt.xticks(rotation=45)
                plt.yticks(ticks=range(len(all_stages)), labels=all_stages)
                plt.grid(True)
                plt.tight_layout()
                plt.show()
            else:
                print(f"Nie znaleziono danych dla drużyny: {team_name}")
        else:
            print("Dane nie zostały załadowane")

    def get_offensive_section(self, team_name):
        data = self.data_loader.get_data()
        if data is not None:
            team_data = data[data['Team Name'].str.lower() == team_name.lower()].copy()
            if not team_data.empty:
                number_of_matches = (team_data['Wins'] + team_data['Draws'] + team_data['Loses'])

                goals_per_game = (team_data['Goals'] / number_of_matches).mean().round(2)
                assists_per_game = (team_data['Assists'] / number_of_matches).mean().round(2)
                average_possession = (team_data['Possession (%)']).mean().round(2)
                corners_per_game = (team_data['Corners taken'] / number_of_matches).mean().round(2)
                average_attacks_per_game = (team_data['Attacks'] / number_of_matches).mean().round(2)
                runs_into_attacking_third_per_game = (team_data['Runs into attacking third'] / number_of_matches).mean().round(2)
                passes_into_penalty_area_per_game = (team_data['Passes into penalty area'] / number_of_matches).mean().round(2)
                offsides_per_game = (team_data['Offsides'] / number_of_matches).mean().round(2)

                total_matches = data['Wins'] + data['Draws'] + data['Loses']
                avg_goals_per_game = (data['Goals'] / total_matches).mean().round(2)
                avg_assists_per_game = (data['Assists'] / total_matches).mean().round(2)
                avg_possession = (data['Possession (%)']).mean().round(2)
                avg_corners_per_game = (data['Corners taken'] / total_matches).mean().round(2)
                avg_attacks_per_game = (data['Attacks'] / total_matches).mean().round(2)
                avg_runs_into_attacking_third_per_game = (data['Runs into attacking third'] / total_matches).mean().round(2)
                avg_passes_into_penalty_area_per_game = (data['Passes into penalty area'] / total_matches).mean().round(2)
                avg_offsides_per_game = (data['Offsides'] / total_matches).mean().round(2)

                print("\n ---> OFFENSIVE METRICS: \n")
                offensive_metrics = {
                    'Goals per game': (goals_per_game, avg_goals_per_game, (goals_per_game - avg_goals_per_game).round(2)),
                    'Assists per game': (assists_per_game, avg_assists_per_game, (assists_per_game - avg_assists_per_game).round(2)),
                    'Average possession (%)': (average_possession, avg_possession, (average_possession - avg_possession).round(2)),
                    'Corners per game': (corners_per_game, avg_corners_per_game, (corners_per_game - avg_corners_per_game).round(2)),
                    'Average attacks per game': (average_attacks_per_game, avg_attacks_per_game, (average_attacks_per_game - avg_attacks_per_game).round(2)),
                    'Runs into attacking third per game': (runs_into_attacking_third_per_game, avg_runs_into_attacking_third_per_game, (runs_into_attacking_third_per_game - avg_runs_into_attacking_third_per_game).round(2)),
                    'Passes into penalty area per game': (passes_into_penalty_area_per_game, avg_passes_into_penalty_area_per_game, (passes_into_penalty_area_per_game - avg_passes_into_penalty_area_per_game).round(2)),
                    'Offsides per game': (offsides_per_game, avg_offsides_per_game, (offsides_per_game - avg_offsides_per_game).round(2))
                }

                for metric, (value, avg_value, difference) in offensive_metrics.items():
                    print(f"{metric}: {value} (Średnia: {avg_value}, Różnica: {difference})")
            else:
                print(f"Nie znaleziono danych dla drużyny: {team_name}")
        else:
            print("Dane nie zostały załadowane")

    def get_defensive_section(self, team_name):
        data = self.data_loader.get_data()
        if data is not None:
            team_data = data[data['Team Name'].str.lower() == team_name.lower()].copy()
            if not team_data.empty:
                number_of_matches = (team_data['Wins'] + team_data['Draws'] + team_data['Loses'])

                goals_conceded_per_game = (team_data['Goals conceded'] / number_of_matches).mean().round(2)
                saves_per_game = (team_data['Saves'] / number_of_matches).mean().round(2)
                balls_recovered_per_game = (team_data['Balls recovered'] / number_of_matches).mean().round(2)
                blocked_shots_per_game = (team_data['Blocks'] / number_of_matches).mean().round(2)
                fouls_committed_per_game = (team_data['Fouls committed'] / number_of_matches).mean().round(2)
                yellow_cards_per_game = (team_data['Yellow cards'] / number_of_matches).mean().round(2)

                total_matches = data['Wins'] + data['Draws'] + data['Loses']
                avg_goals_conceded_per_game = (data['Goals conceded'] / total_matches).mean().round(2)
                avg_saves_per_game = (data['Saves'] / total_matches).mean().round(2)
                avg_balls_recovered_per_game = (data['Balls recovered'] / total_matches).mean().round(2)
                avg_blocked_shots_per_game = (data['Blocks'] / total_matches).mean().round(2)
                avg_fouls_committed_per_game = (data['Fouls committed'] / total_matches).mean().round(2)
                avg_yellow_cards_per_game = (data['Yellow cards'] / total_matches).mean().round(2)

                print("\n ---> DEFENSIVE METRICS: \n")
                defensive_metrics = {
                    'Goals conceded per game': (goals_conceded_per_game, avg_goals_conceded_per_game, (goals_conceded_per_game - avg_goals_conceded_per_game).round(2)),
                    'Saves per game': (saves_per_game, avg_saves_per_game, (saves_per_game - avg_saves_per_game).round(2)),
                    'Balls recovered per game': (balls_recovered_per_game, avg_balls_recovered_per_game, (balls_recovered_per_game - avg_balls_recovered_per_game).round(2)),
                    'Blocked shots per game': (blocked_shots_per_game, avg_blocked_shots_per_game, (blocked_shots_per_game - avg_blocked_shots_per_game).round(2)),
                    'Fouls committed per game': (fouls_committed_per_game, avg_fouls_committed_per_game, (fouls_committed_per_game - avg_fouls_committed_per_game).round(2)),
                    'Yellow cards per game': (yellow_cards_per_game, avg_yellow_cards_per_game, (yellow_cards_per_game - avg_yellow_cards_per_game).round(2))
                }

                for metric, (value, avg_value, difference) in defensive_metrics.items():
                    print(f"{metric}: {value} (Średnia: {avg_value}, Różnica: {difference})")

            else:
                print(f"Nie znaleziono danych dla drużyny: {team_name}")
        else:
            print("Dane nie zostały załadowane")

    def plot_top_scorers(self):
        data = self.data_loader.get_data()
        if data is not None:
            top_5_scorers = data.nlargest(5, 'Goals')
            plt.figure(figsize=(10, 6))
            plt.bar(top_5_scorers['Team Name'], top_5_scorers['Goals'], color='b')
            plt.title('Top 5 Scoring Teams')
            plt.xlabel('Team')
            plt.ylabel('Goals')
            plt.tight_layout()
            plt.show()
        else:
            print("Dane nie zostały załadowane")

    def plot_top_foulers(self):
        data = self.data_loader.get_data()
        if data is not None:
            top_5_foulers = data.nlargest(5, 'Fouls committed')
            plt.figure(figsize=(10, 6))
            plt.bar(top_5_foulers['Team Name'], top_5_foulers['Fouls committed'], color='r')
            plt.title('Top 5 Fouling Teams')
            plt.xlabel('Team')
            plt.ylabel('Fouls Committed')
            plt.tight_layout()
            plt.show()
        else:
            print("Dane nie zostały załadowane")

    def plot_correlation(self):
        data = self.data_loader.get_data()
        if data is not None:
            plt.figure(figsize=(10, 6))
            plt.scatter(data['Points'], data['Possession (%)'], color='b')
            correlation = data['Points'].corr(data['Possession (%)'])
            plt.title(f'Correlation between Points and Possession: {correlation:.2f}')
            plt.xlabel('Points')
            plt.ylabel('Possession')
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        else:
            print("Dane nie zostały załadowane")


class FootballDataApp:
    def __init__(self, data_file):
        self.loader = DataLoader()
        self.loader.load_data(data_file)
        self.analyzer = DataAnalyzer(self.loader)

    def run(self):
        self.analyzer.print_unique_team_names()
        team_name = input('\n Wpisz nazwę drużyny z listy powyżej lub "all" dla ogólnego podsumowania: ')
        if team_name == 'all':
            self.analyzer.plot_top_scorers()
            self.analyzer.plot_top_foulers()
            self.analyzer.plot_correlation()

        else:
            self.analyzer.get_main_metrics(team_name)
            self.analyzer.plot_team_history(team_name)
            self.analyzer.get_offensive_section(team_name)
            self.analyzer.get_defensive_section(team_name)


if __name__ == '__main__':
    app = FootballDataApp('Tu wpisz lokalizacje pliku')
    app.run()