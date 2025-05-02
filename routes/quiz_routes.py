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
    chat_history.is_quizstarted = True

    response = None
    # Check if quiz already exists
     # 🧹 Delete existing quiz and its questions if exists
    existing_quiz = Quiz.query.filter_by(user_id=current_user.id, chat_id=current_user.currentChatID, difficulty=chat_history.difficulty).first()
    if existing_quiz:
        chat_history = ChatHistory.query.filter_by(user_id=current_user.id, id=current_user.currentChatID).first()
        quizResult = QuizResult.query.filter_by(quiz_id=existing_quiz.id).first()
        
        if quizResult:
            quizScore = quizResult.score
            print(quizScore)
            if chat_history.difficulty == "hard":
                QuizQuestion.query.filter_by(quiz_id=existing_quiz.id).delete()
                QuizResult.query.filter_by(quiz_id=existing_quiz.id).delete()
                db.session.delete(existing_quiz)
            elif quizScore >= 70 :
                if chat_history.difficulty == "easy" :
                    chat_history.difficulty = "medium"
                else:
                    chat_history.difficulty = "hard"
            else:
                # Delete associated questions
                QuizQuestion.query.filter_by(quiz_id=existing_quiz.id).delete()
                # Optionally delete the quiz result too if you have that
                QuizResult.query.filter_by(quiz_id=existing_quiz.id).delete()
                db.session.delete(existing_quiz)

            db.session.commit()

        else:
            return jsonify({
                "topic": topic,
                "response": response,
                "isUser": True,
                "chatId": current_user.currentChatID
            })  

    print(chat_history.difficulty)
    prompt = (
        f"Generate exactly 10 multiple-choice questions about {topic} at a {chat_history.difficulty} difficulty level. "
        "Each question must strictly follow **this exact format**:\n\n"
        "Question: [Your question here]\n"
        "Choices:\n"
        "A) [Option A]\n"
        "B) [Option B]\n"
        "C) [Option C]\n"
        "D) [Option D]\n"
        "Correct Answer: [One of A, B, C, or D ONLY — no explanations]\n\n"
        "Do not include explanations or commentary. Return only the formatted questions exactly as shown above. "
        "Ensure consistent formatting for all 10 questions, with no additional content before or after the questions."
    )

   
        
    # Generate quiz and save
    response = llm.invoke(prompt)
    #print(response)
    new_quiz = Quiz(user_id=current_user.id, chat_id=current_user.currentChatID, difficulty=chat_history.difficulty)
    db.session.add(new_quiz)
    db.session.commit()

    # Parse questions and store them
    questions = parse_questions(response, quiz_id=new_quiz.id)
    #print("--------------------------")
    #print(questions)
    db.session.add_all(questions[:10])
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

    chat_history = ChatHistory.query.filter_by(id=chat_id).first()
    quiz = Quiz.query.filter_by(user_id=current_user.id, chat_id=chat_id, difficulty=chat_history.difficulty).first()
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

    chat_history = ChatHistory.query.filter_by(id=chat_id).first()
    quiz = Quiz.query.filter_by(user_id=current_user.id, chat_id=chat_id, difficulty=chat_history.difficulty).first()
    if not quiz:
        flash("Quiz not found", "error")
        return redirect(url_for('home_routes.home_page'))

    questions = QuizQuestion.query.filter_by(quiz_id=quiz.id).all()
    quiz_questions = [{"question": q.text, "options": q.options, "correct_answer": q.correct_answer} for q in questions]

    return jsonify({"quiz_id":quiz.id, "questions": quiz_questions})

@quiz_routes.route("/quiz")
def quiz():
    chat_id = current_user.currentChatID
    if chat_id is None:
        flash("No chat selected", "error")
        return redirect(url_for('home_routes.home_page'))

    chat_history = ChatHistory.query.filter_by(id=chat_id).first()
    quiz = Quiz.query.filter_by(user_id=current_user.id, chat_id=chat_id, difficulty=chat_history.difficulty).first()
    if not quiz:
        flash("Quiz not found", "error")
        return redirect(url_for('home_routes.home_page'))

    existing_result = QuizResult.query.filter_by(quiz_id=quiz.id).first()
    if existing_result:
        QuizResult.query.filter_by(quiz_id=quiz.id).delete()
        db.session.commit()

    questions = QuizQuestion.query.filter_by(quiz_id=quiz.id).all()
    quiz_questions = [{"question": q.text, "options": q.options} for q in questions]

    return render_template("quiz.html", quiz=quiz, questions=quiz_questions)

@quiz_routes.route("/quiz_result")
def quiz_result():
    return render_template("quiz_result.html")

@quiz_routes.route('/quiz/submit', methods=['POST'])
def submit_quiz():
    chat_history = ChatHistory.query.filter_by(user_id=current_user.id, id=current_user.currentChatID).first()
    chat_history.is_sumbitted = True
    data = request.get_json()
    result = QuizResult(
        quiz_id=data['quiz_id'],
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
    chat_history = ChatHistory.query.filter_by(id=chat_id).first()
    quiz = Quiz.query.filter_by(user_id=current_user.id, chat_id=chat_id, difficulty=chat_history.difficulty).first()
    result = QuizResult.query.filter_by(quiz_id=quiz.id).first()

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
    # Regular expression to extract questions
    #cleaned_text = re.sub(r"<think>.*?</think>", "", raw_text, flags=re.DOTALL)
    #print(raw_text)
     # Updated pattern
    pattern = re.compile(
        r"Question:\s*(.*?)\s*Choices:\s*A\)\s*(.*?)\s*B\)\s*(.*?)\s*C\)\s*(.*?)\s*D\)\s*(.*?)\s*Correct Answer:\s*([ABCD])",
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
    print(matches)
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

