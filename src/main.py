import time
import sys
from datetime import datetime

from core import hid_protocol
from monitor.keyboard_monitor import KeyboardMonitor
from controller.mouse_controller import MouseController

import json
import os

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    if not os.path.exists(config_path):
        return None
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output = f"[{timestamp}] {msg}"
    print(output)
    with open("logiboltsync.log", "a", encoding="utf-8") as f:
        f.write(output + "\n")

def main():
    log("LogiBoltSync started.")
    interfaces = hid_protocol.get_hidpp_interfaces()
    if not interfaces['col01'] or not interfaces['col02']:
        log("ERROR: Logi Bolt receiver interfaces not fully found. Exiting.")
        sys.exit(1)
        
    log(f"Opening Logi Bolt Col01 (Monitor): {interfaces['col01']}")
    log(f"Opening Logi Bolt Col02 (Control): {interfaces['col02']}")
    
    try:
        monitor_device = hid_protocol.open_bolt_device(interfaces['col01'])
        control_device = hid_protocol.open_bolt_device(interfaces['col02'])
    except Exception as e:
        log(f"CRITICAL ERROR: Failed to open devices: {e}")
        sys.exit(1)
        
    config = load_config()
    if not config:
        log("ERROR: config.json not found. Please run tools/detect_devices.py first.")
        sys.exit(1)
        
    try:
        KEYBOARD_INDEX = int(config.get("KEYBOARD_INDEX"))
        MOUSE_INDEX = int(config.get("MOUSE_INDEX"))
        TARGET_MOUSE_SLOT = int(config.get("TARGET_MOUSE_SLOT"))
    except Exception as e:
        log(f"ERROR: Invalid config.json format: {e}")
        sys.exit(1)

    keyboard = KeyboardMonitor(monitor_device, KEYBOARD_INDEX)
    mouse = MouseController(control_device, MOUSE_INDEX)
    
    log(f"Monitoring Keyboard (Index {KEYBOARD_INDEX}). Mouse target slot on disconnect: {TARGET_MOUSE_SLOT}")
    
    # State tracking
    is_keyboard_online = None
    has_switched = False
    
    try:
        while True:
            status = keyboard.check_status()
            
            if status == "ONLINE":
                if is_keyboard_online is not True:
                    log("Keyboard is ONLINE.")
                    is_keyboard_online = True
                    has_switched = False # Reset switch flag when keyboard comes back
            
            elif status == "OFFLINE":
                if is_keyboard_online is not False:
                    log("Keyboard goes OFFLINE (Disconnected/Switched).")
                    is_keyboard_online = False
                    
                if not has_switched:
                    log(f"Triggering Mouse Switch to Slot {TARGET_MOUSE_SLOT}...")
                    success = mouse.switch_host(TARGET_MOUSE_SLOT)
                    if success:
                        log("Mouse switch command sent.")
                        has_switched = True
                    else:
                        log("ERROR: Failed to send mouse switch command.")
            
            elif status == "ERROR":
                log("WARNING: Communication error while pinging keyboard.")
                
            time.sleep(3) # Requirement: 3-5 seconds interval
            
    except KeyboardInterrupt:
        log("LogiBoltSync stopped by user.")
    except Exception as e:
        log(f"UNEXPECTED ERROR: {e}")
    finally:
        try: monitor_device.close()
        except: pass
        try: control_device.close()
        except: pass

if __name__ == "__main__":
    main()
