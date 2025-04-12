from flask import request, session, g

def get_locale():
    """
    Retrieves the language preference for the user. First checks the query parameter for 'lang'.
    If 'lang' is not found, it checks the session. If neither is set, it falls back to the browser's language.
    """
    # Check if the language query parameter is set and valid
    if 'lang' in request.args:
        lang = request.args.get('lang')
        if lang in ['en', 'tr']:
            session['lang'] = lang
            return session['lang']
    
    # If not set via query, check if we have it stored in the session
    elif 'lang' in session:
        return session.get('lang')
    
    # Otherwise, use the browser's preferred language
    return request.accept_languages.best_match(['en', 'tr'])

def get_timezone():
    """
    Retrieves the user's timezone from the session if available.
    Assumes that the user object is stored in the Flask global `g`.
    """
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone
