# LogiBoltSync

**LogiBoltSync** is a Python-based utility that automatically synchronizes the connection slot of your Logitech mouse (e.g., MX Master 3S) with your Logitech keyboard (e.g., Signature K855).

When you use the Easy-Switch button on your keyboard to switch to another PC, or when you turn the keyboard off, LogiBoltSync detects the disconnection and instantly switches your mouse to the designated PC slot. This allows for a seamless multi-PC workflow without needing to manually flip your mouse upside down to change its connection.

## Features

- **Automatic Synchronization**: Detects keyboard disconnects and automatically triggers a host change on the mouse.
- **Dual-Interface Architecture**: Intelligently bypasses HID packet interception by official software (like Logi Options+) by using one HID interface for monitoring and another for controlling.
- **Dynamic Configuration**: Includes an auto-detection tool that scans your Logi Bolt receiver to find the correct internal device indices, making it easy to deploy on any PC setup.

## How It Works

LogiBoltSync communicates directly with the Logi Bolt USB Receiver using the Logitech HID++ protocol.
It sends periodic `GetProtocolVersion` pings to the keyboard. When a timeout or `ERROR_0x10` is detected (indicating the keyboard is no longer active on the current PC), it sends a `ChangeHost` command to the mouse using its specific Feature ID and Function index.

## Installation & Usage

Please refer to the [Install.md](Install.md) guide for detailed instructions on how to set up and configure LogiBoltSync on your Windows PCs.

## License

This project is open-source and available under the MIT License.
