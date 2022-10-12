
import yfinance as yf
import datetime  # For datetime objects
import pandas as pd
import backtrader as bt
import numpy as np

# Create a Stratey
class MyStrategy(bt.Strategy):
    params = (
        ('ssa_window', 15),
        ('maperiod', 15),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        # self.ssa = ssa_index_ind(
        #     self.datas[0], ssa_window=self.params.ssa_window)
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)


    def next(self):
        if self.order:
            return
        if not self.position:
            if self.dataclose[0] > self.sma[0]:
                self.order = self.buy()

        else:

            if self.dataclose[0] < self.sma[0]:
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()

    def stop(self):
        self.log('(MA Period %2d) Ending Value %.2f' %
                 (self.params.maperiod, self.broker.getvalue()))


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.optstrategy(
        MyStrategy,
        maperiod=range(10, 31))
    data = bt.feeds.PandasData(dataname=yf.download('600466.SS', '2015-07-06', '2021-09-23', auto_adjust=True))
    cerebro.adddata(data)
    cerebro.broker.setcash(10000.0)
    # cerebro.addsizer(bt.sizers.FixedSize, stake=1)
    cerebro.broker.setcommission(commission=0.0)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # cerebro.plot()  'OptReturn' object has no attribute 'datas'


