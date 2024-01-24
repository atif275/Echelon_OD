from flask import Flask, render_template, Response, jsonify
from flask import Flask, render_template, send_from_directory
import cv2
import os
import numpy as np
from datetime import datetime
import time
from flask import jsonify
import subprocess

app = Flask(__name__)

out= None
streaming_active = False
video_writer = None
output_folder = 'videos'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def start_recording():
    global video_writer
    global out
    print("enetered in sdf............................")
    
    
    filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    out=filename
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can change the codec as needed
    frame_size = (640, 480)  # Adjust the frame size as needed
    # video_writer = cv2.VideoWriter(filename, fourcc, 10.0, frame_size)
    video_writer = cv2.VideoWriter(os.path.join(output_folder, filename), fourcc, 20.0, frame_size)

    return out
    

def stop_recording():
    global video_writer
    global out
    print(f"filename = {out}")
    if video_writer is not None:
        video_writer.release()
        video_writer = None
        rebrand_video(out, "out_videos")

    
        

@app.route('/static/list_videos')
def list_videos():
    video_folder = 'videos'
    videos = [video for video in os.listdir(video_folder) if video.endswith(('.mp4', '.avi', '.mkv'))]
    return jsonify(videos)

    
@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    global video_writer
    folder_path = '/tmp/camera_save_tutorial'
    while streaming_active:
        image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png'))]
        if image_files:
            try:
                latest_image = max(image_files, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
                image_path = os.path.join(folder_path, latest_image)

                frame = cv2.imread(image_path)
                if frame is None:
                    raise FileNotFoundError("Empty image file or format not supported")

                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()

                # Write the frame to the video file if recording is active
                if video_writer is not None:
                    video_writer.write(cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), 1))

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                # time.sleep(0.05)

            except Exception as e:
                print(f"Error processing image: {e}")
                continue

        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_stream')

def start_stream():
    global streaming_active
    global out
    if not streaming_active:
        streaming_active = True
        out=start_recording()
        
        
    
        return jsonify({'status': 'success', 'message': 'Streaming started and recording initiated'})
    else:
        return jsonify({'status': 'error', 'message': 'Streaming is already active'})

@app.route('/stop_stream')
def stop_stream():
    global streaming_active
    global out
    if streaming_active:
        streaming_active = False
        stop_recording()
        
        return jsonify({'status': 'success', 'message': 'Streaming stopped and recording saved'})
    else:
        return jsonify({'status': 'error', 'message': 'Streaming is not active'})

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/videos/<path:filename>')
def videos(filename):
    return send_from_directory('videos', filename)

def rebrand_video(input_file, output_folder, brand='mp42'):
    # Make sure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Extract the file name from the input path
    file_name = os.path.basename(input_file)
    
    # Construct the output path
    output_path = os.path.join(f"new_{file_name}")
    
    print(f"file_name= {file_name}")
    print(f"output path= {output_path}")

    # Construct the FFmpeg command
    # ffmpeg_command = f"ffmpeg -i {file_name} -brand {brand} {output_path}"
    # print(f"ffmdpf{ffmpeg_command}")
    
    # # Run the FFmpeg command using subprocess
    # subprocess.run(ffmpeg_command, shell=True)
def value_ret(file_name):
    out=file_name
    print(out)
    return out

# input_folder = "videos"
# output_folder = "out_videos"
# rebrand_videos(input_folder, output_folder)

if __name__ == '__main__':
    
   
    app.run(debug=True)

