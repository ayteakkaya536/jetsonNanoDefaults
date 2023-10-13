## WORKING TESTED ON WINDOWS ###
## run with python3
## pip3 install flask
## pip3 install opencv-python

### IMPROVEMENT NEEDED ###
## whn you run the code, it gives url and port number. we need to have this stream over internet not only on local computer

### NOT WORKING!! web streaming trial, type the code in terminal
## set FLASK_APP=app.py  
## flask run --host=ipaddress (ipconfig IP4)
## on browser http://ipaddress:5000/


from flask import Flask,render_template,Response
import cv2

app=Flask(__name__)
camera=cv2.VideoCapture(0)

def generate_frames():
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')  ## ('/video' triggered by the template/index.html)
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')  ## this 'frame' name comes from the last frame assigment (frame=buffer.tobytes())

if __name__=="__main__":
    #app.run(debug=True)
    app.run(debug=True, port=5000, host='192.168.30.113') ## host ip needs to be changed according to the ipconfig ALSO port 5000 must be open for external traffic (Windows Firewall)

