from data.library import words, used_words
from data.hangman import HUMAN
import pprint
import random
import os

def play():
    def choiсe_word():
        """
         randomly select a word and save it to a file
        :return: word, status_list_letters
        """
        try:
            choiсe_word = random.choice(words)
            used_words.append(choiсe_word)
            words.remove(choiсe_word)
            status_letters_in_word = {}
            i = 0
            for letter in list(choiсe_word):
                status_letters_in_word[i] = {"let": letter, "stat": "unknown"}
                i += 1
            file = open('data\library.py', 'w')
            file.write('words = ' + pprint.pformat(words) + '\n')
            file.write('used_words = ' + pprint.pformat(used_words) + '\n')
            file.close()
            return choiсe_word, status_letters_in_word
        except IndexError:
            print('the words ran out')

    def display_board(used_letters: set, status_letters_in_word: dict, lifes: int, stat_human: list):
        print(stat_human[len(stat_human) - lifes])
        if used_letters != set():
            print('Used letters: ', used_letters)
        else:
            print('Used letters: ')
        for i in status_letters_in_word:
            if status_letters_in_word[i]["stat"] != "unknown":
                print(status_letters_in_word[i]['let'], end=' ')
                i += 1
            else:
                print('_ ', end='')
                i += 1
        print('\n')
    while True:
        try:
            choiсe_word1, status_letters_in_word = choiсe_word()
            lifes = 9
            used_letters = set()
            while True:
                display_board(used_letters, status_letters_in_word, lifes, HUMAN)
                player_letter = input('Enter letter\n')
                check_player_letter = False
                if len(player_letter) == 1 and (player_letter not in used_letters) and (player_letter not in list(' 1234567890-=!@#$%^&*()_+/.,<>?;:')):
                    used_letters.add(player_letter)
                    for i in range(len(choiсe_word1)):
                        if status_letters_in_word[i]['let'] == player_letter:
                            status_letters_in_word[i]['stat'] = 'known'
                            check_player_letter = True
                    if check_player_letter != True:
                        lifes -= 1
                        print("wrong answer!")
                    else:
                        print("FINE!")
                    clear = lambda: os.system('cls')
                    clear()
                    print('---------Next---------')
                elif len(player_letter) != 1:
                    print("Length must be 1 !")
                elif player_letter in list(' 1234567890-=!@#$%^&*()_+/.,<>?;:'):
                    print("Not LETTER!")
                elif player_letter in used_letters:
                    print("LETTER is USED!")
                # check on victory
                end_game = True
                for i in range(len(choiсe_word1)):
                    if status_letters_in_word[i]['stat'] != 'known':
                        end_game = False

                if end_game is True:
                    print('YEPPPP YOU WIN!!')
                    break
                elif lifes == 1:
                    print('OYYYYYY YOU DIE!!')
                    print(HUMAN[8])
                    break
            if lifes == 1 or end_game is True:
                play_again = input('press 1 to exit\n')
                if play_again == "1":
                    break
        except:
            break

if __name__ == "__main__":
    play()
