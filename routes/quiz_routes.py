from flask import Blueprint, jsonify, flash, redirect, url_for, render_template
from models import db
from models.quiz import Quiz
from models.quiz_question import QuizQuestion
from flask_login import current_user
import re
# Import models after db initialization
from models.user import User  
from models.chat_history import ChatHistory
from models.quiz import Quiz
from models.information import Information 
from models.quiz_question import QuizQuestion
from routes.llm import llm  # Import llm from llm.py
quiz_routes = Blueprint('quiz_routes', __name__)

@quiz_routes.route("/prepareQuestions", methods=["POST"])
def prepare_questions():
    # Get the topic from chat history
    chat_history = ChatHistory.query.filter_by(id=current_user.currentChatID).first()
    topic = chat_history.topic if chat_history.topic else "General"

    prompt = "Generate only " + str(10) + " multiple-choice questions about " + topic + ". Provide the correct answer for each question. Use the following format:\n\n" + \
            "Question: [Write the question here]\n" + \
            "Choices:\n" + \
            "A) [Option A]\n" + \
            "B) [Option B]\n" + \
            "C) [Option C]\n" + \
            "D) [Option D]\n" + \
            "Correct Answer: [Write the correct option letter, e.g., A), B), C), or D)]\n\n" + \
            "Ensure the questions strictly follow this format and are consistent."

    response = None
    # Check if quiz already exists
    existing_quiz = Quiz.query.filter_by(user_id=current_user.id, chat_id=current_user.currentChatID).first()
    if not existing_quiz:
        # Generate quiz and save
        response = llm.invoke(prompt)
        new_quiz = Quiz(user_id=current_user.id, chat_id=current_user.currentChatID)
        db.session.add(new_quiz)
        db.session.commit()

        # Parse questions and store them
        questions = parse_questions(response, quiz_id=new_quiz.id)
        db.session.add_all(questions)
        db.session.commit()

    return jsonify({
        "topic": topic,
        "response": response,
        "isUser": True,
        "chatId": current_user.currentChatID
    })

@quiz_routes.route("/quiz_start")
def quiz_start():
    chat_id = current_user.currentChatID
    if chat_id is None:
        flash("No chat selected", "error")
        return redirect(url_for('home_page'))

    quiz = Quiz.query.filter_by(user_id=current_user.id, chat_id=chat_id).first()
    if not quiz:
        flash("Quiz not found", "error")
        return redirect(url_for('home_page'))

    return render_template("quiz_start.html", quiz=quiz)

@quiz_routes.route("/get-quiz-questions", methods=["GET"])
def get_quiz_questions():
    chat_id = current_user.currentChatID
    if chat_id is None:
        flash("No chat selected", "error")
        return redirect(url_for('home_page'))

    quiz = Quiz.query.filter_by(user_id=current_user.id, chat_id=chat_id).first()
    if not quiz:
        flash("Quiz not found", "error")
        return redirect(url_for('home_page'))

    questions = QuizQuestion.query.filter_by(quiz_id=quiz.id).all()
    quiz_questions = [{"question": q.text, "options": q.options, "correct_answer": q.correct_answer} for q in questions]

    return jsonify({"questions": quiz_questions})

@quiz_routes.route("/quiz")
def quiz():
    chat_id = current_user.currentChatID
    if chat_id is None:
        flash("No chat selected", "error")
        return redirect(url_for('home_page'))

    quiz = Quiz.query.filter_by(user_id=current_user.id, chat_id=chat_id).first()
    if not quiz:
        flash("Quiz not found", "error")
        return redirect(url_for('home_page'))

    questions = QuizQuestion.query.filter_by(quiz_id=quiz.id).all()
    quiz_questions = [{"question": q.text, "options": q.options} for q in questions]

    return render_template("quiz.html", quiz=quiz, questions=quiz_questions)

@quiz_routes.route("/quiz_result")
def quiz_result():
    return render_template("quiz_result.html")


def parse_questions(raw_text, quiz_id):
    pattern = re.compile(
        r'\d+\.\s+(.+?)\nChoices:\nA\)\s(.+?)\nB\)\s(.+?)\nC\)\s(.+?)\nD\)\s(.+?)\nCorrect Answer:\s([A-D])\)',
        re.DOTALL
    )

    answer_map = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3
    }

    questions = []

    matches = pattern.findall(raw_text)
    for match in matches:
        question_text = match[0].strip()
        options = [match[1].strip(), match[2].strip(), match[3].strip(), match[4].strip()]
        correct_answer_index = answer_map[match[5]]
        correct_answer = options[correct_answer_index]

        questions.append(
            QuizQuestion(
                quiz_id=quiz_id,
                text=question_text,
                options=options,
                correct_answer=correct_answer
            )
        )

    return questions