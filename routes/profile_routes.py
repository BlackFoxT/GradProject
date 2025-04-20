from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.chat_history import ChatHistory
from models.information import Information
from models.quiz import Quiz
from models.quiz_result import QuizResult
from models import db
from utils.file_upload import save_profile_image


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
    quizzes = (
        db.session.query(Quiz, QuizResult)
        .join(QuizResult, Quiz.id == QuizResult.quiz_id)
        .filter(Quiz.user_id == current_user.id)
        .order_by(QuizResult.timestamp.desc())
        .all()
    )
    result_list = []
    for quiz, result in quizzes:
        current_chat = ChatHistory.query.filter_by(id=quiz.chat_id).first()
        topic = current_chat.topic if current_chat else "Unknown Topic"
        difficulty = getattr(quiz, 'difficulty', 'Normal')
        result_list.append({
            "difficulty": difficulty,
            "title": f"{topic} - {difficulty} Quiz",
            "score": result.score,
            "correct": result.point,
            "total": 10,
            "time": 10,
            "date": result.timestamp.strftime("%b %d, %Y")
        })
    return render_template("profile.html", info=user_information, user_chats=user_chats, quiz_results=result_list)

@profile_bp.route('/update_information', methods=['POST'])
@login_required
def update_information():
    name = request.form.get('name')
    surname = request.form.get('surname')
    telephone_number = request.form.get('telephone_number')
    birth_date_str = request.form.get('birth_date')
    birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None
    gender = request.form.get('gender')
    address = request.form.get('address')
    language = request.form.get('language')
    file = request.files.get('profile_image')
    image_path = save_profile_image(file)
    

    user_information = Information.query.filter_by(user_id=current_user.id).first()
    if user_information:
        user_information.name = name
        user_information.surname = surname
        user_information.telephone_number = telephone_number
        user_information.birth_date = birth_date
        user_information.gender = gender
        user_information.address = address
        user_information.language = language
    else:
        user_information = Information(
            user_id=current_user.id,
            name=name,
            surname=surname,
            telephone_number = telephone_number,
            birth_date = birth_date,
            gender = gender,
            address = address,
            language = language
        )
        db.session.add(user_information)

    if image_path:
        user_information.profile_image = image_path
        
    db.session.commit()
    flash("Information updated successfully!", "success")
    return redirect(url_for('home_routes.home_page'))

