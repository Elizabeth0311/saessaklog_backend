
from flask import Flask, render_template, request ,flash
from werkzeug.utils import secure_filename
from s3_conn import upload_file_to_s3 ,s3_connection
from config import S3_BUCKET_NAME 
import datetime as dt
import os



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
        file = request.files['file']
        file_name = file.filename.split('.')[0] # 파일명 
        ext = file.filename.split('.')[-1] # 확장자명 
        img_name = dt.datetime.now().strftime(f"{file_name}-%Y-%m-%d-%H-%H-%S.{ext}")
        print(img_name)
        print("==============")
        print(type(file))
        s3 = s3_connection
        upload_file_to_s3(s3,'saessalogfile',file, img_name)
        
        return '파일이 저장되었습니다'

    else :
        return render_template("file_upload.html")
'''
출처 https://gist.github.com/leongjinqwen/9d9a2d58bf2fb923658820559a88a5ec
'''


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
    app.run(host='0.0.0.0', port = 5000, debug=False)
