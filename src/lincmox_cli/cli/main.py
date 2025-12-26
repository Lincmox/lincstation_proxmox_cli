#!/usr/bin/env python3
import os

from lincmox_driver.i2c import I2C, I2CBackendMock
from lincmox_driver.lincstation import LincStationController as LincStation
from .cli import CLI

def main():
    env = os.getenv("LINCMOX_ENV", "prod")
    is_simulation = env == "dev"
    lincstation = LincStation(simulation=is_simulation)

    CLI(lincstation).with_status_cmd() \
                    .with_power_cmd() \
                    .with_sata_cmd() \
                    .with_nvme_cmd() \
                    .with_network_cmd() \
                    .with_strip_cmds() \
                    .with_reset_cmd() \
                    .build();
                          
if __name__ == "__main__":
    main()