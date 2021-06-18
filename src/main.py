from ExtendedClient import ExtendedClient as Client
from linebot import LineBotApi
from linebot.models import TextSendMessage
import settings
import math
import time
import datetime

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
    
    def get_mining_payment_list(self):
        try:
            payment_list = self.client.mining_payment_list(
                algo=settings.MINING_ALGO,
                userName=settings.MINING_USER_NAME
            )
            return payment_list
        except Exception as e:
            print('Exception Message : {}'.format(e))
            return None
    
    def get_latest_mining_amount(self):
        payment_list = self.get_mining_payment_list()
        
        # 1個目のリストを取得（手抜き。担保されていない気がするけど、多分最新。）
        return payment_list['data']['accountProfits'][0]['profitAmount']

class LineBotMessagingApi:

    def __init__(self):
        LINE_CHANNEL_ACCESS_TOKEN = settings.LINE_CHANNEL_ACCESS_TOKEN
        
        self.line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    
    def push_message(self,user_id,message_string):
        try:
            messages = TextSendMessage(text=message_string)
            self.line_bot_api.push_message(user_id, messages=messages)
            return None

        except Exception as e:
            print('Exception Message : {}'.format(e))
            return None



def main():
    binance_set = BinanceAPI()
    MIN_ORDER_ETH = 0.005

    line_bot = LineBotMessagingApi()
    
    # 日本時間のタイムゾーンに合わせたdatetime取得
    dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    result_line_message = dt_now.strftime('%Y年%m月%d日') + "の採掘結果\n"

    ticker = binance_set.get_ticker('BETHETH')
    print ("==BETH→ETH相場==")
    print (ticker['lastPrice'])

    print ("==最新のMining収益(ETH)==")
    latest_mining_amount = binance_set.get_latest_mining_amount()
    print(latest_mining_amount)
    result_line_message += "==稼いだETH==\n" + str(latest_mining_amount) + "(〇〇円:未実装)\n"
    
    print("==miningウォレットからspotウォレットへの振替実行開始==")
    transfer_eth_amount = latest_mining_amount
    transfer = binance_set.transfer_eth_from_pool_to_spot(transfer_eth_amount)
    
    # 振替に必要な額が足りない場合、Noneが返却されるのでそれで区別する
    if transfer is None:
        print("==本日振替済みなので、振替実施しませんでした==")
        result_line_message += "==振替はしなかったよ==\n"
    else:
        print("==振替完了(振替ETH={0[0]} tranId={0[1]})==".format([transfer_eth_amount,transfer['tranId']]))
        result_line_message += "==振替成功したよ==\n"

    current_eth = binance_set.get_asset('ETH')['free']
    print("==財布の中の今のETH==")
    print(current_eth)
    result_line_message += "==今のETH保持数==\n" + str(current_eth) + "(〇〇円:未実装)\n"

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
        result_line_message += "==BETHこれだけ買うよ==\n" + str(order_quantity_beth) + "\n"
    else:
        print("==ETHが足りないのでBETH買いません==")
        result_line_message += "==ETHが足りないよ=="

    # 結果をLineBot経由でPUSH通知
    user_id = settings.LINE_USER_ID
    line_bot.push_message(user_id, result_line_message)

if __name__ == '__main__':
    main()