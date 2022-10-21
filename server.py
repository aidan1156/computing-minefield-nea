from http import server
from flask import Flask, render_template, request, redirect,make_response, send_from_directory
import os
import json
import server_query
import path_generation

main_dir = os.path.dirname(os.path.realpath(__file__))#path to the server (paths referenced in the code are relative to this)

app = Flask(__name__,static_url_path='/static')#static is the directory with all images
app.config['PREFERRED_URL_SCHEME'] = 'https:'


@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'GET':
        if request.cookies.get('user_token') == None:
            return redirect('/sign-in')
        return render_template('home.html')
    if request.method == 'POST':##handle requests to edit/get data
        data = json.loads(request.data)
        if data['request_type'] == 'get_designs':
            user_id = server_query.token_to_user_id(data['user_token'],request.cookies.get('user_token'))
            if not user_id:
                return json.dumps({'state':'signed out'})
            designs = server_query.get_designs(user_id)
            return json.dumps({'state':'done','designs':designs})
        if data['request_type'] == 'get_design':
            user_id = server_query.token_to_user_id(data['user_token'],request.cookies.get('user_token'))
            ##check the user owns the design
            if server_query.get_owner_of_design(data['id']) == user_id:
                #if the user owns it get the pattern
                pattern = server_query.get_design(data['id'])
                return json.dumps({'state':'done','design':pattern,'design_id':data['id']})
            else:
                return json.dumps({'state':'permission denied'})
        if data['request_type'] == 'save_design':
            try:
                user_id = server_query.token_to_user_id(data['user_token'],request.cookies.get('user_token'))
                ##check the user owns the design
                if server_query.get_owner_of_design(data['id']) == user_id:
                    ##if the user owns said design
                    server_query.save_design(data['id'],data['pattern'])
                    return json.dumps({'state':'done'})
                else:
                    return json.dumps({'state':'permission denied'})
            except:
                return json.dumps({'state':'failed'})
        if data['request_type'] == 'new_design':
            user_id = server_query.token_to_user_id(data['user_token'],request.cookies.get('user_token'))
            design_id = server_query.create_new_design(user_id,data['auto_generate'])
            return json.dumps({'state':'done','design_id':design_id})
        if data['request_type'] == 'auto_gen_design':
            pattern = path_generation.generate_path()
            return json.dumps({'state':'done','pattern':pattern})
        if data['request_type'] == 'delete_design':
            user_id = server_query.token_to_user_id(data['user_token'],request.cookies.get('user_token'))
            if user_id == server_query.get_owner_of_design(data['design_id']):
                server_query.delete_design(data['design_id'])
            return json.dumps({'state':'done','design_id':data['design_id']})
        if data['request_type'] == 'get_leaderboard':
            ##ensure the user is actually signed in even though we do nothing with the id
            user_id = server_query.token_to_user_id(data['user_token'],request.cookies.get('user_token'))
            leaderboard = server_query.get_leaderboard()
            return json.dumps({'state':'done','leaderboard':leaderboard})

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