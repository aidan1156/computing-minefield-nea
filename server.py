from flask import Flask, render_template, request, redirect,make_response, send_from_directory
import os

main_dir = os.path.dirname(os.path.realpath(__file__))#path to the server (paths referenced in the code are relative to this)

app = Flask(__name__,static_url_path='/static')#static is the directory with all images
app.config['PREFERRED_URL_SCHEME'] = 'https:'


@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')

@app.route('/sign-in',methods=['GET','POST'])
def sign_in():
    if request.method == 'GET':
        return render_template('sign-in.html')

if __name__ == '__main__':
    app.run(debug=True,port=5003)