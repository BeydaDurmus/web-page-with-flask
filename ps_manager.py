from google.cloud import vision,storage
# from mongodb_manager import DatabaseManager
from google.cloud.vision import types
from google.oauth2 import service_account
import pickle,os
from PIL import Image
import requests
import base64

trendyol_categories=[#'elektronik', #Diğer alt kategorileri ekledim.
                     #'bilgisayar-tablet',
                     #'kucuk-ev-aletleri',
                     #'teknoloji-urunleri',
                     #'telefon',#Kaydetmede sorun çıkarıyor, sebebini anlayamadım. ########
                     #'tv-goruntu-ses-sistemleri',#Kaydetme sorunu ##################
                     #'oyun-ve-oyun-konsollari',
                     #'oyuncu-bilgisayari',
                     #'foto-ve-kamera',
                     #'beyaz-esya',#Kaydetme sorunu #################### 
                     #'elektronik-kisisel-bakim',
                     #'veri-depolama',
                     #'annebebek-bakim',
                     #'oyuncak',
                     #'cocuk-gerecleri',
                     #'beslenme-emzirme',
                     #'sofra--mutfak',
                     #'banyo',
                     #'ev-tekstili',
                     #'mobilya',
                     #'ev-dekorasyon',
                     #'spor-aletleri',
                     #'hobi',
                     #'kirtasiye-ofis-malzemeleri',
                     #'otomobil-ve-motosiklet',
                     #'yapi-market',
                     #'ev-bakim-ve-temizlik',
                     #'kuru-gida-urunleri',
                     #'kozmetik',
                     #'saglik',
                     #'pet-shop-urunleri',
                     #'organik-urunler',
                     #'makyaj',
                     #'parfum-ve-deodorant',
                     #'cilt-bakimi',
                     #'sac-bakimi',
                     #'tiras-agda-epilasyon',
                     #'kadin+ayakkabi',
                     #'erkek+ayakkabi',
                     #'cocuk+ayakkabi',
                     #'kadin+giyim',
                     #'erkek+giyim',
                     #'cocuk+giyim',
                     #'kadin+kozmetik',
                     #'erkek+kozmetik',
                     #'kadin+canta',
                     #'erkek+canta',
                     #'cocuk+canta',
                     #'kadin+aksesuar',
                     #'erkek+aksesuar',
                     #'cocuk+aksesuar'
                     ]

product_search_result={}

class ProductSetManager:
    def __init__(self,project_id,location):
        self.project_id=project_id
        self.location=location

        self.client=vision.ProductSearchClient()

        self.location_path=self.client.location_path(project=self.project_id,location=self.location)

    def CreateProductSet(self,ps_id,ps_display_name):
        product_set=vision.types.ProductSet(display_name=ps_display_name)
        response=self.client.create_product_set(parent=self.location_path,product_set=product_set,product_set_id=ps_id)

        print('created product set:',response.name)

    def DeleteProductSet(self,ps_id):
        product_set_path=self.client.product_set_path(project=self.project_id,location=self.location,product_set=ps_id)
        self.client.delete_product_set(name=product_set_path)

        print('deleted product set:',ps_id)

    def GetProductSets(self):
        return self.client.list_product_sets(parent=self.location_path)

    def PrintProductSets(self):
        product_sets=list(self.GetProductSets())
        if len(product_sets)==0:
            print('no product set found')
            return

        for product_set in product_sets:
            print('name:',product_set.name)
            print('display name:',product_set.display_name)

    def CreateProduct(self,product_id,product_display_name,product_description,category='general-v1',labels={'keys':[],'values':[]}):
        key_value=[]
        for i in range(len(labels['keys'])):
            key_value.append(vision.types.Product.KeyValue(key=labels['keys'][i],value=labels['values'][i]))

        product=vision.types.Product(display_name=product_display_name,product_category=category,description=product_description,product_labels=key_value)
        response=self.client.create_product(parent=self.location_path,product=product,product_id=product_id)

        print('created product:',response.name)

    def DeleteProduct(self,product_id):
        product_path=self.client.product_path(project=project_id,location=self.location,product=product_id)
        self.client.delete_product(name=product_path)
        
        print('product deleted:',product_id)

    def UpdateProductLabels(self,product_id,labels):
        product_path=self.client.product_path(project=self.project_id,location=location,product=product_id)

        key_value=[]
        for i in range(len(labels['keys'])):
            key_value.append(vision.types.Product.KeyValue(key=labels['keys'][i],value=labels['values'][i]))

        product=vision.types.Product(name=product_path,product_labels=key_value)
        update_mask=vision.types.FieldMask(paths=['product_labels'])
        updated_product=self.client.update_product(product=product,update_mask=update_mask)

        print('updated product labels:',product.name,'labels:',product.product_labels)
    
    def InsertProductToProductSet(self,product_id,product_set_id):
        product_set_path=self.client.product_set_path(project=self.project_id,location=self.location,product_set=product_set_id)
        product_path=self.client.product_path(project=self.project_id,location=self.location,product=product_id)
        self.client.add_product_to_product_set(name=product_set_path,product=product_path)

        print('product:',product_id,'is added to product set:',product_set_id)

    def GetProduct(self,product_id):
        products=list(self.GetAllProducts())
        if len(products)==0:
            print('no product found')
            return
        
        for product in products:
            if product_id==product.name.split('/')[-1]:
                print('found product:',product_id)
                return product

        print('couldnt find product:',product_id)
        return None

    def PrintProduct(self,product_id):
        products=list(self.GetAllProducts())
        if len(products)==0:
            print('no product found')
            return

        for product in products:
            if product_id==product.name.split('/')[-1]:
                print('product id:',product.name)
                print('product name:',product.name.split('/')[-1])
                print('product display name:',product.display_name)
                print('product description:',product.description)
                print('product category:',product.product_category)
                print('product labels:',product.product_labels)
                return

        print('couldnt find product:',product_id)
        return None

    def GetAllProducts(self):
        return self.client.list_products(parent=self.location_path)

    def PrintAllProducts(self):
        products=list(self.GetAllProducts())
        if len(products)==0:
            print('no product found')
            return
        
        for product in products:
            self.PrintProduct(product.name.split('/')[-1])

    def AddReferenceImage(self,product_id,gcs_uri):
        product_path=self.client.product_path(project=self.project_id,location=self.location,product=product_id)

        reference_image=vision.types.ReferenceImage(uri=gcs_uri)
        image=self.client.create_reference_image(parent=product_path,reference_image=reference_image,reference_image_id=product_id+'-img')

    def ProductSearch(self,image_content,product_set_id):
        print("ProdycSearch")
        global product_search_result
        image_annotator_client=vision.ImageAnnotatorClient()
        
        image_content = image_content.encode('utf-8')

        # print("*"*100+image_filename)
        
        # with open('static/yuklemeler/'+image_filename,'rb') as image_file:
        #     image_content=image_file.read()

        image=vision.types.Image(content=image_content)
        print('DOSYA OKUNDU')
        product_set_path=self.client.product_set_path(project=self.project_id,location=self.location,product_set=product_set_id)
        product_search_params=vision.types.ProductSearchParams(product_set=product_set_path,product_categories=['general-v1'],filter=None)
        print("Parametreler Oluşturukdu.")
        image_context=vision.types.ImageContext(product_search_params=product_search_params)

        response=image_annotator_client.product_search(image,image_context=image_context)
        print('YANIT ALINDI.')

        print(len(response.product_search_results.results))
        #print(product_search_result.results[0].product.product_labels[0].key)
        product_search_result=[]
        for result in response.product_search_results.results:
            product=result.product

            product_id=product.name.split('/')[-1]
            product_name=product.display_name

            product_labels=[]
            for label in product.product_labels:
                product_labels.append({'key':label.key,'value':label.value})
            
            score=result.score
            image_url=result.image
            image_url='https://storage.cloud.google.com/main-product-set/main-product-set-images/'+image_url.split('/')[-1]+'?authuser=4'

            product_search_result.append({'id':product_id,
                                          'score':score,
                                          'description':product_name,
                                          'image_url':image_url,
                                          'labels':product_labels})

        return product_search_result

class CloudStorageUploader():
    def __init__(self,bucket_name):
        self.client=storage.Client()

        self.bucket=self.client.get_bucket(bucket_name)

    def UploadToBucket(self,blob_name,path_to_file):
        blob = self.bucket.blob(blob_name)
        
        blob.upload_from_filename(path_to_file)
    
        return blob.public_url

    def SaveImage(self,url,filename):
        with open(filename, 'wb') as handle:
            response = requests.get(url, stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)

    
if __name__=='__main__':
    
    project_id='vision-api-291709'
    location='europe-west1'

    ps_manager=ProductSetManager(project_id,location)
    with open('trendyol.jpg','rb') as image_file:
            image_content=image_file.read()
    image=base64.b64encode(image_content)
    ps_manager.ProductSearch(image,'main-product-set')
    print(product_search_result)
    # #ps_manager.CreateProductSet('main-product-set','Main Product Set')
    # bucket_manager=CloudStorageUploader('main-product-set-images')
    # username='ErenSonmez'
    # password='8o90bOBvm0UvkX2B'
    # cluster_name='UrunGirisiCluster'

    # ps_manager.DeleteProduct('tyl-6867233')

    # # with open('tracker.pkl','rb') as f:
    # #     added_ids=pickle.load(f)

    # db_manager=DatabaseManager(username,password,cluster_name)

    # trendyol_db=db_manager.GetDatabase('trendyol')
    # for category in trendyol_categories:
    #     category=category.replace('--','-').replace('+','-')
    #     print('adding category to product set:',category)

    #     collection=db_manager.GetCollection(category,trendyol_db)
    #     items=db_manager.GetAllItems(collection)
        
    #     for item in items:
    #         item_id='tyl-'+str(item['id'])

    #         if item_id in added_ids:
    #             print(item_id,'already exists')
    #             continue
            
    #         print('adding',item_id,item['description'],'-',category)
    #         ps_manager.CreateProduct(item_id,item['description'],item['description'],labels=item['labels'])

    #         img_filename='imgs/'+item_id+'.jpg'
    #         bucket_manager.SaveImage(item['image_url'],img_filename)
    #         bucket_manager.UploadToBucket(img_filename.split('/')[-1],img_filename)
    #         gcs_uri='gs://main-product-set-images/'+img_filename.split('/')[-1]
    #         ps_manager.AddReferenceImage(item_id,gcs_uri)
    #         ps_manager.InsertProductToProductSet(item_id,'main-product-set')
    #         print('added item:',item_id,item['description'])
    #         added_ids.append(item_id)
    #         with open('tracker.pkl','wb') as f:
    #             pickle.dump(added_ids,f)
            

    #manager.CreateProductSet('test-ps','test-ps-dn')
    #manager.PrintProductSets()
    #manager.DeleteProductSet('test-ps')
    #manager.PrintProductSets()

    #manager.DeleteProduct('test-prod')
    #manager.CreateProduct('test-prod','test-prod-dn','test-prod-description')
    #manager.PrintAllProducts()
    #manager.UpdateProductLabels('test-prod',{'keys':['test-key-1','test-key-2'],'values':['test-value-1','test-value-2']})
    #manager.PrintAllProducts()

    #manager.CreateProduct('test-prod','test-prod-dn','test-prod-description',labels={'keys':['test-label-key-1'],'values':['test-label-value-1']})
    #manager.PrintProduct('test-prod')
    #manager.DeleteProduct('test-prod')
    #manager.PrintAllProducts()

    #manager.CreateProductSet('test-ps','test-ps-dn')
    #manager.CreateProduct('test-prod','test-prod-dn','test-prod-desc')
    #manager.InsertProductToProductSet('test-prod','test-ps')

    #manager.DeleteProduct('test-prod')
    #manager.DeleteProductSet('test-ps')
    


    