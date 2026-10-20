Project Structure

Prototyp/
├── src/
│   ├── PiCameraManager/
│   ├── PersonRecognition/
│   ├── LicensePlate/
│   ├── LIDAR_Manager/
│   └── prototyp_daemon.py
│
└── models/
    ├── yolox_nano.pth
    └── latest_ckpt.pth

Required Models

models/latest_ckpt.pth
→ License Plate Recognition

models/yolox_nano.pth
→ Person Recognition

Python Environment

A complete freeze of the development virtual environment can be found in:

requirements.txt

Install all dependencies using:

pip install -r requirements.txt

