from flask import request
from flask import Flask, render_template
from random import choice
import requests


app = Flask(__name__)


@app.route("/user/<user>", methods=['GET', 'POST'])
def user(user):
    if request.method == 'POST':
        search = request.form['search_term'].lower()
        
        page = 1
        gists = []
        raw_gists = 'first'
        
        while raw_gists:
            r = requests.get('https://api.github.com/users/'+user+'/gists?page=' + str(page))
            page += 1
            raw_gists = ''
            
            if r.ok:        
                raw_gists = r.json()
                for gist in raw_gists:
                    if search in gist['files'].keys()[0].lower() or search in gist['description'].lower():
                        gists.append(gist)

        if gists:
            return render_template('search.html', user=user, search_term=search, gists=gists)
        else:
            return ':-( something went wrong. I asked for: ' + r.url

    return render_template('search.html', user=user, search_term='')


if __name__ == '__main__':
    app.debug = True

    if app.config['DEBUG']:
        from werkzeug import SharedDataMiddleware
        import os
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
          '/': os.path.join(os.path.dirname(__file__), 'static'),
        })

    app.run('127.0.0.1', 5001)
