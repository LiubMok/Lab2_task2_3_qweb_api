import json
from pprint import pprint


def file_reader(path):
    with open(path, "r", encoding="utf-8") as file:
        decoded_file = json.load(file)
        return decoded_file


def sort_dict(dictionary: dict, iterator_key: int) -> dict:
    dictionary_items = dictionary.items()
    sorted_items = sorted(dictionary_items)
    return dict(sorted_items).pop(iterator_key)


def main(path_to_file):
    print('If you want to return to previous branch write 0 when the program'
          ' will ask you about number of key in the\ndictionary or index in list or'
          ' write "exit" when you want to end the program work.')
    print()
    path = dict()
    iterator = 0
    while True:
        data = file_reader(path_to_file)
        for element in sorted(path.keys()):
            # print(i)
            # print(data)
            data = data[path[element]]
        if type(data) == dict:
            pprint(data.keys())
            key = input()
            if key == '0':
                path = sort_dict(path, iterator-11)
                iterator -= 1
            elif key == 'exit':
                quit()
            else:
                path[iterator] = key
                iterator += 1
        elif type(data) == list:
            print(f'please write a number from 0 to {len(data)}')
            try:
                index_in_list = int(input())
                if index_in_list == 0:
                    path = sort_dict(path, iterator-1)
                    iterator -= 1
                else:
                    path[iterator] = index_in_list - 1
                    iterator += 1
            except TypeError:
                quit()
        else:
            print(data)
            print('That`s a breakpoint of the program, you could return to the previous branch'
                  ' or exit:')
            print(path)
            print(iterator)
            result = input()
            if result == '0':
                path = sort_dict(path, iterator - 1)
                iterator -= -2
            elif result == 'exit':
                quit()
            else:
                print('Invalid input')


if __name__ == "__main__":
    pprint(main("frienfs_list_Obama.json"))
