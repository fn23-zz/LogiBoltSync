import hid

LOGI_VID = 0x046D
BOLT_PID = 0xC548

def get_hidpp_interfaces():
    """
    Returns a dictionary with matching HID++ paths for the Logi Bolt receiver.
    col01 is used for monitoring (it reports ERROR_0x10 on disconnect).
    col02 is used for control (it is not blocked by Logi Options+).
    """
    interfaces = {'col01': None, 'col02': None}
    for d in hid.enumerate(LOGI_VID, BOLT_PID):
        if d['usage_page'] == 0xFF00:
            if d['usage'] == 0x0001:
                interfaces['col01'] = d['path']
            elif d['usage'] == 0x0002:
                interfaces['col02'] = d['path']
    return interfaces

def open_bolt_device(path):
    device = hid.device()
    device.open_path(path)
    device.set_nonblocking(1)
    
    # clear unread buffer
    while device.read(64):
        pass
        
    return device
