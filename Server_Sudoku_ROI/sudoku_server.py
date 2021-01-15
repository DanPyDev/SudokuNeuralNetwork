#necessary imports for building the server and socket handling
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template

#imports for socket message receiving and sending
from time import sleep
import base64
import json

#numpy.....
import numpy as np

#import opencv for image capturing and manipulation
import cv2

#tensorflow for loading trained neural network models
from tensorflow.keras.models import load_model

#import wraper functions for image preprocessing and model management
from Image_Preprocessing import Image_Pre_Processing, process_frame
from ConvNet_Predict import predict_ConvNet, predict_ConvSolve
from convert_to_image import convert_sudoku_txt_to_image
from blank_sudoku_generator import image_blanck_generator
from sudoku_solver import solve_sudoku

model_ConvNet = load_model('ConvNet_200Epoch.h5')
model_ConvSolve = load_model('train_18_dec.h5')

print("Models Loaded!")

PIL_bs_img = image_blanck_generator()

app = Flask(__name__, template_folder = 'static')

@app.route('/')
def index():
    return render_template('index_sudoku.html')

@app.route('/camera')
def camera():

    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        
        while True:
            cam = cv2.VideoCapture(0)
            
            success = False
            abort = False
            cells = []
            
            while True:
                image = cam.read()[1]
                processed = process_frame(image)
                buffer = cv2.imencode('.jpg', processed)[1].tobytes()
                live_as_text = base64.b64encode(buffer).decode()
                ws.send('{"img":"' + str(live_as_text) + '"}')
                sleep(0.01)
                resp = ws.receive()
                py_resp = json.loads(resp)
                if(py_resp["aqc"]):
                    cam.release()
                    break

            #process image
            cv2.imwrite("debug.jpg", image)
            success, preImage, cells = Image_Pre_Processing(image)
            
            if(success):
                #then wait for another response from html
                preBuffer = cv2.imencode('.jpg', preImage)[1].tobytes()
                pre_as_text = base64.b64encode(preBuffer).decode()
                
                resp = ws.receive()
                py_resp = json.loads(resp)
                
                if(py_resp["waiting"]):
                    ws.send('{"preImg":"' + str(pre_as_text) + '", "good_img": true}')
                    abort = False
                else:
                    ws.send('{"preImg":" ", "good_img": false}')
                    abort = True
            else:
                resp = ws.receive()
                py_resp = json.loads(resp)
                
                ws.send('{"preImg":" ", "good_img": false}')
                abort = True
            
            if(success and not abort):
                for i, cell in enumerate(cells):
                    cells[i] = cell / 255.0
                
                sudoku_img = np.array(cells).reshape(-1, 32, 32, 1)
                
                ConvNet_pred = predict_ConvNet(model_ConvNet, sudoku_img)
                pred_labels = np.array([np.argmax(i) for i in ConvNet_pred])
                prob_labels = np.around(np.array([np.max(i) for i in ConvNet_pred]), 3)
                
                conv_img = convert_sudoku_txt_to_image(pred_labels, PIL_bs_img, "FreeMono.ttf")
                open_cv_image = np.array(conv_img)
                
                convBuffer = cv2.imencode('.jpg', open_cv_image)[1].tobytes()
                conv_as_text = base64.b64encode(convBuffer).decode()
                
                resp = ws.receive()
                py_resp = json.loads(resp)
                if(py_resp["conv"]):
                    ws.send('{"convImg": "' + str(conv_as_text) + '", "labels": [' + 
                            ', '.join(map(str, pred_labels.reshape(9,9).T.flatten())) + 
                            '], "probs": [' + ', '.join(map(str, prob_labels.reshape(9,9).T.flatten())) + 
                            '], "good_img": true}')
                    abort = False
                else:
                    ws.send('{"convImg": " ", "labels": " ", "good_img": false}')
                    abort = True
            elif(not abort):
                resp = ws.receive()
                py_resp = json.loads(resp)
                
                ws.send('{"convImg":" ", "labels": " ", "good_img": false}')
                abort = True
            
            if(not abort):
                resp = ws.receive()
                py_resp = json.loads(resp)
                
                if(py_resp["solve"]):
                    ConvSolve_pred = predict_ConvSolve(model_ConvSolve, pred_labels.reshape(-1, 9, 9, 1).astype("float16"))
                    solve_labels = np.array([np.argmax(i) for i in ConvSolve_pred])
                    solve_probs = np.around(np.array([np.max(i) for i in ConvSolve_pred]), 3)
                
                    solv_img = convert_sudoku_txt_to_image(solve_labels, PIL_bs_img, "FreeMono.ttf")
                    open_cv_image_solve = np.array(solv_img)
                
                    solvBuffer = cv2.imencode('.jpg', open_cv_image_solve)[1].tobytes()
                    solv_as_text = base64.b64encode(solvBuffer).decode()
                    ws.send('{"solution": [' + ', '.join(map(str, solve_labels.reshape(9,9).T.flatten())) + 
                            '], "probs": [' + ', '.join(map(str, solve_probs.reshape(9,9).T.flatten())) + 
                            '], "solvImg": "' + str(solv_as_text) + '", "good_solve": true}')
                    abort = False
                else:
                    ws.send('{"solution":" ", "solvImg": " ", "good_solve": false}')
                    abort = True
            
            if(not abort):
                solution, algo_labels = solve_sudoku(pred_labels.reshape(9, 9))
                
                if(solution):
                    algo_img = convert_sudoku_txt_to_image(algo_labels.flatten(), PIL_bs_img, "FreeMono.ttf")
                    open_cv_image_algo = np.array(algo_img)
                    
                    algoBuffer = cv2.imencode('.jpg', open_cv_image_algo)[1].tobytes()
                    algo_as_text = base64.b64encode(algoBuffer).decode()
                    
                    resp = ws.receive()
                    py_resp = json.loads(resp)
                    
                    if(py_resp["algo"]):
                        ws.send('{"solution": [' + ', '.join(map(str, algo_labels.reshape(9,9).T.flatten())) + '], "solvImg": "' + str(algo_as_text) + '", "good_solve": true}')
                        abort = False
                    else:
                        ws.send('{"solution":" ", "solvImg": " ", "good_solve": false}')
                        abort = True

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0',9999), app, handler_class=WebSocketHandler)
    http_server.serve_forever()