#!/usr/bin/env python

import configparser
import os

# read config
config = configparser.ConfigParser()


def read():
    try:
        # read config
        config.read('goodwe-idm.ini')

        values = {}

        values["idm_ip"] = config['IdmSection']['idm_ip']
        values["idm_port"] = int(config['IdmSection']['idm_port'])
        values["feed_in_limit"] = int(config['IdmSection']['feed_in_limit'])
        if os.getenv('IDM_IP', 'None') != 'None':
            values["idm_ip"] = os.getenv('IDM_IP')
            # print ("using env: IDM_IP")
        if os.getenv('IDM_PORT', 'None') != 'None':
            values["idm_port"] = int(os.getenv('IDM_PORT'))
            # print ("using env: IDM_PORT")
        if os.getenv('FEED_IN_LIMIT', 'None') != 'None':
            values["feed_in_limit"] = int(os.getenv('FEED_IN_LIMIT'))
            # print ("using env: FEED_IN_LIMIT")

        values["inverter_ip"] = config['GoodweSection']['inverter_ip']
        if os.getenv('INVERTER_IP', 'None') != 'None':
            values["inverter_ip"] = os.getenv('INVERTER_IP')
            # print ("using env: INVERTER_IP")

        # print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " config: ", values)

        return values
    except Exception as ex:
        print("ERROR Config: ", ex)
