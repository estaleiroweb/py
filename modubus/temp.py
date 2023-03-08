#!/usr/bin/env python3

import serial
import minimalmodbus
from pymodbus.client import ModbusTcpClient


def coll_rtu(dictAddress: dict, port: str = 'COM1', baudrate: int = 9600, bytesize: int = 8, parity: str = serial.PARITY_NONE, stopbits: int = 1, timeout: float = 0.1, mode: str = minimalmodbus.MODE_RTU) -> dict:
    """Collect a list of modbus address in serial and slave node

    Args:
        dictAddress (dict of tuple(address:int,address:int), optional): _description_. Example {'Addr': (address, address, slave)}.
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

    out = {}
    for i in dictAddress:
        rAddr = dictAddress[i][0]
        fnCod = dictAddress[i][1]
        slave = dictAddress[i][2]
        cli.address = slave
        out[i] = cli.read_register(rAddr, 0, fnCod)

    cli.close_port_after_each_call = True

    return out


def coll_tcp(dictAddress: dict, host: str) -> dict:
    """Collect a list of modbus address in TCP/IP Address

    Args:
        dictAddress (dict of tuple(address:int,address:int), optional): _description_. Example {'Addr': (address, address, slave)}.
        host (str, optional): _description_.
    Returns:
        dict of str: List of values related with addrs argument
    """
    cli = ModbusTcpClient(host)
    dictFnCode = {
        1: cli.read_coils,
        2: cli.read_discrete_inputs,
        3: cli.read_holding_registers,
        4: cli.read_input_registers,
        7: cli.read_exception_status,
        14: cli.read_device_information,
        20: cli.read_file_record,
        24: cli.read_fifo_queue,
    }
    cli.clear_buffers_before_each_transaction = True
    cli.connect()

    out = {}
    for i in dictAddress:
        rAddr = dictAddress[i][0]
        fnCod = dictAddress[i][1]
        slave = dictAddress[i][2]

        result = dictFnCode[fnCod](address=rAddr, count=1, slave=slave)
        out[i] = result.getRegister(0)

    cli.close_port_after_each_call = True
    cli.close()

    return out


addrs = {
    # name: (Address,functionCode,Slave),
    'Temperature': (1, 4, 1),
    'Humidy': (2, 4, 1),
}
print({
    'TCP': coll_tcp(addrs, '192.168.1.45'),
    'RTU': coll_rtu(addrs, 'COM4'),
})
