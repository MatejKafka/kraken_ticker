# kraken_ticker: Kraken market ticker
Small library/CLI that connects to Kraken exchange websocket API
and exposes a simple API for subscribing to tickers
and creating custom handlers.

## API
Currently undocumented, but the code should be reasonably readable. See
https://docs.kraken.com/websockets/ for documentation on the passed
message format (the library just parses the JSON, no other processing is done).
When sending, sequentially generated `reqid` is automatically
added to all sent messages.

## CLI usage
Also works as a console notifier on Windows 10 - when launched directly,
current market rates are shown in console and if a provided threshold is
crossed, a toast notification is shown.

**Usage:** `py -m src <CURRENCY_1> <CURRENCY_2> <THRESHOLD>` (see `run.ps1` for example).

`<CURRENCY_1>` and `CURRENCY_2>` are the market pair you want a ticker
for (e.g. "XBT" "EUR").

`THRESHOLD` is the delta from last displayed
ask price that must be crossed to show a notification (e.g. if threshold is 1 and
last notification was shown when market rate was 500, next notification
will be shown when crossing 499 or 501).

![Windows 10 notification](https://i.imgur.com/MlbqHK2.png)

## Dependencies:
 - `win10toast`
 - `websockets`

(see `requirements.txt`)
