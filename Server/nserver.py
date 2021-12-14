from flask import Flask, Response, render_template
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2, time

app = Flask(__name__)


camera = PiCamera()
rawCapture = PiRGBArray(camera)
time.sleep(0.1)


@app.route('/')
def index():
    return render_template('index.html')


def generate_img():
    try:
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
    except Exception as e:
        print("Error: No Image")
        return
    

@app.route('/get_img')
def get_img():
    return Response(generate_img(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)