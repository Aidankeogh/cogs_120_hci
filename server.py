from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from backend import get_backend, set_backend
import yaml
import string
import random
# Check out flask cheat sheet here
# https://s3.us-east-2.amazonaws.com/prettyprinted/flask_cheatsheet.pdf

app = Flask(__name__)
Bootstrap(app)

def create_url():
    url = ''
    for i in range(3):
        url += random.choice(string.ascii_letters + string.digits)
    return url

backend = get_backend()
@app.route('/', methods=['GET', 'POST'])
@app.route('/search', methods=['GET', 'POST'])
def search():
    backend = get_backend()
    if request.method == 'POST': #this block is only entered when the form is submitted
        r = request.form
        print r
        if  'edit' in r: # attend event
            link = r['edit']
            e = backend['events'][link]
            e['title'] = r[link+'title']
            e['date'] = r[link+'date']
            e['location'] = r[link+'location']
            e['description'] = r[link+'description']
        if  'attend' in r: # attend event
            link = r['attend']
            e = backend['events'][link]
            e['attendees'].append(r[link+'name'])
            backend['users'][backend['user']]['events'].append(link)
        if  'unattend' in r: # attend event
            link = r['unattend']
            e = backend['events'][link]
            e['attendees'].remove(r[link+'name'])
            backend['users'][backend['user']]['events'].remove(link)
        set_backend(backend)

    return render_template('search.html', backend = backend)

@app.route('/<something>', methods=['GET', 'POST'])
def other_profile(something):
    backend = get_backend()
    if request.method == 'POST': #this block is only entered when the form is submitted
        r = request.form
        print r
        if  'edit' in r: # attend event
            link = r['edit']
            e = backend['events'][link]
            e['title'] = r[link+'title']
            e['date'] = r[link+'date']
            e['location'] = r[link+'location']
            e['description'] = r[link+'description']
        if  'attend' in r: # attend event
            link = r['attend']
            e = backend['events'][link]
            e['attendees'].append(r[link+'name'])
        if  'unattend' in r: # attend event
            link = r['unattend']
            e = backend['events'][link]
            e['attendees'].remove(r[link+'name'])
        if 'edituser' in r:
            link = r['edituser']
            u = backend['users'][link]
            u['name'] = r[link+'name']
            u['picture'] = r[link+'picture']
            u['about'] = r[link+'about']
            u['email'] = r[link+'email']
        if 'newevent' in r:
            url = create_url()
            while(url in backend['events']):
                url = create_url()
            backend['events'][url] = {}
            e = backend['events'][url]
            e['attendees'] = []
            e['host'] = backend['user']
            e['title'] = r['newtitle']
            e['date'] = r['newdate']
            e['description'] = r['newdescription']
            e['location'] = r['newlocation']
            e['img_src'] = ''
            e['link'] = url
            backend['users'][backend['user']]['events'].append(url)
            set_backend(backend)
            return redirect("/"+url, code=302)
        if 'delete' in r:
            link = r['delete']
            e = backend['events'][link]
            for user in e['attendees']:
                backend['users'][user]['events'].remove(link)
            backend['users'][e['host']]['events'].remove(link)
            del backend['events'][link]
            set_backend(backend)
            return redirect("/", code=302)


        set_backend(backend)

    if something in backend['users']:
        user = something
        return render_template('profile.html', backend = backend, user=user)
    elif something in backend['events'] :
        event = something
        return render_template('event.html', backend = backend, event=backend['events'][event])
    else:
        return render_template('404')

@app.route('/login', methods=['GET', 'POST'])
def login():
    backend = get_backend()
    if backend['logged_in'] :
        print 'here'
        backend['user'] = None
        backend['logged_in'] = False
        print backend
        set_backend(backend)

    if request.method == 'POST': #this block is only entered when the form is submitted
        r = request.form
        if 'login' in r:
            backend['logged_in'] = True
            if request.form['username'] not in backend['users']:
                backend['user'] = 'percy'
            else:
                backend['user'] = request.form['username']
            set_backend(backend)
            return redirect("/"+backend['user'], code=302)
        if 'create' in r:
            backend['users'][r['link']] = {}
            u = backend['users'][r['link']]
            u['name'] = r['name']
            u['link'] = r['link']
            u['badges'] = [None,None,None,None]
            u['events'] = []
            u['email'] = r['email']
            u['about'] = ''
            u['friends'] = []
            u['picture'] = r['picture']
            backend['user'] = r['link']
            backend['logged_in'] = True
            set_backend(backend)
            return redirect("/"+backend['user'], code=302)


    return render_template('login.html', backend = backend)


@app.route('/about')
def about():
    return render_template('about.html', backend = backend)

@app.route('/favicon.ico')
def favicon():
    return 'null'

@app.route('/new_event', methods=['GET', 'POST'])
def new_event():
    return render_template('new_event.html', backend = backend)





if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
