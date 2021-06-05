from ExtendedClient import ExtendedClient as Client
import settings
import math

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
    
    def get_asset(self, symbol):
        try:
            value = self.client.get_asset_balance(asset=symbol)
            return value
        except Exception as e:
            print('Exception Message : {}'.format(e))
            return None
    
    def get_account_info(self):
        try:
            value = self.client.get_account()
            return value
        except Exception as e:
            print('Exception Message : {}'.format(e))
            return None
    
    def get_sub_account_info(self):
        try:
            value = self.client.get_sub_account_list()
            return value
        except Exception as e:
            print('Exception Message : {}'.format(e))
            return None

    def get_asset_details(self):
        try:
            value = self.client.get_asset_details()
            return value
        except Exception as e:
            print('Exception Message : {}'.format(e))
            return None
    
    def place_test_order(self,quantity):
        try:
            order = self.client.create_test_order(
                symbol='BETHETH',
                side='BUY',
                type='MARKET',
                quantity=quantity)
            return order
        except Exception as e:
            print('Exception Message : {}'.format(e))
            return None
    
    def place_beth_order(self,quantity):
        try:
            order = self.client.order_market_buy(
                symbol='BETHETH',
                quantity=quantity)
            return order
        except Exception as e:
            print('Exception Message : {}'.format(e))
            return None

    def transfer_eth_from_pool_to_spot(self,amount):
        try:
            transfer = self.client.user_universal_transfer(
                type='MINING_MAIN',
                asset='ETH',
                amount=amount
            )
            return transfer
        except Exception as e:
            print('Exception Message : {}'.format(e))
            return None



def main():
    binance_set = BinanceAPI()
    MIN_ORDER_ETH = 0.005

    ticker = binance_set.get_ticker('BETHETH')
    print ("==BETH→ETH==")
    print (ticker['lastPrice'])
    
    current_eth = binance_set.get_asset('ETH')['free']
    print("==財布の中の今のETH==")
    print(current_eth)

    # 市場取引ではMIN_ORDER_ETH以上の取引を受け付ける
    order_min_beth = round(MIN_ORDER_ETH / float(ticker['lastPrice']),5)

    # 最低額以上のETHが溜まっていた場合、BETHにトレードする
    if float(current_eth) >= order_min_beth:
        # 小数点以下４桁までのトレードを受け付ける
        cut_digits_num = 4
        # 今持っているETHで支払える最大量のBETHを計算
        order_quantity_beth = math.floor(round(float(current_eth) / float(ticker['lastPrice']),5) * 10 ** cut_digits_num) / (10 ** cut_digits_num)

        print("==購入予定のBETH量==")
        print(order_quantity_beth)
        order = binance_set.place_beth_order(order_quantity_beth)
        print(order)
    else:
        print("==ETHが足りないのでBETH買いません==")
    
    print("**振替テスト**")
    transfer = binance_set.transfer_eth_from_pool_to_spot(0.001)
    print(transfer)


if __name__ == '__main__':
    main()