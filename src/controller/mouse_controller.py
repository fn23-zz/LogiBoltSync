import time

class MouseController:
    def __init__(self, device, dev_index):
        self.device = device
        self.dev_index = dev_index
        self.change_host_feature_index = 0x0A  # Discovered during testing

    def switch_host(self, target_slot):
        """
        Sends the ChangeHost command to the mouse to switch to the target slot.
        target_slot: 1, 2, or 3
        """
        slot_index = target_slot - 1
        
        # Test 10 showed that applying Function 1, 2, or 3 successfully triggered a switch.
        # Usually, Function 1 is used to change host. Let's send Function 1 (0x10).
        func_id = 1
        byte3 = func_id << 4
        
        packet = [0x11, self.dev_index, self.change_host_feature_index, byte3, slot_index, 0x00] + [0]*14
        
        try:
            self.device.write(packet)
            # Give it a tiny bit of time to send
            time.sleep(0.1)
            return True
        except Exception as e:
            return False
