# region imports
from AlgorithmImports import *
# endregion

class JumpingBlackBaboon(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2022, 1, 6)
        self.SetEndDate(2022, 6, 6)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.SelectionFilter)
        self.UniverseSettings.Leverage = 2 # allows holdings of twice capital by borrowing from broker - extra gain but extra risk
        # self.SetSecurityInitializer(lambda x: x.SetFeeModel(ConstantFeeModel(0))) # removes trading fees

    def SelectionFilter(self, coarse):
        sortedvol = sorted(coarse, key = lambda x: x.DollarVolume, reverse = True)
        filtered = [x.Symbol for x in sortedvol if x.Price > 50]
        return filtered[:10]

    def OnSecuritiesChanged(self, changes):
        self.changes = changes
        self.Log(f"Securities changed on {self.Time}: {changes}")

        for security in changes.RemovedSecurities: # ensures only invested in top 10 securities
            if security.Invested:
                self.Liquidate(security.Symbol)

        for security in changes.AddedSecurities:
            if not security.Invested:
                self.SetHoldings(security.Symbol, 0.1)