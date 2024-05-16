import time
from fastapi_socketio import SocketManager
from .engine import Engine
from .bindings import MiddlewareWork, MWStatus, MWSignal, MWClient


class SocketHandler:
    def __init__(self, socket_manager: SocketManager):
        self.sio = socket_manager

        self.sio.on("connect", self.sio_connect)
        self.sio.on("disconnect", self.sio_disconnect)

        self.sio.on("*", self.catch_all)

        self.db = {}

    async def catch_all(self, event_name: str, sid: str, data: dict):
        print(f"{event_name} called by {sid} with data = {data}")

        now = time.time_ns() / 1_000_000
        ping = now - data["time"]
        del data["time"]

        if not data.get("id") or not self.db.get(data["id"]):
            engine = Engine()
            print("NEW ENGINE CREATED")
        else:
            engine = self.db[data["id"]]["engine"]
            del data["id"]

        work: MiddlewareWork = getattr(engine, event_name)(**data)

        if work.status == MWStatus.ERROR:
            return {"error": True, "reason": work.status_msg}, ping

        if not self.db.get(engine.state.id):
            self.db[engine.state.id] = {"engine": None, "clients": [], "room": ""}

        self.db[engine.state.id]["engine"] = engine

        if work.client == MWClient.APPEND:
            self.db[engine.state.id]["clients"].append(
                {"sid": sid, "local_id": work.client_id}
            )
        elif work.client == MWClient.REMOVE:
            for i in range(len(self.db[engine.state.id]["clients"])):
                if self.db[engine.state.id]["clients"][i]["sid"] == sid:
                    del self.db[engine.state.id]["clients"][i]
                    break

            self.db[engine.state.id]["clients"].remove(sid)

        if work.signal == MWSignal.BROADCAST:
            await self.sio.emit(work.signal_name, work.signal_content)
            return

        if work.signal == MWSignal.CLIENT_AND_BROADCAST:
            print(f"EMMITING {work.signal_name} with content={work.signal_content}")
            for client in self.db[engine.state.id]["clients"]:
                if client["sid"] != sid:
                    print(f"    sending to client {client['sid']}")
                    await self.sio.emit(
                        work.signal_name, work.signal_content, client["sid"]
                    )

        if work.signal in [MWSignal.CLIENT, MWSignal.CLIENT_AND_BROADCAST]:
            for client in self.db[engine.state.id]["clients"]:
                if client["sid"] == sid:
                    return engine.player_state(client["local_id"]), ping

    def sio_connect(self, *args):
        print("client connected")

    def sio_disconnect(self, *args):
        print("client disconnected")
