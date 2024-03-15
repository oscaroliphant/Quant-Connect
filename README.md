<span style="text-decoration: underline;">Top_10_Securities:</span>
Initialization: Sets up backtesting parameters, including start and end dates, cash allocation, and resolution.
Selection Filter: Filters a universe of assets based on dollar volume and price, selecting the top 10 symbols.
OnSecuritiesChanged: Liquidates positions for removed securities and sets holdings for newly added securities to 10% of the portfolio.

<span style="text-decoration: underline;">Simple Trading Algo:</span>
Initialization: Sets up parameters for trading, such as start and end dates, cash allocation, and indicator settings.
OnDataConsolidated: Consolidates minute data into 4-hour bars, calculates indicators, and generates buy/sell signals based on SMA and RSI conditions.
OnOrderEvent: Handles order events, although it's currently commented out in the code.

Note: This code is designed for backtesting trading strategies on the QuantConnect platform, utilizing features like universe selection, leverage, and handling security changes.

