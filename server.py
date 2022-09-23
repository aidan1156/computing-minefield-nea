from flask import Flask, render_template, request, redirect,make_response, send_from_directory
import os
import json
import server_query

main_dir = os.path.dirname(os.path.realpath(__file__))#path to the server (paths referenced in the code are relative to this)

app = Flask(__name__,static_url_path='/static')#static is the directory with all images
app.config['PREFERRED_URL_SCHEME'] = 'https:'


@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    if request.method == 'POST':##handle requests to edit/get data
        data = json.loads(request.data)
        if data['request_type'] == 'get_designs':
            user_id = server_query.token_to_user_id(data['user_token'],request.cookies.get('user_token'))
            designs = server_query.get_designs(user_id)
            return json.dumps({'state':'done','designs':designs})

@app.route('/sign-in',methods=['GET','POST'])
def sign_in():
    if request.method == 'GET':
        return render_template('sign-in.html')
    if request.method == 'POST':
        data = json.loads(request.data)
        user_id = server_query.check_password(data['username'],data['password'])
        if user_id:
            token,cookie_token = server_query.create_token(user_id)
            resp = make_response(json.dumps({'state':'done','user_token':token}))##set the user token cookie that lasts a year
            resp.set_cookie('user_token', cookie_token,httponly = True,max_age=31536000, secure=True,samesite='Strict')
            return resp
        else:
            return json.dumps({'state':'Incorrect password or username'})

if __name__ == '__main__':
    app.run(debug=True,port=5003)