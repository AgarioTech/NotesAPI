# This is a sample Python script.
import requests


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi():
    url = 'https://dog.ceo/api/breeds/list/all/'
    response = requests.get(url)
    return response.json()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(print_hi())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
