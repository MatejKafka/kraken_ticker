# kraken_ticker: Kraken market ticker
Small library/CLI that connects to Kraken exchange websocket API
and exposes a simple API for subscribing to tickers
and creating custom handlers.

Also works as a console notifier on Windows 10 - when launched directly
as `py -m src <CURRENCY_1> <CURRENCY_2> <THRESHOLD>`
(see `run.ps1` for example), where CURRENCY 1 and 2 are the market
pair you want a ticker for (e.g. "XBT" "EUR"),
and THRESHOLD is the change relative to last displayed
ask price that must be crossed to notify, the app prints latest ask/bid prices
to console and if threshold is crossed, a system toast notification is shown.

![Windows 10 notification](https://i.imgur.com/MlbqHK2.png)

## Dependencies:
 - `win10toast`
 - `websockets`
(see `requirements.txt`)
