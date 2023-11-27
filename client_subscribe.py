import logging
import asyncio

from amqtt.client import MQTTClient, ClientException
from amqtt.mqtt.constants import QOS_1, QOS_2

import time

#
# This sample shows how to subscbribe a topic and receive data from incoming messages
# It subscribes to '$SYS/broker/uptime' topic and displays the first ten values returned
# by the broker.
#

logger = logging.getLogger(__name__)


async def uptime_coro():
    C = MQTTClient()
    await C.connect("mqtt://192.168.1.12/")
    # Subscribe to '$SYS/broker/uptime' with QOS=1
    await C.subscribe(
        [
            ("iOT/dbLevel", QOS_1),
        ]
    )
    logger.info("Subscribed")
    try:
        i = 0
        start_time = time.time()
        while True:
            message = await C.deliver_message()
            packet = message.publish_packet
            i+=1
            now = time.time()
            if now-start_time >= 1:
                elapsed_time = now - start_time
                loops_per_second = i / elapsed_time
                logging.info(f"Messages/second: {loops_per_second}")
                logging.info(
                    "%d: %s => %s"
                    % (i, packet.variable_header.topic_name, str(packet.payload.data))
                )
                start_time = now
                i=0
        await C.unsubscribe(["iOT/dbLevel"])
        logger.info("UnSubscribed")
        await C.disconnect()
    except ClientException as ce:
        logger.error("Client exception: %s" % ce)


if __name__ == "__main__":
    formatter = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(uptime_coro())