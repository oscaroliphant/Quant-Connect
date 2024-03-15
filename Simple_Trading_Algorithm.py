# region imports
from AlgorithmImports import *
# endregion

class EmotionalYellowOwl(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2023, 5, 6)
        self.SetEndDate(2023, 6, 6)
        self.SetCash(5000)
        self.ticker = self.AddEquity("SPY", Resolution.Minute)
        self.newma = self.SMA(self.ticker.Symbol, 100)
        self.newma30 = None
        self.rsi = self.RSI(self.ticker.Symbol, 14, Resolution.Minute)
        self.Consolidate(self.ticker.Symbol, timedelta(minutes = 240), self.OnDataConsolidated)
        self.lastTradeTime = None

        self.SetWarmup(100)

    def OnData(self, data: Slice):
        pass

    def OnDataConsolidated(self, bar):
        self.currentbar = bar
        self.Plot("4 hour Chart", "Close", self.currentbar.Close)
        
        if self.newma30 is None:
            self.newma30 = self.SMA(self.ticker.Symbol, 30) # for the first value, after each minute (data point), MA is updated below using else statment
        else:
            self.newma30.Update(bar.EndTime, bar.Close) # updates new MA with end time and close price value

        if self.newma30.IsReady:
            ma30_value = self.newma30.Current.Value
            self.Plot("4 hour Chart", "30 minute MA", ma30_value)

        if self.newma30 is not None and self.newma30.IsReady:
            currentBarEndTime = self.currentbar.EndTime # The variable currentBarEndTime will now hold the value of the EndTime attribute of the self.currentbar object.
            if self.lastTradeTime is not None and currentBarEndTime - self.lastTradeTime < timedelta(minutes = 30): # if there has been a trade less than 30 mins ago, return
                return
            ma30_value = self.newma30.Current.Value
            close_price = self.currentbar.Close
            rsi = self.rsi.Current.Value

            if close_price > ma30_value and self.newma30 is not None: #and rsi > 70:
                self. SetHoldings(self.ticker.Symbol, 1)
                self.Debug("Buy Signal")  
                self.lastTradeTime = currentBarEndTime

            if close_price < ma30_value: # and rsi < 30:
                self.Liquidate(self.ticker.Symbol)
                self.Debug("Sell Signal")
                self.lastTradeTime = currentBarEndTime

"""

    def OnData(self, data: Slice) :
        if self.IsWarmingUp:
            return
       
            rsi_value = self.rsi.Current.Value

            if not self.Portfolio.Invested:
                if self.ticker.Price > self.newma30.Current.Value:
                    self.SetHoldings(self.ticker.Symbol, 1)
                    self.Debug("Buy Signal")

            if self.Portfolio.Invested:
                if self.ticker.Price < (self.Portfolio[self.ticker.Symbol].AveragePrice) * 0.9 and self.ticker.Price < self.newma150.Current.Value and rsi_value < 30:
                    self.Liquidate()
                    self.Debug("Stop Loss Signal")

                if self.ticker.Price > (self.Portfolio[self.ticker.Symbol].AveragePrice) * 1.3 and self.ticker.Price > self.newma30.Current.Value and rsi_value > 70:
                    self.Liquidate()
                    self.Debug("Take Profit Signal")

            self.Plot("SPY", "MA30", self.newma30.Current.Value)
            self.Plot("SPY", "MA150", self.newma150.Current.Value)
            self.Plot("SPY", "SPY", self.ticker.Price)

def OnOrderEvent(self, OnOrderEvent):
    #order = self.Transaction.GetOrderById(OrderEvent.OrderId)
    #self.Log("{0}: {1}: {2}".format(self.Time, order.Type, orderEvent))