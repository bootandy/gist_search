from flask import request
from flask import Flask
from flask import jsonify
from flask.ext.classy import FlaskView
from random import choice
import requests

app = Flask(__name__)


class GistsView(FlaskView):

    def user(self, user):
        result = """
            <html>
            <body>
                <h1>Intuitive Gist Search for """+ user + """</h1>
                <p> Note the URL /\ above - bookmark it!
                </p>

                <p>Search my Gists:
                    <form id="lookup-form">
                        <input id='search_term' type='textbox'>
                        <button onclick='go()'>search</button>
                    </form>
                </p>

                <script>
                    function go() {
                        document.getElementById('lookup-form').onsubmit = function() {
                            window.location = '/gists/""" + user + """/' + document.getElementById('search_term').value;
                            return false;
                        };
                    }
                </script>

                </body>
            </html>
        """
        return result

    def index(self, user, search):
        result = ''
        r = requests.get('https://api.github.com/users/'+user+'/gists')

        if r.ok:
            raw_gists = r.json()
            result = '<h1>' + user + ' gists</h1><h2>search for ' + search + '</h2>'

            for gist in raw_gists:
                if search.lower() in gist['files'].keys()[0].lower() or search in gist['description'].lower():
                    result += '<p><a href="' + gist['html_url'] + '">' + gist['files'].keys()[0] + '</a> : ' + gist['description'] + ' : ' + '</p>'
        else:
            result = ':-( something went wrong. I asked for: ' + r.url

        return result


GistsView.register(app)


if __name__ == '__main__':
    app.debug = True

    if app.config['DEBUG']:
        from werkzeug import SharedDataMiddleware
        import os
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
          '/': os.path.join(os.path.dirname(__file__), 'static')
        })

    app.run('127.0.0.1', 5001)
