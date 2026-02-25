import time

class KeyboardMonitor:
    def __init__(self, device, dev_index):
        self.device = device
        self.dev_index = dev_index

    def check_status(self):
        """
        Pings the keyboard using HID++ 2.0 GetProtocolVersion.
        Returns:
            "ONLINE": Device is connected and responding.
            "OFFLINE": Device is disconnected or switched to another PC (Error 0x10).
            "ERROR": Communication issue.
        """
        # HID++ 2.0 GetProtocolVersion
        packet = [0x10, self.dev_index, 0x00, 0x10, 0x00, 0x00, 0x00]
        try:
            self.device.write(packet)
        except Exception as e:
            return "ERROR"
            
        start_time = time.time()
        while time.time() - start_time < 0.2:
            resp = self.device.read(64)
            if resp:
                # Response to Root Feature (0x00)
                if resp[0] == 0x10 and resp[1] == self.dev_index:
                    if resp[2] == 0x8F and resp[4] == 0x10:
                        # Error 0x10 indicates device is offline/disconnected.
                        return "OFFLINE"
                    elif resp[2] == 0x00:
                        return "ONLINE"
            time.sleep(0.01)
        # Timeout without error means the response was intercepted by Logi Options+, signifying it is actually ONLINE
        return "ONLINE"
