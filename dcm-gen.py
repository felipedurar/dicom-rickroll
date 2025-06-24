import cv2
import pydicom
import numpy as np
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import generate_uid, ExplicitVRLittleEndian
import yt_dlp
import subprocess
import datetime
import os

fps_target = 10
max_seconds = 20
target_size = (640, 480)  # (width, height)

# Check output path
output_path = './output'
if not os.path.exists(output_path):
    os.mkdir(output_path)

# Download the Video
mp4_input_file = './output/input.mp4'
if os.path.exists(mp4_input_file):
    print('Video File already downloaded!')
else:
    print('Downloading YouTube Video...')
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': mp4_input_file,
        'merge_output_format': 'mp4',  # Ensures output is .mp4
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print('YouTube Video Downloaded!')

# Convert using ffmpeg
# ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset fast converted.mp4
mpeg_output_file = './output/output.mp4'
if not os.path.exists(mpeg_output_file):
    print('Converting Video Format to H.264...')
    command = [
        'ffmpeg',
        '-i', mp4_input_file, '-t', str(max_seconds),
        '-c:v', 'libx264', '-crf', '23', '-preset', 'fast',
        mpeg_output_file
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)
    print('Video Format Converted!')

# Generate the Dicom File
output_path = "./output/rickroll.dcm"
if not os.path.exists(output_path):
    print('Writing DICOM File...')
    cap = cv2.VideoCapture(mpeg_output_file)

    # Target parameters
    max_frames = fps_target * max_seconds
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(round(original_fps / fps_target))

    frames = []
    frame_count = 0
    collected = 0

    while cap.isOpened() and collected < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb_resized = cv2.resize(rgb, target_size, interpolation=cv2.INTER_AREA)

            frames.append(rgb_resized)

            #frames.append(rgb)
            collected += 1

        frame_count += 1

    cap.release()

    if not frames:
        raise ValueError("No frames were extracted from the video.")

    # Stack frames: shape becomes (num_frames, rows, cols, 3)
    pixel_array = np.stack(frames, axis=0)
    num_frames, rows, cols, samples = pixel_array.shape

    # Convert to interleaved byte string: (frames, rows, cols, RGB) → bytes
    pixel_bytes = pixel_array.tobytes()

    # Create DICOM
    dt = datetime.datetime.now()
    file_meta = pydicom.dataset.FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = pydicom.uid.SecondaryCaptureImageStorage
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    file_meta.ImplementationClassUID = generate_uid()

    ds = FileDataset(output_path, {}, file_meta=file_meta, preamble=b"\0" * 128)
    ds.SOPClassUID = file_meta.MediaStorageSOPClassUID
    ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
    ds.StudyInstanceUID = generate_uid()
    ds.SeriesInstanceUID = generate_uid()
    ds.InstanceNumber = 1

    # Patient/study data
    ds.PatientName = "Video^Color"
    ds.PatientID = "VIDCOLOR"
    ds.StudyDate = dt.strftime('%Y%m%d')
    ds.StudyTime = dt.strftime('%H%M%S')
    ds.ContentDate = ds.StudyDate
    ds.ContentTime = ds.StudyTime
    ds.Modality = "OT"

    # Image info
    ds.SamplesPerPixel = 3
    ds.PhotometricInterpretation = "RGB"
    ds.Rows = rows
    ds.Columns = cols
    ds.NumberOfFrames = num_frames
    ds.BitsAllocated = 8
    ds.BitsStored = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0
    ds.PlanarConfiguration = 0  # Interleaved RGB

    # Pixel data
    ds.PixelData = pixel_bytes

    # Save
    ds.save_as(output_path)
    print(f"Saved color multi-frame DICOM with {num_frames} frames to: {output_path}")