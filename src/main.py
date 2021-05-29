from binance.client import Client
import settings

class BinanceAPI:

    def __init__(self):
        API_KEY = settings.BINANCE_API_KEY
        API_SECRET = settings.BINANCE_API_SECRET

        self.client = Client(API_KEY, API_SECRET)

    def get_ticker(self, pair):
        try:
            value = self.client.get_ticker(symbol=pair)
            return value
        except Exception as e:
            print('Exception Message : {}'.format(e))
            return None

def main():
    binance_set = BinanceAPI()

    ticker = binance_set.get_ticker('BTCUSDT')
    print (ticker['lastPrice'])

if __name__ == '__main__':
    main()