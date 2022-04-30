

from cgitb import html
from os import environ
from model import User,Session,engine

def render_template(template_name="index.html",context={}):
    html_str = ""
    with open(template_name, 'r') as f:
        html_str = f.read()
        html_str = html_str.format(**context)
    return html_str 

def home(environ,path):
    return render_template(template_name='index.html',context={"path":path})

def contact(environ,name):
    local_session = Session(bind=engine)
    result = local_session.query(User).first()
    print(result.username)
    return render_template(template_name='contact.html',context={"name":result.username})
def addUser(environ):
    local_session = Session(bind=engine)
    user = User(username="hadi",email="hadi@gmail.com")
    local_session.add(user)
    local_session.commit()
    return render_template(template_name="add_user.html",context={"name":"hadi"})   
def not_found(environ,path):
    return render_template(template_name='404.html',context={"path":path})

def app(environ, start_response):
    path = environ.get("PATH_INFO")
    if path.endswith("/"):
        path = path[:-1]
    if path == "" :
        data = home(environ,path)
    elif path == "/contact":
    
        data = contact(environ,"contact here")
    elif path == "/add":
    
        data = addUser(environ)
    else:
        data = render_template(template_name='404.html',context={"path":path})
  
    data = data.encode("utf-8")
    start_response(
        f"200 OK",[
            ("Content-Type","text/html"),
            ("Content-Length",str(len(data)))
        ]
    )
    return iter([data])