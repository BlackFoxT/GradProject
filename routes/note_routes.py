from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, flash
from datetime import datetime
from models import db
from models.notes import Note
from flask_login import current_user, login_required

# Create a Blueprint for note-related routes
note_routes = Blueprint('note_routes', __name__)

@note_routes.route("/saveNote", methods=["POST"])
def saveNote():
    content = request.json.get('content')
    num = request.json.get('number')
    number = num
    
    notes = Note.query.filter_by(user_id=current_user.id, chat_id=current_user.currentChatID).all()
    if notes:
        last_note = Note.query.filter_by(
            user_id=current_user.id,
            chat_id=current_user.currentChatID
        ).order_by(Note.note_id.desc()).first()
        print(last_note.note_id)
        number = last_note.note_id + 1 if last_note else 1
    note = Note.query.filter_by(user_id=current_user.id, note_id=num, chat_id=current_user.currentChatID).first()

    if note is None:
        note = Note(user_id=current_user.id, chat_id=current_user.currentChatID, note_id=number, text=content)
        db.session.add(note)
    else:
        note.text = content

    db.session.commit()
    #flash('Note have been saved.', 'success')
    return jsonify({})

@note_routes.route("/get-note-history", methods=["GET"])
def get_note_history():
    current_chat_id = current_user.currentChatID
    
    # Filter notes by current user and current chat
    notes = Note.query.filter_by(user_id=current_user.id, chat_id=current_chat_id).all()

    notes_data = [
        {
            "note_id": note.note_id,
            "text": note.text,
            "chat_id": note.chat_id
        }
        for note in notes
    ]
    return jsonify(notes_data), 200

@note_routes.route('/note/delete/<int:id>', methods=['POST'])
@login_required
def delete_note(id):
    note = Note.query.filter_by(user_id=current_user.id, chat_id=current_user.currentChatID, note_id=id).first()
    if note:
        db.session.delete(note)
        db.session.commit()


    db.session.commit()
    flash('Note have been deleted.', 'success')
    return redirect(url_for('chat_routes.note')) 


@note_routes.route("/askForNote", methods=["POST"])
def askNote():
    number = request.json.get('number')
    notes = Note.query.filter_by(user_id=current_user.id, chat_id=current_user.currentChatID).all()
    if notes:
        last_note = Note.query.filter_by(
            user_id=current_user.id,
            chat_id=current_user.currentChatID
        ).order_by(Note.note_id.desc()).first()
        print(last_note.note_id)
        number = last_note.note_id + 1 if last_note else 1
        
    #flash('Note have been saved.', 'success')
    return jsonify({"number": number})