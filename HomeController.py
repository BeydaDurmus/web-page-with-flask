from flask import Flask
from flask import jsonify,request,render_template
import requests
from werkzeug.utils import secure_filename
import os,base64

from ps_manager import CloudStorageUploader


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
    return app.send_static_file('index.html')


@app.route('/detail',methods=['GET','POST'])
def static_file():
    if request.method=='POST':
      if 'uploadFile' not in request.files:
         return app.send_static_file('product_detail3.html')     

      uploadFile = request.files['uploadFile']					
      if uploadFile.filename == '':
         return app.send_static_file('product_detail3.html')
					
      if uploadFile and uzanti_kontrol(uploadFile.filename):
         dosyaadi = secure_filename(uploadFile.filename)
         uploadFile.save(os.path.join(app.config['UPLOAD_FOLDER'], dosyaadi))

      cloud_manager=CloudStorageUploader('main-product-set-images')
      cloud_manager.UploadToBucket('api-imgs/deneme.jpg',YUKLEME_KLASORU+'/'+uploadFile.filename)
      response_api=requests.post(url="http://127.0.0.1:3005//api/v1/PostVision/")
      print(response_api.content)
      
    return app.send_static_file('product_detail3.html',response=response_api.content)

if __name__=='__main__':
    app.run(port=3003,debug=True)