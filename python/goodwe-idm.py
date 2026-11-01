#!/usr/bin/env python

from datetime import datetime

import asyncio
import goodwe

import IdmPump
import Config


async def process_goodwe_data(goodwe_ip, idm_ip, idm_port, feed_in_limit):

    inverter = await goodwe.connect(goodwe_ip)
    runtime_data = await inverter.read_runtime_data()

    # ET/EH/BT/BH inverters report active_power,
    # ES/EM/BP inverters (e.g. GW5048D-ES) report pgrid.
    # grid_in_out:  0 = Idle, 1 = Exporting, 2 = Importing
    if 'active_power' in runtime_data:
        grid_power = runtime_data['active_power']
    else:
        grid_power = runtime_data['pgrid']

    # https://github.com/marcelblijleven/goodwe/blob/master/goodwe/const.py#L34
    if grid_power > feed_in_limit and runtime_data.get('grid_in_out') == 1:
        feed_in = grid_power/1000
    else:
        feed_in = 0

    # connection iDM
    idmval = IdmPump.writeandread(idm_ip, idm_port, feed_in)

    # for sensor in inverter.sensors():
    #     if sensor.id_ in runtime_data:
    #         print(f"{sensor.id_}: \t\t {sensor.name} = {runtime_data[sensor.id_]} {sensor.unit}")

    log_stmt = "Goodwe (" + inverter.model_name + "): " + str(grid_power) + ", IDM: " + str(idmval)
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " " + log_stmt)


if __name__ == "__main__":
    # print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " START #####")
    try:
        conf = Config.read()

        # read Goodwe and send to iDM
        asyncio.run(process_goodwe_data(conf["inverter_ip"], conf["idm_ip"],
                                        conf["idm_port"], conf["feed_in_limit"]
                                        ))

        # print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " END #####")

    except Exception as ex:
        print("ERROR: ", ex)
