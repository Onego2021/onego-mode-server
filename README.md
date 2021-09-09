# onego-model-server

 본 Repository는 **자필 원고지 인식 및 맞춤법 교정 시스템**인 **One Go!** 의 모델 서버를 위한 것입니다. 사용자가 메인 서버로 보낸 요쳥에 의거하여, AWS EC2로 배포된 고정 IP에서 easyOCR이라는 PyTorch 기반 문자 인식 모델을 통해 자필 원고지의 문자를 읽어내고 이를 AWS S3로 업로드하는 역할을 합니다.
<br>
- AWS EC2 : Deep Learning AMI (Ubuntu 18.04) Version 49.0

> 고정 IP : 3.38.9.213:5000/

<br>

## 주요 기능

- AWS S3에서 이미지 파일과, 메인서버에서 UID를 받아와 원고지 파일을 다운로드
- 다운로드된 원고지 이미지 파일을 easyOCR로 recognize하여, 글자를 인식한다.
- 인식된 글자를  txt파일로 생성하여 AWS S3에 사용자 UID로 되어있는 폴더에 업로드한다.
- main server에게 업로드한 txt 파일의 맞춤법 검사를 요청한다.

 <br>

## 설치 및 실행

- Git 프로젝트 디렉토리 생성 및 원격 저장소 연결 혹은 git clone

```
$ mkdir onego-model-server
$ cd onego-model-server
$ git init
$ git remote add origin https://github.com/Onego2021/onego-mobile.git
$ git pull origin master

$ git clone https://github.com/Onego2021/onego-mobile.git
```
<br>
-  dependency : easyocr, boto3, imutils, numpy, Pillow, torch, torchvision, scikit-image, scikit-learn, scipy

```
$ pip3 install easyocr, boto3, imutils, numpy, Pillow, torch, torchvision, scikit-image, scikit-learn, scipy
```
<br>
- Flask 0.12.2

```
$ sudo apt install python3-flask
```
<br>
- 실행  및 접속

```
~/onego-model-server$ FLASK_APP=app.py flask run --host=0.0.0.0
// 접속 : 3.38.9.213:5000/
```

<br>

## 개발 환경

- AWS EC2 : Deep Learning AMI (Ubuntu 18.04) Version 49.0
- Python 3.6.9
- Flask 0.12.2
- PyTorch 1.9.0
- CUDA 10.0

<br>

## OCR 이미지
![onego3](https://user-images.githubusercontent.com/28584299/132631906-fedf4257-ca1a-448f-8172-f4005a87ee03.jpg)

![capture](https://user-images.githubusercontent.com/28584299/132631892-c21c1b6c-3994-4999-8154-da4401273954.PNG)

<br>

## 개발자

- 민대인(bamin0422) : 모델 서버 구성 및 easyOCR 적용
- 최지희(judyi19997) : 모델 서버와 메인 서버 간 통신 router 생성
- 이제혁(hall20000) : 모델 서버 원고지 이미지 전처리

<br>

## 라이센스

- BSD 2-Clause - [LICENSE](https://github.com/Onego2021/onego-model-server/blob/master/LICENSE)

