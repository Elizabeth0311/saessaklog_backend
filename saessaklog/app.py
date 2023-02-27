
from flask import Flask, render_template, request 
from werkzeug.utils import secure_filename
from s3_conn import upload_file_to_s3 ,s3_connection 
from config import S3_BUCKET_NAME 
import datetime as dt

import base64 
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import io
from io import BytesIO


app = Flask(__name__)

# @app.route("/main")
# def hello() :
#     return "Hello, World!"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 확장자 확인
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route("/file_upload", methods = ['GET', 'POST'])
def upload_file() :
    if request.method == 'POST' :
        # file = request.files['file']
  
        body = request.get_json()
       
        base_string = body['imageFile']# json 읽어오기 
        data = base_string.split(';base64,') # 확장자명과 base64 분리 
        img_string = data[1] # base64 
        ext =  data[0].split('/')[1]# 확장자
        content_type = data[0].split(':')[1]
        
        data= img_string + '='*(4-len(img_string)%4)#패딩
        decoded_image = base64.b64decode(data) # bytes
        
        
        img_buffer = io.BytesIO(decoded_image) # 바이트열 데이터 메모리버퍼로 전환
        img = Image.open(img_buffer) # 메모리 버퍼로부터 이미지 생성
        file_name = body['fileName'].split('.')[0]
        img.save(file_name)
        img_file = open(file_name, "rb")
        
        
      
        # file_name = file.filename.split('.')[0] # 파일명 
      
        # ext = file.filename.split('.')[-1] # 확장자명 
       
        img_name = dt.datetime.now().strftime(f"{file_name}-%Y-%m-%d-%H-%H-%S.{ext}")# ex) 파일명-2023-02-21-22-22-21.png
        print(img_name)
        
        # 버킷에 이미지 업로드 
        s3  = s3_connection()
        if upload_file_to_s3(s3,S3_BUCKET_NAME, img_file, img_name, content_type): 
            return img_name #'파일이 저장되었습니다. # 자바서버에 key값 주기 create 
                
        else : return '파일 저장 실패' 
        
    else : 
        return render_template("file_upload.html")


# @app.route("/file_upload", methods = ['GET', 'POST'])
# def file_upload() :
#     if request.method == 'POST' :
#         f = request.files['file'] # http에서 파일가져오기
#         # filename = f.save(secure_filename(f.filename))
#         filename = secure_filename(f.filename)
#         f.save(os.path.join('/Users/hyeri/Downloads/s3_save',filename))
        
 

    #     return '파일이 저장되었습니다.'
    # else : 
    #     return render_template("file_upload.html")

if __name__ == "__main__" :
    app.secret_key = "saessak_servser"
    app.run(host='0.0.0.0', port = 5000, debug=True)
