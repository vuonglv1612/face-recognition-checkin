# FACE RECOGNITION CHECK-IN

Basic Real time Face Recognition Check-in Application

## 1. Dependencies
- cmake 3.22
- poetry 1.1
- python 3.8

## 2. Installation
```bash
poetry env use python3.8
poetry install
```

## 3. Configuration
```bash
cp .env.template .env
```
Edit .env file configuration

## 4. Training
Add face images to `images` folder

And run following command
```bash
poetry run python train.py
```

## 5. Start recognizer
```bash
poetry run python main.py
```
Press `q` to stop recognizer

## 6. Start worker
If you want to send check in image to telegram group, start worker at another terminal
```bash
poetry run python worker.py
```
