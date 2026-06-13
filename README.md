# ESP32 Hand Gesture LED Control using OpenCV & MediaPipe

Control 5 LEDs connected to an ESP32 using real-time hand gestures detected by a webcam. This project uses OpenCV, MediaPipe, and Python to track finger positions and send commands to the ESP32 over USB Serial communication.

## Features

* Real-time hand tracking using MediaPipe
* Individual finger controls individual LEDs
* Thumb → LED1
* Index → LED2
* Middle → LED3
* Ring → LED4
* Pinky → LED5
* Live LED status display on webcam preview
* Finger count display
* Hand bounding box visualization
* FPS counter
* USB Serial communication with ESP32
* Cross-platform Python implementation

## Hardware Required

* ESP32 Development Board
* 5 x LEDs
* 5 x 220Ω Resistors
* Breadboard
* Jumper Wires
* USB Cable
* Webcam

## ESP32 Pin Connections

| LED  | ESP32 GPIO |
| ---- | ---------- |
| LED1 | GPIO 2     |
| LED2 | GPIO 4     |
| LED3 | GPIO 5     |
| LED4 | GPIO 18    |
| LED5 | GPIO 19    |

### Circuit

LED Anode → 220Ω Resistor → ESP32 GPIO

LED Cathode → GND

## Software Requirements

### Python Libraries

Install required packages:

```bash
pip install opencv-python mediapipe pyserial
```

### Arduino IDE

Install:

* ESP32 Board Package
* USB Driver (CP210x or CH340 depending on board)

## Project Structure

```text
ESP32-Hand-Gesture-Control/
│
├── ESP32_Code/
│   └── ESP32_Gesture_Control.ino
│
├── Python_Code/
│   └── gesture_control.py
│
└── README.md
```

## How It Works

1. Webcam captures video frames.
2. MediaPipe detects hand landmarks.
3. Finger states are calculated.
4. Binary data is generated.

Example:

```text
10000
```

Means:

```text
Thumb  = ON
Index  = OFF
Middle = OFF
Ring   = OFF
Pinky  = OFF
```

5. Python sends the data via Serial USB.
6. ESP32 receives the command.
7. LEDs update instantly.

## Finger Mapping

| Gesture       | Serial Data | LED State      |
| ------------- | ----------- | -------------- |
| Thumb         | 10000       | LED1 ON        |
| Index         | 01000       | LED2 ON        |
| Middle        | 00100       | LED3 ON        |
| Ring          | 00010       | LED4 ON        |
| Pinky         | 00001       | LED5 ON        |
| Thumb + Index | 11000       | LED1 + LED2 ON |
| Open Palm     | 11111       | All LEDs ON    |
| Closed Fist   | 00000       | All LEDs OFF   |

## Running the Project

### Upload ESP32 Code

1. Open Arduino IDE
2. Select ESP32 Board
3. Select COM Port
4. Upload ESP32 firmware

### Run Python Application

Update COM Port:

```python
PORT = "COM5"
```

Run:

```bash
python gesture_control.py
```

## Troubleshooting

### LEDs Not Responding

* Verify COM port
* Check baud rate is 115200
* Ensure Serial Monitor is closed
* Verify LED wiring

### Webcam Not Opening

Try:

```python
cap = cv2.VideoCapture(0)
```

or

```python
cap = cv2.VideoCapture(1)
```

### Thumb Detection Reversed

Depending on camera orientation and mirroring, reverse the thumb comparison logic in the code.

## Future Improvements

* RGB LED Strip Control
* Home Automation Integration
* Servo Motor Control
* Gesture-Based Robot Control
* Face Recognition
* AI Assistant Integration
* IoT Dashboard

## Demo

Watch the project in action on the Cooltronics Projects YouTube channel.

## License

This project is released under the MIT License.

## Author

Cooltronics Projects

YouTube: Cooltronics Projects

Making Electronics, IoT, ESP32, Arduino, and Embedded Systems Projects.
