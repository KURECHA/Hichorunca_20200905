from flask import Flask, render_template, Response, redirect, url_for, session, request
# from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
# from keras.preprocessing import image
from camera import VideoCamera
import requests
import numpy as np
# import tensorflow as tf
import cap_box
import os


app = Flask(__name__)

# model = VGG16(include_top=True, weights='imagenet', input_tensor=None, input_shape=None)
# graph = tf.get_default_graph()

@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/custom')
def castum():
    return render_template('./custom_size.html')


@app.route('/box_camera')
def box_camera():
    global result
    return render_template('./box_camera.html',)


@app.route('/box_camera/big')
def big_bag():
    global size
    size = 23
    return redirect('/box_camera')


@app.route('/box_camera/small')
def small_bag():
    global size

    size = 6
    return redirect('/box_camera')


@app.route('/box_camera/none')
def none_bag():
    global size
    size = 0
    # cap_box.cap_box(size)
    return redirect('/box_camera')


@app.route('/box_camera/custom', methods=["POST"])
def custom_bag():

    width = request.form["width"]
    height = request.form["height"]
    depth = request.form["depth"]
    
    
    global size
    size = float(width) * float(height) * float(depth) * 0.000001

    print(size)

    return redirect('/box_camera')

@app.route('/video_feed')

def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    # print(size)
    while True:  
        
        global egg_flag
        global result

        frame, result, egg_flag = camera.get_frame(size)
        # result = np.array([ecobag_used, s_bag_num, l_bag_num])
        yield (b'--frame\r\n' 
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/result')
def result():

    print("#####result#######", result)

    # resultの内容を変更するとresult.htmlの表示が変わる.
    # リストの順番は左からエコバッグの占有率、レジ袋Lの枚数、レジ袋Sの枚数
    # result = [0, 2, 1]
    ecometa = result[0]


    if result[0] <= 0:
        image = "poli.png"

        if result[1] > 0 and result[2] >0:
            result_text = "レジ袋L{0[2]}枚、S{0[1]}枚必要".format(result)

        elif result[1] > 0 and result[2] == 0:
            result_text = "レジ袋S{0[1]}枚必要".format(result)
        
        elif result[1] == 0 and result[2] > 0:
            result_text = "レジ袋L{0[2]}枚必要".format(result)

        else:
            image = "logo2.png"
            result_text = "もう一度測定してください"

    elif result[0] > 0 and result[0] <= 100:

        if result[1] == 0 and result[2] == 0:
            image = "eco_kurecha.png"
            result_text = "はいっちょる！！"

        else:
            image = "logo2.png"
            result_text = "もう一度測定してください"

    elif result[0] > 100:
        image = "poli_and_eco.png"

        if result[1] > 0 and result[2] >0:
            result_text = "エコバッグ＋レジ袋L{0[2]}枚、S{0[1]}枚必要".format(result)

        elif result[1] > 0 and result[2] == 0:
            result_text = "エコバッグ＋レジ袋S{0[1]}枚必要".format(result)
        
        elif result[1] == 0 and result[2] > 0:
            result_text = "エコバッグ＋レジ袋L{0[2]}枚必要".format(result)

        else:
            image = "logo2.png"
            result_text = "もう一   度測定してください"

    else:
        image = "logo2.png"
        result_text = "もう一度測定してください"


        
    return render_template('./result.html', image = image, result = result_text, ecometa=ecometa)

if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=8080)

