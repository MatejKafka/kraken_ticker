from __future__ import annotations

import itertools
import json
from typing import Union, Dict, Callable, List, Tuple

import websockets


class KrakenConnection:
	KRAKEN_URL = "wss://ws.kraken.com"

	WS = websockets.WebSocketClientProtocol
	ParsedMsg = Union[dict, list]
	SentMsg = Dict
	Handler = Callable[[ParsedMsg], bool]
	ReqID = int

	_ws: WS
	_handlers: List[Handler]
	_reqid_iter: iter

	def __init__(self, ws: WS):
		self._ws = ws
		self._handlers = []
		# Kraken allows to add request id, which is echoed in related response
		self._reqid_iter = itertools.count()
		self.add_handler(KrakenConnection._heartbeat_handler)
		self.add_handler(KrakenConnection._system_status_handler)

	@staticmethod
	def _heartbeat_handler(msg: ParsedMsg):
		return "event" in msg and msg["event"] == "heartbeat"

	@staticmethod
	def _system_status_handler(msg: ParsedMsg):
		return "event" in msg and msg["event"] == "systemStatus"

	@staticmethod
	async def connect() -> KrakenConnection:
		ws = await websockets.connect(KrakenConnection.KRAKEN_URL)
		return KrakenConnection(ws)

	async def start_listening(self):
		while True:
			raw_msg = await self._ws.recv()
			msg: KrakenConnection.ParsedMsg = json.loads(raw_msg)
			# copy to allow removing handlers during iteration
			handlers = self._handlers.copy()
			for handler in handlers:
				if handler(msg): break
			else:
				# message not handled by any handler
				yield msg

	async def send(self, msg: SentMsg) -> ReqID:
		if type(msg) is not dict:
			raise Exception("send can currently only accept a dictionary")
		reqid = self._reqid_iter.__next__()
		msg_with_id = dict(reqid=reqid, **msg)
		await self._ws.send(json.dumps(msg_with_id))
		return reqid

	def remove_handler(self, handler_ref: Handler):
		self._handlers.remove(handler_ref)

	def add_handler(self, handler: Handler):
		self._handlers.append(handler)

	def add_once_handler(self, handler: Handler):
		def h(msg):
			if handler(msg):
				self.remove_handler(h)
				return True
			return False

		self.add_handler(h)

	def add_response_handler(self, req_id: ReqID, handler: Callable[[ParsedMsg], None]):
		def h(msg):
			if type(msg) is not dict or "reqid" not in msg \
					or msg["reqid"] != req_id:
				return False
			handler(msg)
			return True

		self.add_once_handler(h)

	async def subscribe_ticker(self, currency_pair: Tuple[str, str],
			ticker_cb: Callable[[ParsedMsg], None]):
		req_id = await self.send(dict(
			event="subscribe",
			pair=["/".join(currency_pair)],
			subscription=dict(
				name="ticker"
			)
		))

		channel_id = None

		def confirmation_handler(msg):
			nonlocal channel_id
			channel_id = msg["channelID"]
			self.add_handler(subscription_handler)

		def subscription_handler(msg):
			nonlocal channel_id
			if type(msg) is not list:
				return False
			if msg[0] != channel_id:
				return False
			ticker_cb(msg)
			return True

		self.add_response_handler(req_id, confirmation_handler)
