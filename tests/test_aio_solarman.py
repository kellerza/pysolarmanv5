from setup_test import SolarmanServer, AioSolarmanServer
from pysolarmanv5 import PySolarmanV5Async, NoSocketAvailableError
import asyncio
import logging

log = logging.getLogger()
# server = SolarmanServer('127.0.0.1', 8899)
server = AioSolarmanServer("127.0.0.1", 8899)


def test_async():
    async def wrapper():
        log.debug("Async starting")
        solarman = PySolarmanV5Async(
            "127.0.0.1", 2612749371, auto_reconnect=True, verbose=True, socket_timeout=2
        )
        await solarman.connect()
        log.debug("Async connected!!!")
        res = await solarman.read_holding_registers(20, 4)
        assert len(res) == 4
        res = await solarman.read_holding_registers(40, 4)
        assert len(res) == 4
        await asyncio.sleep(
            0.2
        )  # wait for auto-reconnect if enabled (see SolarmanServer)
        try:
            res = await solarman.read_holding_registers(2000, 4)
        except NoSocketAvailableError:
            await asyncio.sleep(1)
            res = await solarman.read_holding_registers(2000, 4)
        assert len(res) == 4
        await solarman.disconnect()
        log.debug("Async disconnected!!!")

    try:
        loop = asyncio.get_running_loop()
        loop.run_until_complete(wrapper())
    except RuntimeError:
        asyncio.run(wrapper())
