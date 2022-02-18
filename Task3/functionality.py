"""
Python code that do all functional.
"""
import random
from typing import Dict
import requests
import folium
from geopy.exc import GeocoderUnavailable
from geopy.geocoders import Nominatim
from Task3.flask_app import dashboard_errors


def make_request(url: str) -> Dict:
    """
    Make a request to the Twitter.
    :param url: url that will be sent to Twitter.
    :return: data
    """

    bearer_token = 'AAAAAAAAAAAAAAAAAAAAAMjqZAEAAAAAyG9kB4mUtaz%2BwBOx1qGjAz4q' \
                   'f18%3Dz5SOmNAmwDaPPHYTYPnOsu3IOpjSmvKf2yC7WcoTp9jpE8CSV8'
    headers_for_search = {
        'Authorization': f'Bearer {bearer_token}'
    }
    return requests.get(url, headers=headers_for_search).json()


def get_information_with_api(name: str) -> dict:
    """
    Thanks to extra function finds users friends as json file.
    :param name: name of the user.
    :return: json file as a dict.
    """
    try:
        user_id = make_request(f"https://api.twitter.com/2/users/by/"
                               f"username/{name}")["data"]["id"]
        return make_request(f'https://api.twitter.com/2/users/{user_id}/'
                            f'following?user.fields=location')
    except KeyError:
        return dashboard_errors('for_errors.html')
    except TypeError:
        return dashboard_errors('for_errors.html')


def find_coords(address: str) -> tuple:
    """
    Function that finds coordinates of the location.
    :param address: location
    :return: coordinates as a tuple.
    >>> find_coords('Los Angeles, California, USA')
    (34.0536909, -118.242766)
    >>> find_coords('Hudson Valley, New York, USA')
    (41.31611085, -74.12629189225156)
    """
    geolocator = Nominatim(user_agent='UCU_APP')
    if location := geolocator.geocode(address):
        return location.latitude, location.longitude


def sort_data(json_file: dict, amount) -> list:
    """
    Function creates data list which will be shown in the map.
    :param json_file: dictionary with data from Twitter.
    :param amount: amount of friends that should be in the map.
    :return: data as a list.
    """
    data = []
    try:
        for person in json_file['data']:
            if 'location' in person:
                nickname = person['name']
                try:
                    if coordinates := find_coords(person['location']):
                        data.append(tuple((nickname, coordinates[0],
                                           coordinates[1], person['location'])))
                except GeocoderUnavailable:
                    continue
        return data[:int(amount)]
    except TypeError:
        return dashboard_errors('for_errors.html')
    except IndexError:
        return dashboard_errors('for_errors.html')


def create_html(data: list):
    """
    Creates an html file which will show a location of user's friends.
    :param data: data form sort_data().
    :return: html file.
    """
    m = folium.Map(location=[45, 10], zoom_start=3)
    try:
        for friend in range(len(data)):
            folium.Marker(location=[data[friend][1], data[friend][2]],
                          tooltip=data[friend][0], popup=data[friend][3],
                          icon=folium.Icon(color='blue')).add_to(m)
        return m.get_root().render()
    except IndexError:
        return dashboard_errors('for_errors.html')


def main(name, amount):
    """
    Main function that runs extra.
    :param name: name of the user to find.
    :param amount: amount of friends to be shown in the map
    :return: html map.
    """

    information = get_information_with_api(name)
    sorted_information = sort_data(information, amount)
    return create_html(sorted_information)
