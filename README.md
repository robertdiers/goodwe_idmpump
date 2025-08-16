# goodwe_idmpump
using Python and TCP Modbus to send fed-in energy from GoodWe GW8K-ET to iDM AERO SLM 6-17
(iDM Option "TCP Modbus" or "Gebaedeleittechnik/Smartfox" in German Version)

### Defaults
plaese check IPs in goodwe_idm.ini file, could be overridden by Docker env variables

### Docker usage

environment variables:

INVERTER_IP (default: 192.168.1.186)

IDM_IP (default: 192.168.1.81)

IDM_PORT (default: 502)

FEED_IN_LIMIT (default: 300)

docker run -d --restart always -e INVERTER_IP=192.168.1.186 -e IDM_IP=192.168.1.81 --name goodweidmpump ghcr.io/robertdiers/goodwe_idmpump:1.0.0

### create Docker image for your architecture
./image.sh
