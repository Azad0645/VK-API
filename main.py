import requests
import os
import argparse
from dotenv import load_dotenv

load_dotenv()


def is_short_url(vk_token, url):
    api_url = "https://api.vk.com/method/utils.getLinkStats"
    params = {
        "access_token": vk_token,
        "key": url,
        "interval": "forever",
        "v": "5.199"
    }
    response = requests.get(api_url, params=params)
    return "response" in response.json()


def get_short_link(vk_token, url_to_shorten):
    api_url = "https://api.vk.com/method/utils.getShortLink"
    params = {
        "access_token": vk_token,
        "url": url_to_shorten,
        "v": "5.199"
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    return response.json()["response"]["short_url"]


def get_clicks_count(vk_token, short_url):
    api_url = "https://api.vk.com/method/utils.getLinkStats"
    params = {
        "access_token": vk_token,
        "key": short_url,
        "interval": "forever",
        "v": "5.199"
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    return response.json()["response"]["stats"]["views"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Сокращение ссылок и получение статистики VK.")
    parser.add_argument("url", help="Введите ссылку для обработки (длинную или короткую).")
    args = parser.parse_args()

    vk_token = os.environ["VK_ACCESS_TOKEN"]
    url = args.url

    try:
        if is_short_url(vk_token, url):
            print(f"Количество кликов по ссылке: {get_clicks_count(vk_token, url)}")
        else:
            print(f"Сокращенная ссылка: {get_short_link(vk_token, url)}")
    except requests.exceptions.HTTPError:
        print("Ошибка HTTP: Некорректный запрос.")
    except KeyError:
        print("Ошибка: Некорректная ссылка или токен.")