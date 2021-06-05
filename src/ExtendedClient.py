from binance.client import Client

class ExtendedClient(Client):
    # User Universal Transfer API を呼ぶための関数を新規作成
    def user_universal_transfer(self, **params):
        return self._request_margin_api('post', 'asset/transfer', True, data=params)