# chat_routes.py
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, flash
from datetime import datetime
from models import db
from models.chat_history import ChatHistory
from flask_login import current_user, login_required
from routes.llm import llm  # Assuming this is where llm.invoke is defined

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
        print(chat_history)

        if chat_history:
           # print(chat_history.chats)
            return jsonify({
                "contentVisible": True,
                "chats": chat_history.chats,
                "chatId": current_user.currentChatID,
                "isUser": True  # Assuming `chats` is JSON serializable
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
    #print(user_message)
    topic = request.json.get('chatTopic')
    if topic is None:
        topic = request.json.get('topic', 'General')
    #print(topic)
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    response = None

    if user_message.startswith('!'):
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

        chat_history.chats.append(chat_entry)
        db.session.add(chat_history)
        db.session.commit()

        return jsonify({
                "topic": topic,
                "chats": chat_history.chats,
                "chatId": chat_history.id,
                "isUser": True  # Assuming `chats` is JSON serializable
            })

    return jsonify({
        "topic": topic,
        "chat_entry": chat_entry,
        "isUser": False
    })


@chat_routes.route("/note")
@login_required
def note():
    user_chats = None
    selected_chat = None

    if current_user.is_authenticated:
        user_chats = ChatHistory.query.filter_by(user_id=current_user.id).all()

    chat_id = request.args.get("chat_id", type=int)
    print(chat_id)
    # Fetch the selected chat content, if chat_id is provided
    if chat_id:
        selected_chat = ChatHistory.query.filter_by(id=chat_id).first()
        
        # If no chat is found, flash an error message and redirect to home page
        if selected_chat.id != current_user.id:
            flash('Unathenticated chat is found, you can not enter !!!', 'error')
            return redirect(url_for('home_routes.home_page'))  # Redirect to the homepage if no chat found
        
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
        "note.html",
        user_chats=user_chats,
        selected_chat=selected_chat
    )
