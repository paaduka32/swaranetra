# Swaranetra  

**Swaranetra** is a computer-vision powered assistive tool that processes live camera feeds from an ESP32 cam and provides:  

- **Scene description** using the BLIP-2 vision-language model  
- **Text recognition (OCR)** with intelligent grammar and spelling correction  

The system is designed to serve as a low-cost prototype for visually impaired assistance and real-time environmental understanding.  



## Table of Contents  

- Introduction
- Features  
- Requirements  
- Usage  
- Contributors 


## Introduction  

Swaranetra bridges IoT and AI for accessibility. It streams frames from an **ESP32-CAM module** into a **Flask server**, where frames are analyzed by either:  

1. **Scene Description** – generating natural language descriptions of the captured scene using **BLIP-2**.  
2. **OCR Pipeline** – extracting and refining text from the environment using **Tesseract OCR**, **SpellChecker**, and **Grammar Correction** (via spaCy + LanguageTool).  

---

## Features  

- **ESP32 camera live stream** integration  
- **Scene understanding** using BLIP-2 vision-language model  
- **OCR with smart corrections** (spelling + grammar)  
- **Web interface** built with Flask  


## Requirements  

Software:
- Python 3.8+  
- Flask  
- OpenCV  
- NumPy  
- PyTesseract (ensure Tesseract OCR is installed in your system)  
- spaCy (`en_core_web_sm` model)  
- language-tool-python  
- pyspellchecker  
- Hugging Face Transformers (for BLIP-2)  
- Torch  

Hardware::  
- **ESP32-CAM** with Arduino Uno for live streaming
- FTDI module for uart transmission with the computer

## Usage  

1. Ensure ESP32-CAM is running the **camerawebserver** and note its stream URL.  
2. Update the `ESP32_STREAM_URL` in `app.py` with your ESP32’s IP.  
3. Run the script to the flask interface

##Contributors
**[Paaduka32](https://github.com/paaduka32)** 
**[Manohara-Ai](https://github.com/Manohara-Ai)** 

