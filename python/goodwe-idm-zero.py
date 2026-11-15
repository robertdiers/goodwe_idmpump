#!/usr/bin/env python

from datetime import datetime

import time

import IdmPump
import Config

# emergency write: try hard to get a 0 to the iDM
MAX_ATTEMPTS = 5
RETRY_DELAY = 10


def log(msg):
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " " + msg)


if __name__ == "__main__":
    # no goodwe/inverter access here on purpose,
    # this must work even if the regular script is broken
    try:
        conf = Config.read()

        for attempt in range(1, MAX_ATTEMPTS + 1):
            idmval = IdmPump.writeandread(conf["idm_ip"], conf["idm_port"], 0)

            if idmval == 0:
                log("EMERGENCY zero -> IDM: " + str(idmval)
                    + " (attempt " + str(attempt) + "/" + str(MAX_ATTEMPTS) + ")")
                break

            log("EMERGENCY zero -> IDM: attempt " + str(attempt) + "/"
                + str(MAX_ATTEMPTS) + " did not return 0 (got: "
                + str(idmval) + ")")
            if attempt < MAX_ATTEMPTS:
                time.sleep(RETRY_DELAY)
        else:
            log("EMERGENCY zero -> IDM: FAILED after "
                + str(MAX_ATTEMPTS) + " attempts")

    except Exception as ex:
        print("ERROR: ", ex)
