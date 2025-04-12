from flask_babel import gettext, get_locale

def inject_babel():
    return dict(_=gettext)

def inject_locale():
    # This makes the function available directly in templates
    return {'get_locale': get_locale}
