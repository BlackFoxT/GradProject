from flask import Blueprint, jsonify, flash, redirect, url_for, render_template, request
from models import db
from models.quiz import Quiz
from models.quiz_question import QuizQuestion
from models.quiz_result import QuizResult
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
    

    
    # Check if quiz already exists
     # 🧹 Delete existing quiz and its questions if exists
    existing_quiz = Quiz.query.filter_by(user_id=current_user.id, chat_id=current_user.currentChatID).first()
    if existing_quiz:
        chat_history = ChatHistory.query.filter_by(user_id=current_user.id, id=current_user.currentChatID).first()
        quizResult = QuizResult.query.filter_by(chatId=current_user.currentChatID).first()
        
        quizScore = quizResult.score
        print(quizScore)
        if quizScore >= 10 :
            if chat_history.difficulty == "easy" :
                chat_history.difficulty = "medium"
            else:
                chat_history.difficulty = "hard"
            
        # Delete associated questions
        QuizQuestion.query.filter_by(quiz_id=existing_quiz.id).delete()

        # Optionally delete the quiz result too if you have that
        QuizResult.query.filter_by(chatId=current_user.currentChatID).delete()

        db.session.delete(existing_quiz)
        db.session.commit()

    difficulty = chat_history.difficulty
    print(difficulty)
    prompt = "Generate only " + str(10) + " multiple-choice questions about " + topic + " and the difficulty level is " + difficulty + ". Provide the correct answer for each question. Use the following format:\n\n" + \
            "Question: [Write the question here]\n" + \
            "Choices:\n" + \
            "A) [Option A]\n" + \
            "B) [Option B]\n" + \
            "C) [Option C]\n" + \
            "D) [Option D]\n" + \
            "Correct Answer: [Write the correct option letter, e.g., A), B), C), or D)]\n\n" + \
            "Ensure the questions strictly follow this format and are consistent."
   
    response = None
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
        return redirect(url_for('home_routes.home_page'))

    quiz = Quiz.query.filter_by(user_id=current_user.id, chat_id=chat_id).first()
    if not quiz:
        flash("Quiz not found", "error")
        return redirect(url_for('home_routes.home_page'))

    return render_template("quiz_start.html", quiz=quiz)

@quiz_routes.route("/get-quiz-questions", methods=["GET"])
def get_quiz_questions():
    chat_id = current_user.currentChatID
    if chat_id is None:
        flash("No chat selected", "error")
        return redirect(url_for('home_routes.home_page'))

    quiz = Quiz.query.filter_by(user_id=current_user.id, chat_id=chat_id).first()
    if not quiz:
        flash("Quiz not found", "error")
        return redirect(url_for('home_routes.home_page'))

    questions = QuizQuestion.query.filter_by(quiz_id=quiz.id).all()
    quiz_questions = [{"question": q.text, "options": q.options, "correct_answer": q.correct_answer} for q in questions]

    return jsonify({"questions": quiz_questions})

@quiz_routes.route("/quiz")
def quiz():
    chat_id = current_user.currentChatID
    if chat_id is None:
        flash("No chat selected", "error")
        return redirect(url_for('home_routes.home_page'))

    quiz = Quiz.query.filter_by(user_id=current_user.id, chat_id=chat_id).first()
    if not quiz:
        flash("Quiz not found", "error")
        return redirect(url_for('home_routes.home_page'))

    existing_result = QuizResult.query.filter_by(chatId=chat_id).first()
    if existing_result:
        QuizResult.query.filter_by(chatId=current_user.currentChatID).delete()
        db.session.commit()

    questions = QuizQuestion.query.filter_by(quiz_id=quiz.id).all()
    quiz_questions = [{"question": q.text, "options": q.options} for q in questions]

    return render_template("quiz.html", quiz=quiz, questions=quiz_questions)

@quiz_routes.route("/quiz_result")
def quiz_result():
    return render_template("quiz_result.html")

@quiz_routes.route('/quiz/submit', methods=['POST'])
def submit_quiz():
    data = request.get_json()
    result = QuizResult(
        chatId=data['chatId'],
        score=data['score'],
        point=data['point'],
        passed=data['passed'],
        userAnswers=data['userAnswers'],
        correctAnswers=data['correctAnswers']
    )
    db.session.add(result)
    db.session.commit()
    return jsonify({'message': 'Quiz result saved to database.'}), 201

@quiz_routes.route('/quiz/result', methods=['GET'])
def get_quiz_result():
    chat_id = current_user.currentChatID
    result = QuizResult.query.filter_by(chatId=chat_id).first()
    
    if not result:
        return jsonify({"error": "Result not found"}), 404

    print(len(result.userAnswers))
    # Convert model to dict manually
    result_dict = {
        "score": result.score,
        "point": result.point,
        "passed": result.passed,
        "userAnswers": result.userAnswers,        # assuming it's a list (e.g., JSON column)
        "correctAnswers": result.correctAnswers   # same here
    }
    #print(result_dict)

    return jsonify(result_dict)



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

