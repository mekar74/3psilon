import json
from dataclasses import dataclass
from typing import List, Optional

import requests
from colorama import Fore, Style
from dacite import from_dict
from decode import decode
from game.models import Board, Bot
from requests import Response


@dataclass
class Api:
    url: str

    def _get_url(self, endpoint: str) -> str:
        return "{}{}".format(self.url, endpoint)

    def _req(self, endpoint: str, method: str, body: dict) -> Response:
        print(
            ">>> {} {} {}".format(
                Style.BRIGHT + method.upper() + Style.RESET_ALL,
                Fore.GREEN + endpoint + Style.RESET_ALL,
                body,
            )
        )
        func = getattr(requests, method)
        headers = {"Content-Type": "application/json"}
        res = func(self._get_url(endpoint), headers=headers, data=json.dumps(body))
        if res.status_code == 200:
            print("<<< {} OK".format(res.status_code))
        else:
            print("<<< {} {}".format(res.status_code, res.text))
        return res

    def _return_response_and_status(self, response: Response):
        response_data = json.loads(response.text)  # ubah string jadi dict
        return decode(response_data), response.status_code

    def bots_get(self, bot_token: str) -> Optional[Bot]:
        response = self._req("/bots/{}".format(bot_token), "get", {})
        data, status = self._return_response_and_status(response)
        if status == 200:
            return from_dict(Bot, data)
        return None

    def bots_register(
        self, name: str, email: str, password: str, team: str
    ) -> Optional[Bot]:
        response = self._req(
            "/bots",
            "post",
            {"email": email, "name": name, "password": password, "team": team},
        )
        resp, status = self._return_response_and_status(response)
        if status == 200:
            return from_dict(Bot, resp)
        return None

    def boards_list(self) -> Optional[List[Board]]:
        response = self._req("/boards", "get", {})
        resp, status = self._return_response_and_status(response)
        if status == 200:
            return [from_dict(Board, board) for board in resp]
        return None

    def bots_join(self, bot_token: str, board_id: int) -> bool:
        response = self._req(
            f"/bots/{bot_token}/join", "post", {"preferredBoardId": board_id}
        )
        resp, status = self._return_response_and_status(response)
        return status == 200

    def boards_get(self, board_id: str) -> Optional[Board]:
        response = self._req("/boards/{}".format(board_id), "get", {})
        resp, status = self._return_response_and_status(response)
        if status == 200:
            return from_dict(Board, resp)
        return None

    def bots_move(self, bot_token: str, direction: str) -> Optional[Board]:
        response = self._req(
            "/bots/{}/move".format(bot_token),
            "post",
            {"direction": direction},
        )
        resp, status = self._return_response_and_status(response)
        if status == 200:
            return from_dict(Board, resp)
        return None

    def bots_recover(self, email: str, password: str) -> Optional[str]:
        try:
            response = self._req(
                "/bots/recover", "post", {"email": email, "password": password}
            )
            resp, status = self._return_response_and_status(response)
            if status == 201:
                return resp["id"]
            return None
        except:
            return None
