from flask import Blueprint, request, redirect, session
from flask_babel import gettext
# language_routes.py
from flask import Blueprint, redirect, request, session, url_for

# Create a Blueprint for language-related routes
language_bp = Blueprint('language_routes', __name__)

@language_bp.route('/change_language/<lang_code>')
def change_language(lang_code):
    """
    Change the language based on the lang_code parameter passed in the URL.
    The selected language will be saved in the session.
    """
    # Check if the lang_code is valid (could be 'en' or 'tr' based on your app's configuration)
    if lang_code in ['en', 'tr']:
        session['lang'] = lang_code  # Store the selected language in the session
    else:
        # If invalid lang_code, redirect to home page (optional handling)
        return redirect(url_for('home_page'))

    # Redirect to the referrer page or home page if no referrer is present
    return redirect(request.referrer or url_for('home_page'))

@language_bp.route('/setlang')
def setlang():
    lang = request.args.get('lang', 'en')
    session['lang'] = lang
    return redirect(request.referrer)

@language_bp.route('/js_translations')
def js_translations():
    translations = {
        'logoutText': gettext('Logout'),
        'accountText': gettext('Account'),
        'successTitle': gettext('Success!'),
        'successText': gettext('You are registered.'),
        'validEmail': gettext('Please enter a valid email address.')
    }
    return jsonify(translations)
