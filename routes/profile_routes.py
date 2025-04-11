from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.chat_history import ChatHistory
from models.information import Information
from models import db

# Create a blueprint for profile-related routes
profile_bp = Blueprint('profile_routes', __name__)

@profile_bp.route("/profile")
@login_required
def profile_page():
    user_chats = ChatHistory.query.filter_by(user_id=current_user.id).all()
    current_user.currentChatID = None
    # Save the change to the database
    db.session.commit()
    user_information = Information.query.filter_by(user_id=current_user.id).first()
    return render_template("profile.html", info=user_information, user_chats=user_chats)

@profile_bp.route('/update_information', methods=['POST'])
@login_required
def update_information():
    name = request.form.get('name')
    surname = request.form.get('surname')
    telephone_number = request.form.get('telephone_number')

    user_information = Information.query.filter_by(user_id=current_user.id).first()
    if user_information:
        user_information.name = name
        user_information.surname = surname
        user_information.telephone_number = telephone_number
    else:
        user_information = Information(
            user_id=current_user.id,
            name=name,
            surname=surname,
            telephone_number=telephone_number
        )
        db.session.add(user_information)

    db.session.commit()
    flash("Information updated successfully!", "success")
    return redirect(url_for('profile_routes.profile_page'))
