Description: this is an ai aimbot that utilizes the yolov11n model to predict the position of enemies and target head using computer vision

prerequisites:
- an rtx gpu [preferably the latest for the best performance]
- arduino leonardo
How to use:
- create a custom environment , preferably python 3.8.10 others work too I think
- https://developer.nvidia.com/cuda-11-8-0-download-archive?target_os=Windows <-- download cuda
- pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
- install the varies dependencies given in main.py [note: pip install pywin32 for win32gui ]
- python main.py to run
- change the enemy color to purple for better accuracy

## Game settings
- enemy highlight color: purple
- sensitivity Aim 0.8


## Running the Application
- put the code from [mousemov.ino](mousemov.ino) into arduino leonardo [make sure the port is COM6]
- connect the arduino to the pc
- run the convert.py file [wait for it to finish]
- run the headhunter.py file