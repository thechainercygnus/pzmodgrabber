import re

import requests
from bs4 import BeautifulSoup

MOD_DETAIL_DICT = {}
MOD_ID_PATTERN = '(Mod\\sID:\\s*[a-zA-Z0-9]*)'

def get_mod_id_from_url(workshop_url: str) -> int | None:
    mod_id_index = workshop_url.find("id=")
    mod_id = workshop_url[mod_id_index:]
    try:
        cleaned_mod_id = mod_id.strip("id=")
        mod_id_int = int(cleaned_mod_id)
        return mod_id_int
    except Exception as e:
        print(e)
        return None

def get_soup(workshop_url: str) -> BeautifulSoup | None:
    try:
        response = requests.get(workshop_url)
        return BeautifulSoup(response.content, features="html.parser")
    except Exception  as e:
        print(e)
        return None

def get_mod_configurations(soup: BeautifulSoup):
    matches = re.findall(MOD_ID_PATTERN, soup.text)
    parsed_matches = parse_mod_configurations(matches)
    return parsed_matches

def parse_mod_configurations(mod_configs: list[str]) -> list[str]:
    parsed_mod_configs = [mod_config.split(":")[-1].strip() for mod_config in mod_configs]
    return parsed_mod_configs

def process_workshop_urls(workshop_urls: list[str]) -> dict:
    for workshop_url in workshop_urls:
        mod_id = get_mod_id_from_url(user_args.wu)
        if mod_id is not None:
            MOD_DETAIL_DICT['workshopitems'] = mod_id
        else:
            print("Mod ID not at end of URL. Enter URL as:")
            print("  https://steamcommunity.com/sharedfiles/filedetails/?id=")
            exit(1)
        soup = get_soup(user_args.wu)
        if soup.title.text.startswith("Steam Workshop::"):
            MOD_DETAIL_DICT['mod_title'] = soup.title.text.strip("Steam Workshop::")
        else:
            MOD_DETAIL_DICT['mod_title'] = soup.title.text
        MOD_DETAIL_DICT['modids'] = get_mod_configurations(soup)
        print(MOD_DETAIL_DICT)