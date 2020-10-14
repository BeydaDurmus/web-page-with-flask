from flask import Flask
from flask import jsonify,request,render_template
import requests
from werkzeug.utils import secure_filename
import os,base64
import ast
from ps_manager import CloudStorageUploader
from PIL import Image 
import io
import urllib.request


YUKLEME_KLASORU = 'static/yuklemeler'
UZANTILAR = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
response = None
# app = Flask(__name__,static_url_path="/static")
app=Flask(__name__)
app.static_folder='static'
app.config['UPLOAD_FOLDER'] = YUKLEME_KLASORU


################### Uzantı Kontrolü #########################

def uzanti_kontrol(dosyaadi):
   return '.' in dosyaadi and \
   dosyaadi.rsplit('.', 1)[1].lower() in UZANTILAR

#############################################################


@app.route('/tydetail',methods=['GET'])
def GetProductPage():
    return render_template('single-product.html')


@app.route('/detail',methods=['GET','POST'])
def product_detail():
   global response
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
      if not response_api is None:
         response=response_api.content
         byte_response=response_api.content
         dict_str=byte_response.decode("UTF-8")
         response=ast.literal_eval(dict_str)
         url=response['image_url']
         with urllib.request.urlopen(url) as url:
            f = io.BytesIO(url.read())

         img = Image.open(f)

         # image=requests.get()
         # image=Image.open(BytesIO(image.content))
         labels=response['labels']['values']
         product_info=response['product_info']

         print(labels)
         return render_template('deneme.html',response=response,labels=labels,product_info=product_info,image=img)
      else:
         response=None
         print(response)
   if request.method=='GET':
      return render_template('deneme.html')
      
   return render_template('deneme.html')

if __name__=='__main__':
    app.run(port=3003,debug=True)