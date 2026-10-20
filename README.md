# Project Structure
 
```text
Prototyp/
├── src/
│ ├── PiCameraManager/
│ ├── PersonRecognition/
│ ├── LicensePlate/
│ ├── LIDAR_Manager/
│ └── prototyp_daemon.py
│
└── models/
├── yolox_nano.pth
└── latest_ckpt.pth
```
 
# Required Models
 
```text
models/latest_ckpt.pth
→ License Plate Recognition
 
models/yolox_nano.pth
→ Person Recognition
```
 
# Python Environment
 
A complete freeze of the development environment can be found in:
 
```text
requirements.txt
```
 
Install dependencies using:
 
```bash
pip install -r requirements.txt
```
 
# Run

Install all dependencies using:

pip install -r requirements.txt

