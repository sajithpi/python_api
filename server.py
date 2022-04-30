

from cgitb import html
from os import environ
from model import User,Session,engine
from urllib.parse import urlparse
from urllib.parse import parse_qs

def render_template(template_name="index.html",context={}):
    html_str = ""
    with open(template_name, 'r') as f:
        html_str = f.read()
        html_str = html_str.format(**context)
    return html_str 

def home(environ,path):
    return render_template(template_name='index.html',context={"path":path})

def contact(environ,url):
    parsed_url = urlparse(url)
    # captured_id = parse_qs(parsed_url.query)['id'][0]
    # captured_name = parse_qs(parsed_url.query)['name'][0]
    local_session = Session(bind=engine)
    result = local_session.query(User).first()
    print(result.username)
    return render_template(template_name='contact.html',context={})
def addUser(environ,url):
    parsed_url = urlparse(url)
    captured_name = parse_qs(parsed_url.query)['name'][0]
    captured_email=parse_qs(parsed_url.query)['email'][0]
    local_session = Session(bind=engine)
    username = input("Enter your name")
    email = input("enter email")
    user = User(username=captured_name,email=captured_email)
    local_session.add(user)
    local_session.commit()
    print(username,"Inserted Successfully")
    return render_template(template_name="add_user.html",context={"name":username})   
def not_found(environ,path):
    return render_template(template_name='404.html',context={"path":path})

def app(environ, start_response):
    path = environ.get("PATH_INFO")
    url = environ.get("RAW_URI")
    
    for k,v in environ.items():
        print(k,v)
    if path.endswith("/"):
        path = path[:-1]
        
    if path == "" :
        data = home(environ,path)
    elif path == "/contact":
    
        data = contact(environ,url)
    elif path == "/add":
    
        data = addUser(environ,url)
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
