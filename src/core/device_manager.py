import time
import core.hid_protocol as hid_protocol

def get_feature_index(device, dev_index, feature_id):
    feature_hi = (feature_id >> 8) & 0xFF
    feature_lo = feature_id & 0xFF
    packet = [0x11, dev_index, 0x00, 0x00, feature_hi, feature_lo] + [0]*14
    device.write(packet)
    start_time = time.time()
    while time.time() - start_time < 0.2:
        resp = device.read(64)
        if resp and resp[0] == 0x11 and resp[1] == dev_index and resp[2] == 0x00 and resp[3] == 0x00:
            if resp[4] != 0:
                return resp[4]
        time.sleep(0.01)
    return None

def get_device_name(device, dev_index):
    # System/Device Name Feature is 0x0005
    feature_idx = get_feature_index(device, dev_index, 0x0005)
    if not feature_idx:
        return None
        
    packet = [0x11, dev_index, feature_idx, 0x10, 0x00, 0x00] + [0]*14
    device.write(packet)
    start_time = time.time()
    while time.time() - start_time < 0.2:
        resp = device.read(64)
        if resp and resp[0] == 0x11 and resp[1] == dev_index and resp[2] == feature_idx and resp[3] == 0x10:
            chars = []
            for c in resp[4:]:
                if c == 0: break
                chars.append(chr(c))
            name = "".join(chars)
            return name
        time.sleep(0.01)
    return None

def find_devices(device):
    """
    Scans indices 1 to 6 to find the K855 Keyboard and MX Master 3S Mouse.
    Returns: (keyboard_index, mouse_index, mouse_changehost_feature_index)
    """
    keyboard_index = None
    mouse_index = None
    mouse_ch_feature = None
    
    print("Initiating dynamic device discovery on Logi Bolt receiver...")
    
    for i in range(1, 7):
        name = get_device_name(device, i)
        if name:
            print(f"  Found device at Index {i}: '{name}'")
            if "K855" in name or "Keyboard" in name:
                keyboard_index = i
            elif "Master 3S" in name or "Mouse" in name:
                mouse_index = i
                # Discover its ChangeHost feature index (0x1814)
                ch_feature = get_feature_index(device, i, 0x1814)
                if ch_feature:
                    mouse_ch_feature = ch_feature
                    print(f"    -> ChangeHost Feature resolved to {hex(ch_feature)}")
    
    return keyboard_index, mouse_index, mouse_ch_feature
