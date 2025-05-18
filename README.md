# Face Recognition and Smart Cropping Pipeline

This project detects faces in images, crops them intelligently with a margin to keep background/clothing, ensures the crop covers at least 50% of the original image area, and resizes the output to 512×512 pixels. It supports batch processing of images from a folder and sorts output into recognized and unrecognized folders.

Additionally, it includes an option to use OpenCV’s DNN face detector for improved robustness against occlusions (e.g., faces partially covered by objects like phones).

---

## Features

- Detect faces in images using either:
  - `face_recognition` (dlib-based), or
  - OpenCV DNN face detector (more robust to occlusions)
- Automatically crop images around faces with a configurable margin, preserving some background
- Ensure crops cover at least 50% of the original image area, avoiding over-cropping
- Resize crops to 512×512 pixels for uniform output
- Process all images in an input folder (`load`)
- Save processed images to:
  - `output/` for images with recognized faces
  - `failed/` for images with no detected faces
- Optional maximum crop size to handle very large images efficiently

---

## Installation

Make sure you have Python 3.7+ installed. Then install required packages:

```bash
pip install face_recognition opencv-python
```
## Dont Forget To Clone Into Repo
```
git clone https://github.com/chsagar141/auto-crop-face.git
```
Credits

### This project uses the following open-source libraries:

---

[face_recognition GitHub repo](https://github.com/ageitgey/face_recognition)

[OpenCV (opencv-python)](https://pypi.org/project/opencv-python/)


Thanks to the developers and contributors of these libraries for making powerful tools freely available.
