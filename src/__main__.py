import asyncio
import sys

import win10toast

from . import KrakenConnection


# noinspection PyShadowingNames
async def __main__(currency_pair, notification_threshold):
	notifier = win10toast.ToastNotifier()
	conn = await KrakenConnection.connect()

	# too lazy to handle None, use dummy value
	last_notified_ask = 0.1
	currency_str = "/".join(currency_pair)

	print("")

	def ticker_cb(msg):
		nonlocal last_notified_ask
		bid = float(msg[1]["b"][0])
		ask = float(msg[1]["a"][0])

		# added spaces to `end` to overwrite any leftover chars in case of longer price string
		print(f"   {currency_str}: bid({bid}), ask({ask})", end="              \r", flush=True)

		if abs(ask - last_notified_ask) > notification_threshold:
			last_notified_ask = ask
			notifier.show_toast(currency_str + " ticker",
				f"BID: {bid} {currency_pair[1]}\nASK: {ask} {currency_pair[1]}",
				None, 3, True)

	await conn.subscribe_ticker(currency_pair, ticker_cb)
	async for unhandled_msg in conn.start_listening():
		raise Exception("unhandled server message: " + str(unhandled_msg))


if __name__ == "__main__":
	currency_pair = (sys.argv[1], sys.argv[2])
	notification_threshold = float(sys.argv[3])

	try:
		asyncio.get_event_loop().run_until_complete(__main__(currency_pair, notification_threshold))
	except Exception as err:
		if not isinstance(err, SystemExit):
			# if a terminating error occurs, log it
			import traceback

			with open("./error.log", "w") as fd:
				fd.write(traceback.format_exc())
			raise
