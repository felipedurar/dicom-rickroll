# Dicom Rickroll
A Rickroll DICOM File Generator

![alt text](screenshots/screenshot1.png)

## What is it?
This project generates a Rickroll Meme DICOM File!

Unfortunatelly i cannot provide the Rickroll DICOM file here due to copyright, that's why i created this script, it basically downloads the Youtube video, 
encodes it to the H.264 format and them convert it to DICOM format.

My objective here is not to just add the MPEG content into the DICOM dataset, actually i wanted to make everyframe as an instance, just like an MR/CT image.

This also garantees that almost any DICOM viewer can visualize this Rickroll.

## How to generate the Rickroll DICOM File?
I'm provinding two methods to generate the Rickroll DICOM file, the first one by 
using Docker Compose, and the seconds method manually installing the python, ffmpeg and its packages.

### Generating using Docker Compose (Easy Method)
You just need to have docker and docker compose installed on your computer and run the following command:
```
docker-compose up
```
This will generate the ```rickroll.dcm``` file in the ```./output``` folder locally.

### Generating manually running the Python Script
First of all, you need to have FFMPEG installed on your computer, you can do it running this:
```
sudo apt install ffmpeg
```

I recommend you to create a venv, you can do it by running:
```
python -m venv venv
source venv/bin/activate     # Linux/macOS
```

And then you need to install the packages:
```
pip install -r requirements.txt
```

Now you are ready to run the python code and generate it, you just need to run:
```
python dcm-gen.py
```

This will generate the ```rickroll.dcm``` file in the ```./output``` folder locally.


## License
MIT License

Copyright (c) 2025 Felipe Durar

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
