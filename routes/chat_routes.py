# chat_routes.py
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, flash
from datetime import datetime
from models import db
from models.chat_history import ChatHistory
from models.information import Information
from models.quiz import Quiz
from models.quiz_question import QuizQuestion
from models.quiz_result import QuizResult
from models.notes import Note
from flask_login import current_user, login_required
from routes.llm import llm  # Assuming this is where llm.invoke is defined
import re
import markdown

# Create a Blueprint for chat-related routes
chat_routes = Blueprint('chat_routes', __name__)

@chat_routes.route("/chatl")
@login_required
def chatl():
    # Get the 'id' query parameter from the URL
    chat_id = request.args.get('id', type=int)
    
    if chat_id:
        # Fetch the chat history and ensure it belongs to the current user
        chat_history = ChatHistory.query.filter_by(user_id=current_user.id, id=chat_id).first()
        if chat_history:
            current_user.currentChatID = chat_id  # Store the current chat ID
            # Save the change to the database
            db.session.commit()

    # Redirect to home_page with the chat_id as a query parameter
    return redirect(url_for("home_routes.home_page", chat_id=chat_id))


@chat_routes.route("/get-chat-history", methods=["GET"])
def get_chat_history():
    topic = request.args.get("topic", "General")  # Default topic or fetch from user preference
    if current_user.is_authenticated:
        if current_user.currentChatID is None:
            return jsonify({"contentVisible": False, "chats": [],"isUser": True})
        # For authenticated users, fetch chat history from the database

        chat_history = ChatHistory.query.filter_by(id=current_user.currentChatID).first()

        if chat_history.is_quizstarted or chat_history.realchat_count == 0:
              chat_history.is_quizstarted = False
            
        if chat_history:

            return jsonify({# Assuming `chats` is JSON serializable
                "contentVisible": True,
                "chats": chat_history.chats,
                "chatId": current_user.currentChatID,
                "chatCount":  chat_history.realchat_count,
                "isQuizSubmitted": chat_history.is_sumbitted,
                "isQuizStarted": chat_history.is_quizstarted,
                "extraChat": chat_history.extrachat,
                "isUser": True  
            })
        else:
            return jsonify({"contentVisible": False, "chats": [],"isUser": True})
    else:
        # For non-authenticated users, use localStorage or session to fetch chat history
        chat_history = session.get("chat_history", {})

        return jsonify({
            "contentVisible": bool(chat_history),  # Check if there are any chats for this topic
            "chats": chat_history,
            "isUser": False
        })

@chat_routes.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get('message')
    topic = request.json.get('chatTopic')

    if topic is None:
        topic = request.json.get('topic', 'General')
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    response = None
    realchatflag = False

    if user_message.startswith('!'):
        realchatflag = True
        command = user_message[1:].lower()

        if command in ['userinfo', 'kullanıcıbilgisi']:
            if current_user.is_authenticated:
                response = "Redirecting to your profile page..."
            else:
                response = "You need to be logged in to view your profile."

        elif command in ['quiz', 'sınav']:
            if current_user.is_authenticated:
                response = "Redirecting to the quiz page..."
            else:
                response = "You need to be logged in to access the quiz page."

        elif command == 'help':
            response = (
                "Here are the available commands:\n"
                "!time / !saat - Get the current server time\n"
                "!date / !tarih - Show today's date\n"
                "!userinfo / !kullanıcıbilgisi - Display your account information\n"
                "!note / !note - Directly open note page\n"
                "!clearhistory / !temizle - Clear your chat history\n"
                "!about / !hakkında - Learn more about me\n"
            )
        elif command == 'yardım':    
            response = (
                "Mevcut komutlar şunlardır:\n"
                "!time / !saat - Sunucunun mevcut saatini gösterir\n"
                "!date / !tarih - Bugünün tarihini gösterir\n"
                "!userinfo / !kullanıcıbilgisi - Kullanıcı bilgilerinizi gösterir\n"
                "!note / !note - note sayfasına yönlendirir\n"
                "!clearhistory / !temizle - Sohbet geçmişinizi siler\n"
                "!about / !hakkında - Benim hakkımda bilgi verir\n"
            )
        elif command == 'time':
            response = f"The current server time is: {datetime.now().strftime('%H:%M:%S')}"
        elif command == 'saat':
            response = f"Sunucu saati: {datetime.now().strftime('%H:%M:%S')}"
        elif command == 'date':
            response = f"Today's date is: {datetime.now().strftime('%Y-%m-%d')}"
        elif command == 'tarih':
            response = f"Bugünün tarihi: {datetime.now().strftime('%Y-%m-%d')}"
        elif command == 'about':
            response = (
                "I am an educational bot designed to assist you with various topics.\n"
                "My purpose is to provide helpful information, guide you through lessons, and answer your questions on a variety of subjects.\n"
            )
        elif command == 'hakkında':    
            response = (
                "Ben bir eğitim botuyum, çeşitli konularda size yardımcı olmak için tasarlandım.\n"
                "Amacım, size faydalı bilgiler sunmak, derslerde rehberlik yapmak ve birçok konuda sorularınızı cevaplamak.\n"
            )
        else:
            response = "Command cannot be found! Type !help or !yardım to see the available commands."
    else:
        response = llm.invoke(user_message)
        response = markdown.markdown(response)
    chat_entry = {
        "question": user_message,
        "response": response,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    if current_user.is_authenticated:

        if current_user.currentChatID is None:
            chat_history = ChatHistory(user_id=current_user.id, topic=topic, chats=[])
        else:
            chat_history = ChatHistory.query.filter_by(id=current_user.currentChatID).first()

        if chat_history.realchat_count is None:
            chat_history.realchat_count = 0
        chat_history.extrachat = 0
        if realchatflag is False:
            chat_history.realchat_count += 1
        else:
            chat_history.extrachat = 1

        if chat_history.realchat_count > 0 or chat_history.realchat_count < 10:
            chat_history.is_sumbitted = False
            chat_history.is_quizstarted = False
        chat_history.chats.append(chat_entry)
        db.session.add(chat_history)
        db.session.commit()

        return jsonify({ # Assuming `chats` is JSON serializable
                "topic": topic,
                "chats": chat_history.chats,
                "chatCount":  chat_history.realchat_count,
                "chatId": chat_history.id,
                "isQuizSubmitted": chat_history.is_sumbitted,
                "isQuizStarted": chat_history.is_quizstarted,
                "extraChat": chat_history.extrachat,
                "isUser": True 
            })
    return jsonify({
        "topic": topic,
        "chat_entry": chat_entry,
        "isUser": False
    })

@chat_routes.route('/chat/delete/<int:id>', methods=['POST'])
@login_required
def delete_chat(id):
    # Get the chat
    chat_history = ChatHistory.query.filter_by(id=id).first_or_404()

    # Delete related Quiz
    existing_quiz = Quiz.query.filter_by(
        user_id=current_user.id,
        chat_id=chat_history.id,
        difficulty=chat_history.difficulty
    ).first()

    if existing_quiz:
        # Delete all quiz questions
        quiz_questions = QuizQuestion.query.filter_by(quiz_id=existing_quiz.id).all()
        for question in quiz_questions:
            db.session.delete(question)

        # Delete related QuizResult
        quiz_result = QuizResult.query.filter_by(quiz_id=existing_quiz.id).first()
        if quiz_result:
            db.session.delete(quiz_result)

        db.session.delete(existing_quiz)

    # Delete related Notes
    notes = Note.query.filter_by(user_id=current_user.id, chat_id=chat_history.id).all()

    if notes:
        for note in notes:
            db.session.delete(note)

    # Delete the chat history
    db.session.delete(chat_history)
    db.session.commit()

    return redirect(url_for('home_routes.home_page')) 


@chat_routes.route("/note")
@login_required
def note():
    user_chats = None
    selected_chat = None
    user_information = None
    
    if current_user.is_authenticated:
        user_information = Information.query.filter_by(user_id=current_user.id).first()
        user_chats = ChatHistory.query.filter_by(user_id=current_user.id).all()
        
    chat_id = current_user.currentChatID
    
    if chat_id:
        selected_chat = ChatHistory.query.filter_by(id=chat_id).first()
        
        # If no chat is found, flash an error message and redirect to home page
        if selected_chat.user_id != current_user.id:
            flash('Unathenticated chat is found, you can not enter !!!', 'error')
            return redirect(url_for('home_routes.home_page')) 
        
        # If no chat is found, flash an error message and redirect to home page
        if selected_chat is None:
            flash('Selected chat not found', 'error')
            return redirect(url_for('home_routes.home_page'))  
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
        "note.html",
        user_chats=user_chats,
        selected_chat=selected_chat,
        info=user_information
    )
