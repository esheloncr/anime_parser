import requests
import random
from requests.exceptions import ReadTimeout
from typing import Union


class RandomAnimePicker:
    """
    This is public interface to get random anime from "myanimelist.net"
    """

    def __init__(self):
        self.url = "https://api.jikan.moe/v3/"
        self.user_agent = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
        }

    def get_random_anime(self) -> dict:
        """
        This method create a random id and send request to public API. Then parse data and return an answer.
        If timeout reaches or error occurred - method calls self
        :return: dict
        """
        anime_id = random.randint(1, 20000)
        url = f"{self.url}anime/{anime_id}"
        try:
            response = requests.get(url, headers=self.user_agent, timeout=2)
            pictures = requests.get(
                f"{self.url}anime/{anime_id}/pictures",
                headers=self.user_agent,
                timeout=2,
            )
        except ReadTimeout:
            print("Bad request..Restarting")
            return self.get_random_anime()
        pictures = self._get_pictures(pictures)
        data = self._validate(response)
        if len(data) < 2:
            return self.get_random_anime()
        parsed_data = self._collect(data)
        parsed_data["pictures"] = pictures
        return parsed_data

    def _validate(self, response) -> dict:
        """
        This method validates response code
        :param response: HTTPResponse
        :return: dict
        """
        if response.status_code == 404:
            return {"error": "not found"}
        if response.status_code == 503:
            return {"error": "server did not respond"}
        return response.json()

    def _get_title(self, response) -> str:
        return response.get("title")

    def _get_episodes_counter(self, response) -> int:
        return int(response.get("episodes"))

    def _get_rank(self, response) -> Union[int, str]:
        try:
            return int(response.get("rank"))
        except TypeError:
            return "Has no rank"

    def _get_genre(self, response) -> list:
        parsed_genres = response.get("genres")
        genres = []
        for genre in parsed_genres:
            genres.append(genre.get("name"))
        return genres

    def _get_pictures(self, response) -> list:
        pictures_list = response.json().get("pictures")
        return pictures_list

    def _collect(self, response) -> dict:
        """
        This method collects all data
        :param response: HTTPResponse
        :return: dict
        """
        title = self._get_title(response)
        episodes = self._get_episodes_counter(response)
        rank = self._get_rank(response)
        genres = self._get_genre(response)
        data = {"title": title, "episodes": episodes, "genres": genres, "rank": rank}
        return data


class RandomAnimeFact:
    """
    Public interface to get random anime facts.
    """

    def __init__(self):
        self.url = "https://anime-facts-rest-api.herokuapp.com/api/v1"
        self.user_agent = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
        }

    def get_random_facts(self) -> dict:
        """
        This method makes request and calls parsers. If timeout reaches method calls self.
        :return: dict
        """
        try:
            response = requests.get(self.url, headers=self.user_agent, timeout=2)
        except ReadTimeout:
            return self.get_random_facts()
        titles = self._parse_anime_names(response)
        random_title = random.choice(titles).get("anime_name")
        request_fact = requests.get(f"{self.url}/{random_title}/")
        facts = self._parse_fact(request_fact)
        return {"anime": random_title, "facts": facts}

    def _parse_anime_names(self, response) -> list:
        titles = [title for title in response.json().get("data")]
        return titles

    def _parse_fact(self, response) -> list:
        data = response.json().get("data")
        parsed_facts = [fact.get("fact") for fact in data]
        return parsed_facts
