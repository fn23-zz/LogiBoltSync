# LogiBoltSync

<!-- Badges or other repo info can go here -->

LogiBoltSync is a utility that synchronizes the connection slot of your Logitech mouse (e.g., MX Master 3S) with your Logitech keyboard (e.g., Signature K855) via Logi Bolt receiver.

When you switch your keyboard to another PC, LogiBoltSync detects this and automatically commands your mouse to switch to the same PC, allowing for a seamless multi-device workflow.

LogiBoltSyncは、Logi Boltレシーバー経由で接続されたLogitechのキーボード（例：Signature K855）とマウス（例：MX Master 3S）の接続スロットを同期するユーティリティです。
キーボードを別のPCに切り替えると、LogiBoltSyncがこれを検知し、マウスにも自動的に同じPCへの切り替えコマンドを送信します。これにより、シームレスなマルチデバイスワークフローが実現します。

---

## 📖 Documentation / ドキュメント

Please choose your preferred language: / 言語を選択してください：

### English

- **[Read the Overview & Features](docs/Readme.md)**
- **[Step-by-Step Installation Guide](docs/Install.md)**

### 日本語

- **[概要と主要機能について](docs/Readme_JP.md)**
- **[インストールと環境構築の手順](docs/Install_JP.md)**

---

## Quick Start

If you already have Python installed, you can clone the repository, install the dependencies, and run the configuration tool:

```powershell
pip install -r requirements.txt
python tools/detect_devices.py
```

See the installation guides above for detailed instructions on multi-PC setup and auto-start configuration.

---
**License**: MIT
