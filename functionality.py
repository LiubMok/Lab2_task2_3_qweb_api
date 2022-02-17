from typing import Dict
import requests
import folium
from geopy.geocoders import Nominatim
from app import dashboard_errors


def make_request(url: str) -> Dict:
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAAMjqZAEAAAAAyG9kB4mUtaz%2BwBOx1qGjAz4q' \
                   'f18%3Dz5SOmNAmwDaPPHYTYPnOsu3IOpjSmvKf2yC7WcoTp9jpE8CSV8'
    headers_for_search = {
        'Authorization': f'Bearer {bearer_token}'
    }
    return requests.get(url, headers=headers_for_search).json()


def get_information_with_api(name):
    try:
        user_id = make_request(f"https://api.twitter.com/2/users/by/username/{name}")["data"]["id"]
        print(user_id)
        return make_request(f'https://api.twitter.com/2/users/{user_id}/following?user.fields=location')
    except KeyError:
        return dashboard_errors('for_errors.html')
    except TypeError:
        return dashboard_errors('for_errors.html')


def find_coords(address):
    geolocator = Nominatim(user_agent='UCU_APP')
    if location := geolocator.geocode(address):
        return location.latitude, location.longitude


def sort_data(json_file: dict, amount) -> list:
    data = []
    try:
        for person in json_file['data']:
            if 'location' in person:
                nickname = person['name']
                if coordinates := find_coords(person['location']):
                    data.append(tuple((nickname, coordinates[0], coordinates[1], person['location'])))
        return data[:int(amount)]
    except TypeError:
        return dashboard_errors('for_errors.html')
    except IndexError:
        return dashboard_errors('for_errors.html')


def create_html(data: list):
    m = folium.Map(zoom_start=2)
    try:
        for friend in range(len(data)):
            folium.Marker(location=[data[friend][1], data[friend][2]], tooltip=data[friend][0], popup=data[friend][3],
                          icon=folium.Icon(color="red")).add_to(m)
        return m.get_root().render()
    except IndexError:
        return dashboard_errors('for_errors.html')


def main(name, amount):
    information = get_information_with_api(name)
    sorted_information = sort_data(information, amount)
    return create_html(sorted_information)
