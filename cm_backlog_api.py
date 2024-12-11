import requests
import json
from typing import Dict


class CMBacklogAPI:
    """
    Backlog APIのCodeMonkey用wrapperクラス
    現段階では課題の作成のみ対応
    """
    def __init__(self, api_key: str) -> None:
        """コンストラクタ
        """
        self.SERVER_URL: str = 'https://n-contents.backlog.com/api/v2'
        self.API_KEY: str = api_key

    def _get(self, path: str, params: Dict = dict(), **kwargs) -> requests.Response:
        """BacklogAPIにgetする内部関数

        Args:
            path (str): getするエンドポイントのパス
            params (:obj:`dict`, optional): 送信する情報. Defaults to empty dict.

        Returns:
            response (requests.Response): APIのレスポンス
        """
        params['apiKey'] = self.API_KEY
        url = self.SERVER_URL + path

        return requests.get(url=url, params=params, **kwargs)

    def _post(self, path: str, params: Dict = dict(), **kwargs) -> requests.Response:
        """BacklogAPIにpostする内部関数

        Args:
            path (str): postするエンドポイントのパス
            params (:obj:`dict`, optional): 送信する情報. Defaults to empty dict.

        Returns:
            response (requests.Response): APIのレスポンス
        """
        params['apiKey'] = self.API_KEY
        url = self.SERVER_URL + path

        return requests.post(url=url, params=params, **kwargs)

    def _patch(self, path: str, params: Dict = dict(), updates: Dict = dict(), **kwargs) -> requests.Response:
        """BacklogAPIにpatchする内部関数

        Args:
            path (str): postするエンドポイントのパス
            params (:obj:`dict`, optional): 送信する情報. Defaults to empty dict.

        Returns:
            response (requests.Response): APIのレスポンス
        """
        params['apiKey'] = self.API_KEY
        url = self.SERVER_URL + path

        return requests.patch(url=url, params=params, json=updates, **kwargs)
    
    def get_issues(self, **kwargs) -> json: 
        # 無料体験
        params = {
            'issueTypeId[]': 726004,
            'count':100, #  取得上限が100
            **kwargs,
        }
        response = self._get('/issues', params=params)
        return response
    
    def update_issue(self, issue_id, params, updates):
        # idを受け取って指定し、対象の課題にUsernameとログインIDを追加
        response = self._patch(f'/issues/{issue_id}', params=params, updates=updates)
        if response.status_code == 200:
            return True, response.url, response
        else:
            return False, '', response
