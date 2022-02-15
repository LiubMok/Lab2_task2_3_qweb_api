"""Module that can walk through json files"""

import json
from pprint import pprint
from sys import exit


def file_reader(path):
    """
    Function that reads json file.
    :param path: file name.
    :return: read file as an array or dictionary.
    >>> file_reader('frienfs_list_Obama.json')['users'][0]["id"]
    1330457336
    """
    with open(path, "r", encoding="utf-8") as file:
        decoded_file = json.load(file)
        return decoded_file


def sort_dict(dictionary: dict) -> dict:
    """
    Function that sorts dictionary by its keys.
    :param dictionary: dictionary to sort.
    :return: sorted dict.
    >>> sort_dict({23: 1, 42: 4, 37: 9, 41: 16, 50: 25})
    {23: 1, 37: 9, 41: 16, 42: 4, 50: 25}
    """
    dictionary_items = dictionary.items()
    sorted_items = sorted(dictionary_items)
    return dict(sorted_items)


def main(path_to_file):
    """
    This function gets all data and "walk through the file".
    :param path_to_file: file name where we will walk.
    """
    print('If you want to return to previous branch write 0 when the program'
          ' will ask you about number of key in the\ndictionary or index in'
          ' list or write "exit" when you want to end the program work.')
    print()
    path = dict()
    iterator = 0
    while True:
        data = file_reader(path_to_file)
        for element in sort_dict(path).keys():
            try:
                data = data[path[element]]
            except KeyError:
                continue
            except IndexError:
                continue
            except ValueError:
                continue
            except TypeError:
                continue
        if type(data) == dict:
            pprint(data.keys())
            key = input()
            if key == '0':
                path.pop(iterator - 1)
                iterator -= 1
            elif key == 'exit':
                exit()
            else:
                path[iterator] = key
                iterator += 1
        elif type(data) == list:
            print(f'please write a number from 0 to {len(data)}')
            try:
                index_in_list = input()
                if index_in_list == '0':
                    path.pop(iterator - 1)
                    iterator -= 1
                elif index_in_list == "exit":
                    exit()
                else:
                    path[iterator] = int(index_in_list) - 1
                    iterator += 1
            except TypeError:
                exit()
            except ValueError:
                continue
        else:
            print(data)
            print('!!!!That`s a breakpoint of the program, you could return to the'
                  ' previous branch or exit:')
            result = input()
            if result == '0':
                path.pop(iterator - 1)
                iterator -= 1
            elif result == 'exit':
                exit()
            else:
                print('Invalid input')


if __name__ == "__main__":
    print('Please write the name of the file:')
    file_name = input()
    pprint(main(file_name))
