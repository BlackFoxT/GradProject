from flask import request, session
from flask_babel import Babel

def get_locale():
    if 'lang' in request.args:
        lang = request.args.get('lang')
        if lang in ['en', 'tr']:
            session['lang'] = lang
            return session['lang']
    elif 'lang' in session:
        return session.get('lang')
    return request.accept_languages.best_match(['en', 'tr'])