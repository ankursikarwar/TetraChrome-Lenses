# TetraChrome Lenses: Smart Glasses for Visually Impaired People


TetraChrome Lenses is a portable, robust and efficient device capable of assisting a visually impaired person in a seamless manner. The device integrates different technologies like computer vision, embedded systems, and text-to-speech to create a powerful personal assistant for the blind. It generates audio cues and haptic feedback for helping the blind person to perceive and interact with the surrounding.
<br>
<br>

<img src="https://drive.google.com/uc?id=1-nSVDjGjqTAFR0CwkxBnScoYO84j4KhF" alt="Image4" width="500" height="400"/>     
<br>
<img src="https://drive.google.com/uc?id=102709c1dePEORxNlqz3pIIVObpDHAQ6x" alt="Image4" width="500" height="400"/> 

<br>
<br>

## Prerequisites

1. Raspberry Pi 3B+
2. USB Camera
3. Switch Board with 4 switches (Attach 4 switches on the GPIO pins 17, 18, 22, 27)
4. Power Supply for Raspberry Pi (You can also use a Power Bank)
5. Bluetooth Earpiece

#### Optional (In case of Overheating) 

1. Heat Sink
2. Cooling Fan

## Getting Started

Access the Raspberry Pi via SSH

```
ssh pi@<ip-address>
<password>
```

## Installation

1. Firstly, install virtualenv

```
pip install virtualenv
```

2. Create a project folder

```
mkdir TetraChrome_Lenses
cd TetraChrome_Lenses
```

3. Initialize virtual environment 

```
virtualenv venv
```

4. Activate the virtual environment

```
source venv/bin/activate
```

5. Clone the Repo

```
(venv) git clone https://github.com/ankursikarwar/TetraChrome-Lenses.git
```

6. Navigate to the sub-folder

```
(venv) cd TetraChrome-Lenses
```

7. Install the dependencies

```
(venv) pip install -r requirements.txt
```

## Starting the Application 

Attach the USB camera and run main.py

```
(venv) python main.py
```

