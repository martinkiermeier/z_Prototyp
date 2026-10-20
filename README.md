
project structure:
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

    
required models:
models/latest_ckpt.pth
→ license plate recognition
models/yolox_nano.pth
→ person recognition

complete freeze of venv during develpment:
requirement.txt
