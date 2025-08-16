#!/usr/bin/env python

from datetime import datetime

import asyncio
import goodwe

import IdmPump
import Config


async def process_goodwe_data(goodwe_ip, idm_ip, idm_port, feed_in_limit):

    inverter = await goodwe.connect(goodwe_ip)
    runtime_data = await inverter.read_runtime_data()

    # active_power:            Active Power = 2948 W
    # grid_in_out:             On-grid Mode code = 1
    # grid_in_out_label:       On-grid Mode = Exporting
    # print(f"active_power: {runtime_data['active_power']}")
    # print(f"grid_in_out: {runtime_data['grid_in_out']}")
    # print(f"grid_in_out_label: {runtime_data['grid_in_out_label']}")

    feed_in = runtime_data['active_power']
    # https://github.com/marcelblijleven/goodwe/blob/master/goodwe/const.py#L34
    if feed_in > feed_in_limit and runtime_data['grid_in_out'] == 1:
        # print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " iDM feed-in reached: ", feed_in)       
        feed_in = feed_in/1000
    else:
        # print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " iDM send ZERO: ", feed_in)
        feed_in = 0

    # connection iDM
    idmval = IdmPump.writeandread(idm_ip, idm_port, feed_in)

    # for sensor in inverter.sensors():
    #     if sensor.id_ in runtime_data:
    #         print(f"{sensor.id_}: \t\t {sensor.name} = {runtime_data[sensor.id_]} {sensor.unit}")

    log_stmt = "Goodwe: " + str(runtime_data['active_power']) + ", IDM: " + str(idmval)
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " " + log_stmt)


if __name__ == "__main__":
    # print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " START #####")
    try:
        conf = Config.read()

        # read Goodwe and send to iDM
        asyncio.run(process_goodwe_data(conf["inverter_ip"], conf["idm_ip"], conf["idm_port"], conf["feed_in_limit"]))

        # print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " END #####")

    except Exception as ex:
        print("ERROR: ", ex)
