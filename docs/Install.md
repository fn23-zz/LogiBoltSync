# Installing LogiBoltSync

This guide will walk you through setting up LogiBoltSync to automatically switch your mouse when your keyboard switches to another PC.

For a true two-way automated experience between two PCs (PC1 and PC2), you will need to perform this installation on **both** computers.

## Prerequisites

- **OS**: Windows 10 / 11
- **Hardware**: Logitech Bolt USB Receiver, a compatible keyboard (e.g., K855), and a compatible mouse (e.g., MX Master 3S). Both devices must be paired to the Bolt receiver on each PC.
- **Python**: Python 3.10 or newer.

## 1. Setup Python Environment

1. Download and install Python from the [official website](https://www.python.org/downloads/windows/).
2. **Important**: During installation, check the box that says **"Add Python to PATH"**.
3. Open PowerShell or Command Prompt and verify the installation:

   ```powershell
   python --version
   ```

## 2. Install Dependencies

Clone or download the LogiBoltSync repository. Open PowerShell, navigate to the LogiBoltSync directory, and install the required `hidapi` package:

```powershell
pip install -r requirements.txt
```

## 3. Generate Configuration

LogiBolt receivers assign different internal ID numbers (Indices) to connected devices depending on the PC. You must run the included detection tool to generate a `config.json` specific to the current PC.

1. Ensure both your keyboard and mouse are currently connected to the PC you are setting up.
2. Run the detection tool:

   ```powershell
   python tools\detect_devices.py
   ```

3. The script will scan the Bolt receiver and identify your devices.
4. It will ask for a **Target Mouse Slot (1, 2, or 3)**. Enter the slot number of the *other* PC you want the mouse to switch to when the keyboard leaves this PC.
   - *Example: If PC1 is Slot 1, and PC2 is Slot 2. When installing on PC1, enter `2`. When installing on PC2, enter `1`.*
5. A `config.json` file will be generated in the root directory.

## 4. Run LogiBoltSync

Test the application by running the main loop:

```powershell
python src\main.py
```

While the script is running, physically switch your keyboard to the other PC. The mouse should automatically follow. Press `Ctrl+C` to stop the script.

## 5. Auto-start on Boot (Optional but Recommended)

To run LogiBoltSync silently in the background every time you start your PC:

1. Create a file named `start_logiboltsync.bat` in the LogiBoltSync folder with the following content:

   ```bat
   pythonw src\main.py
   ```

   *(Using `pythonw` prevents the console window from appearing).*

2. Open **Task Scheduler** in Windows.
3. Click **Create Task...**
4. **General Tab**: Name the task (e.g., "LogiBoltSync"). Check **"Run with highest privileges"**.
5. **Triggers Tab**: Click New, and select **"At log on"**.
6. **Actions Tab**: Click New, set Action to "Start a program".
   - **Program/script**: Browse and select the `start_logiboltsync.bat` you created.
   - **Start in (optional)**: Enter the full path to the LogiBoltSync directory (e.g., `C:\path\to\LogiBoltSync`). *This is critical for the script to find its config file.*
7. Save the task. LogiBoltSync will now run automatically in the background.
