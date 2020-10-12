from flask import Flask
from flask import jsonify,request,render_template
import requests
from werkzeug.utils import secure_filename
import os,base64


YUKLEME_KLASORU = 'static/yuklemeler'
UZANTILAR = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__,static_url_path="/static")
app.config['UPLOAD_FOLDER'] = YUKLEME_KLASORU


################### Uzantı Kontrolü #########################

def uzanti_kontrol(dosyaadi):
   return '.' in dosyaadi and \
   dosyaadi.rsplit('.', 1)[1].lower() in UZANTILAR

#############################################################


@app.route('/mainPage',methods=['GET'])
def static_file1():
    # if request.method=="GET":
    #     response=requests.get(url+my_img)

    #     return render_template('index.html', title='Home')
    # else:
    return app.send_static_file('index.html')


@app.route('/detail',methods=['GET','POST'])
def static_file():
    if 'uploadFile' not in request.files:
            print("NO FILE")
            return app.send_static_file('product_detail3.html')
    if request.method == 'POST':
        uploadFile=request.files['uploadFile']
        with open(uploadFile.filename,'rb') as image_file:
            image_content=image_file.read()
        # if uploadFile and uzanti_kontrol(uploadFile.filename):
        #     dosyaadi = secure_filename(uploadFile.filename)
        #     uploadFile.save(os.path.join(app.config['UPLOAD_FOLDER'], dosyaadi))
        #     #return redirect(url_for('dosyayukleme',dosya=dosyaadi))
        # else:
        #    print("UYMAYAN UZANTI")
        # print(uploadFile)
        # conv=base64.b64encode(uploadFile.read())
        # print(conv)
        response_api=requests.post(url="http://127.0.0.1:3005//api/v1/PostVision/"+str(image_content))
        print("İstek atıldı")
        print(type(response_api))
    return app.send_static_file('product_detail3.html')
# @app.route('/productDetail',methods=['POST'])
# def postProductDetail():
#     try:
#         render_template('product_detail.html')
#     except expression as identifier:
#         pass

if __name__=='__main__':
    app.run(port=3003,debug=True)