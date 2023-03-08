#!/usr/bin/env python3

import serial
import minimalmodbus


def coll_rtu(addrs: dict, port: str = 'COM1', baudrate: int = 9600, bytesize: int = 8, parity: str = serial.PARITY_NONE, stopbits: int = 1, timeout: float = 0.1, mode: str = minimalmodbus.MODE_RTU) -> dict:
    """Collect a list of modbus address in serial and slave node

    Args:
        addrs (dict of tuple(address:int,address:int), optional): _description_. Example {'Addr': (address, address)}.
        port (str, optional): _description_. Defaults to 'COM1'.
        slave (int, optional): _description_. Defaults to 1.
        baudrate (int, optional): _description_. Defaults to 9600.
        bytesize (int, optional): _description_. Defaults to 8.
        parity (_type_, optional): _description_. Defaults to serial.PARITY_NONE.
        stopbits (int, optional): _description_. Defaults to 1.
        timeout (float, optional): _description_. Defaults to 0.1.
    Returns:
        dict of str: List of values related with addrs argument
    """
    cli = minimalmodbus.Instrument(port=port, slaveaddress=0, mode=mode)
    cli.serial.baudrate = baudrate
    cli.serial.bytesize = bytesize
    cli.serial.parity = parity
    cli.serial.stopbits = stopbits
    cli.serial.timeout = timeout
    cli.clear_buffers_before_each_transaction = True

    for i in addrs:
        cli.address = addrs[i][2]
        addrs[i] = cli.read_register(
            registeraddress=addrs[i][0], functioncode=addrs[i][1])

    cli.close_port_after_each_call = True

    return addrs

addrs = {
    'Temperature': (1, 4, 1),
    'Humidy': (2, 4, 1),
}
print(coll_rtu(addrs, 'COM4'))
