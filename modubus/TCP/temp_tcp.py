from pymodbus.client import ModbusTcpClient

def coll_tcp(addrs: dict, host: str) -> dict:
    """Collect a list of modbus address in TCP/IP Address

    Args:
        addrs (dict of tuple(address:int,address:int), optional): _description_. Example {'Addr': (address, address, slave)}.
        host (str, optional): _description_.
    Returns:
        dict of str: List of values related with addrs argument
    """
    cli = ModbusTcpClient(host)
    dictFnCode={
        1:cli.read_coils,
        2:cli.read_discrete_inputs,
        3:cli.read_holding_registers,
        4:cli.read_input_registers,
        7:cli.read_exception_status,
        14:cli.read_device_information,
        20:cli.read_file_record,
        24:cli.read_fifo_queue,
    }
    cli.clear_buffers_before_each_transaction = True
    cli.connect()
    
    for i in addrs:
        result = dictFnCode[addrs[i][1]](address=addrs[i][0],count=1,slave=addrs[i][2])
        addrs[i] = result.getRegister(0)

    cli.close_port_after_each_call = True
    cli.close()

    return addrs

addrs = {
    'Temperature': (1, 4, 1),
    'Humidy': (2, 4, 1),
}
print(coll_tcp(addrs,'192.168.1.45'))

