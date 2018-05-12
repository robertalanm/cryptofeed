'''
Copyright (C) 2017-2018  Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
'''
from cryptofeed.callback import TickerCallback, TradeCallback, BookCallback
from cryptofeed import FeedHandler
from cryptofeed import Bitmex, GDAX, Bitfinex, Poloniex, Gemini, HitBTC, Bitstamp
from cryptofeed.defines import L3_BOOK, L2_BOOK, BID, ASK, TRADES, TICKER


# Examples of some handlers for different updates. These currently don't do much.
# Handlers should conform to the patterns/signatures in callback.py
# Handlers can be normal methods/functions or async. The feedhandler is paused
# while the callbacks are being handled (unless they in turn await other functions or I/O)
# so they should be as lightweight as possible
async def ticker(feed, pair, bid, ask):
    print('Feed: {} Pair: {} Bid: {} Ask: {}'.format(feed, pair, bid, ask))



async def trade(feed, pair, id, side, amount, price):
    if id:
        print("Feed: {} Pair: {} ID: {} Side: {} Amount: {} Price: {}".format(feed, pair, id, side, amount, price))
    else:
        print("Feed: {} Pair: {} Side: {} Amount: {} Price: {}".format(feed, pair, side, amount, price))


async def book(feed, pair, book):
        print('Feed: {} Pair: {} Book Bid Size is {} Ask Size is {}'.format(feed, pair, len(book[BID]), len(book[ASK])))


def main():
    f = FeedHandler()
    f.add_feed(GDAX(pairs=['BTC-USD'], channels=[L3_BOOK], callbacks={L3_BOOK: BookCallback(book)}))
    f.add_feed(Bitfinex(pairs=['BTC-USD'], channels=[L3_BOOK], callbacks={L3_BOOK: BookCallback(book)}))
    f.add_feed(Poloniex(channels=[TICKER, 'USDT-BTC'], callbacks={L3_BOOK: BookCallback(book), TICKER: TickerCallback(ticker)}))
    f.add_feed(Gemini(pairs=['BTC-USD'], callbacks={L3_BOOK: BookCallback(book), TRADES: TradeCallback(trade)}))
    f.add_feed(HitBTC(channels=[TRADES], pairs=['BTC-USD'], callbacks={TRADES: TradeCallback(trade)}))
    f.add_feed(Bitstamp(channels=[L3_BOOK, TRADES], pairs=['BTC-USD'], callbacks={L3_BOOK: BookCallback(book), TRADES: TradeCallback(trade)}))

    bitmex_symbols = Bitmex.get_active_symbols()
    f.add_feed(Bitmex(channels=[TRADES], pairs=bitmex_symbols, callbacks={TRADES: TradeCallback(trade)}))
    f.add_feed(Bitmex(pairs=['XBTUSD'], channels=[L2_BOOK], callbacks={L2_BOOK: BookCallback(book)}))
    f.run()


if __name__ == '__main__':
    main()
