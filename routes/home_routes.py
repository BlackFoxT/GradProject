from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from models import db
from models.chat_history import ChatHistory

home_routes = Blueprint('home_routes', __name__)

@home_routes.route("/")
def home_page():
    user_chats = None
    selected_chat = None

    if current_user.is_authenticated:
        user_chats = ChatHistory.query.filter_by(user_id=current_user.id).all()

    chat_id = request.args.get("chat_id", type=int)

    # Fetch the selected chat content, if chat_id is provided
    if chat_id:
        selected_chat = ChatHistory.query.filter_by(id=chat_id).first()
        
        # If no chat is found, flash an error message and redirect to home page
        if selected_chat is None:
            flash('Selected chat not found', 'error')
            return redirect(url_for('home_routes.home_page'))  # Redirect to the homepage if no chat found
        else:
            # If a valid chat is found, update currentChatID and save to the database
            current_user.currentChatID = chat_id
            db.session.commit()
    else:
        # If no chat is selected, set currentChatID to None
        current_user.currentChatID = None
        db.session.commit()

    # Render the home page with the user's chats and the selected chat (if any)
    return render_template(
        "index.html",
        user_chats=user_chats,
        selected_chat=selected_chat
    )
