# 📏 Object Size Measurement Using OpenCV

This project uses Python and OpenCV to **measure the real-world size of rectangular objects** from a live webcam feed.  
It is designed to be run on any machine, including **Raspberry Pi**, and is calibrated using a known reference object (like a credit card).

---

## 🖼️ What It Does

- Detects **2D rectangular objects** in a video stream.
- Measures their **width and height in centimeters**.
- Uses a reference object for **pixel-to-centimeter calibration**.
- Displays live measurement overlays on the video feed.

---

## 🧰 Requirements

Install these before running:

```bash
pip install opencv-python numpy
