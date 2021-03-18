import glicko2
import csv
import random
from file_handler import *

rbCSV = "rb.csv"
wrCSV = "wr.csv"

class ratings():
    def __init__(self):
        self._playerList = FileHandler.load_data(rbCSV,Extensions.CSV)

    def load_player_dictionary(self):
        for key in self._playerList.items():
            print(key)



    def createPlayerRatings(self):
       pass





# def saveRBRatings():
#     pass
# def savePlayerRatings():
#     playerList.sort(key=lambda x: x.rating, reverse=True)
#     with open(data, mode='w', newline='') as csv_file:
#         writer = csv.writer(csv_file, delimiter=',')
#         for player in playerList:
#             writer.writerow([player.name, player.rating])
#             print(player)
#
# def createPlayerRatings(data):
#     load
#
#     with open(data) as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         for row in csv_reader:
#                 if len(row) > 1:
#                     newPlayer = glicko2.Player(row[0], row[1])
#                     playerList.append(newPlayer)
#                 else:
#                     newPlayer = glicko2.Player(row[0])
#                     playerList.append(newPlayer)
#
#     run = True
#
#     while(run):
#         player1, player2 = random.sample(playerList, 2)
#
#         choice = None
#
#         while choice != '1' and choice != '2' and choice != 'q':
#             print('1: ', player1.name, " | 2: ", player2.name)
#             choice = input()
#
#         if choice == 'q':
#             return
#         elif (choice == '1'): #player1 wins
#             player1.update_player([player2.rating], [player2.rd], [1])
#             player2.update_player([player1.rating], [player1.rd], [0])
#         else: #player2 wins
#             player1.update_player([player2.rating], [player2.rd], [0])
#             player2.update_player([player1.rating], [player1.rd], [1])
#
#         savePlayerRatings()

def main():
    pRatings = ratings()
    pRatings.load_player_dictionary()
    pRatings.createPlayerRatings()


if __name__ == "__main__":
    main()