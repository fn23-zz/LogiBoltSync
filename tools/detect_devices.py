import sys
import os
import time
import json

# Add src to path so we can use core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from core import hid_protocol

def get_feature_index(device, dev_index, feature_id):
    feature_hi = (feature_id >> 8) & 0xFF
    feature_lo = feature_id & 0xFF
    packet = [0x11, dev_index, 0x00, 0x00, feature_hi, feature_lo] + [0]*14
    
    for attempt in range(3):
        try:
            device.write(packet)
        except Exception as e:
            time.sleep(0.1)
            continue
            
        start_time = time.time()
        while time.time() - start_time < 0.3:
            resp = device.read(64)
            if resp and resp[0] == 0x11 and resp[1] == dev_index and resp[2] == 0x00 and resp[3] == 0x00:
                if resp[4] != 0:
                    return resp[4]
            time.sleep(0.01)
    return None

def get_device_name(device, dev_index):
    for attempt in range(3):
        # Wake up ping
        ping_packet = [0x10, dev_index, 0x00, 0x10, 0x00, 0x00, 0x00]
        try: device.write(ping_packet)
        except: pass
        time.sleep(0.1)
        
        # SystemName/DeviceName feature is 0x0005
        feature_idx = get_feature_index(device, dev_index, 0x0005)
        if not feature_idx:
            continue
            
        # Function 0: get length
        packet = [0x11, dev_index, feature_idx, 0x00, 0x00, 0x00] + [0]*14
        device.write(packet)
        length = 0
        start_time = time.time()
        while time.time() - start_time < 0.3:
            resp = device.read(64)
            if resp and resp[0] == 0x11 and resp[1] == dev_index and resp[2] == feature_idx and resp[3] == 0x00:
                length = resp[4]
                break
            time.sleep(0.01)
            
        if length == 0:
            continue
            
        # Function 1: get name
        packet = [0x11, dev_index, feature_idx, 0x10, 0x00, 0x00] + [0]*14
        device.write(packet)
        start_time = time.time()
        while time.time() - start_time < 0.3:
            resp = device.read(64)
            if resp and resp[0] == 0x11 and resp[1] == dev_index and resp[2] == feature_idx and resp[3] == 0x10:
                chars = []
                for c in resp[4:]:
                    if c == 0: break
                    chars.append(chr(c))
                name = "".join(chars).strip()
                if name:
                    return name
            time.sleep(0.01)
            
    return None

def main():
    print("--- LogiBoltSync Device Detector ---")
    interfaces = hid_protocol.get_hidpp_interfaces()
    if not interfaces['col02']:
        print("Error: Could not find Logi Bolt Col02 interface.")
        return
        
    print(f"Opening interface: {interfaces['col02']}")
    try:
        device = hid_protocol.open_bolt_device(interfaces['col02'])
    except Exception as e:
        print(f"Failed to open device: {e}")
        return

    detected_keyboard = None
    detected_mouse = None

    print("\nScanning Device Indices (1-6)...")
    for i in range(1, 7):
        # We need to wake up the device or just query its name
        name = get_device_name(device, i)
        if name:
            print(f"  [Index {i}] Found Device: {name}")
            if "K855" in name or "Keyboard" in name:
                detected_keyboard = i
            elif "Master 3S" in name or "Mouse" in name:
                detected_mouse = i
        else:
            print(f"  [Index {i}] Empty or Offline")

    device.close()
    
    print("\n--- Configuration Generation ---")
    if detected_keyboard and detected_mouse:
        print("Successfully identified Keyboard and Mouse indices.")
        
        target_slot = input(f"Enter the Target Mouse Slot to switch to when Keyboard disconnects (1, 2, or 3): ").strip()
        if target_slot not in ['1', '2', '3']:
            target_slot = 1
            print("Invalid input, defaulting to 1.")
            
        config = {
            "KEYBOARD_INDEX": detected_keyboard,
            "MOUSE_INDEX": detected_mouse,
            "TARGET_MOUSE_SLOT": int(target_slot)
        }
        
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
            
        print(f"\nConfiguration saved to {os.path.abspath(config_path)}")
        print(json.dumps(config, indent=4))
    else:
        print("Could not identify both Keyboard and Mouse automatically.")
        print("Please ensure both devices are turned on, connected to this PC, and try again.")
        print("You can also manually create 'config.json' in the root directory.")

if __name__ == "__main__":
    main()
