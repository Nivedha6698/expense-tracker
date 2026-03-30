from flask import Blueprint, request, jsonify, render_template
from .models import db, User, Expense
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

main = Blueprint('main', __name__)

# ---------------- AUTH ---------------- #

@main.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Invalid input"}), 400

    # Check if user already exists
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    user = User(
        username=data['username'],
        password=generate_password_hash(data['password'])  # ✅ secure password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created"}), 201


@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Invalid input"}), 400

    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password, data['password']):
        token = create_access_token(identity=str(user.id))  # ✅ FIXED
        return jsonify(access_token=token)

    return jsonify({"message": "Invalid credentials"}), 401


# ---------------- EXPENSE ---------------- #

@main.route('/expenses', methods=['POST'])
@jwt_required()
def add_expense():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()

        if not data or 'amount' not in data:
            return jsonify({"error": "Invalid data"}), 400

        expense = Expense(
            amount=float(data['amount']),  # ✅ ensure float
            category=data.get('category'),
            notes=data.get('notes'),
            user_id=user_id
        )

        db.session.add(expense)
        db.session.commit()

        return jsonify({"message": "Expense added"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    user_id = int(get_jwt_identity())
    category = request.args.get('category')

    query = Expense.query.filter_by(user_id=user_id)

    if category:
        query = query.filter_by(category=category)

    expenses = query.all()

    result = []
    for e in expenses:
        result.append({
            "id": e.id,
            "amount": e.amount,
            "category": e.category,
            "notes": e.note
            "created_at": e.created_at.strftime("%Y-%m-%d %H:%M")  
        })

    return jsonify(result)


@main.route('/expenses/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_expense(id):
    user_id = int(get_jwt_identity())

    # ✅ FIX: user can delete only their expense
    expense = Expense.query.filter_by(id=id, user_id=user_id).first()

    if not expense:
        return jsonify({"message": "Not found"}), 404

    db.session.delete(expense)
    db.session.commit()

    return jsonify({"message": "Deleted"})

@main.route('/expenses/<int:id>', methods=['PUT'])
@jwt_required()
def update_expense(id):
    user_id = int(get_jwt_identity())
    data = request.get_json()

    expense = Expense.query.filter_by(id=id, user_id=user_id).first()

    if not expense:
        return jsonify({"message": "Not found"}), 404

    expense.amount = float(data.get('amount', expense.amount))
    expense.category = data.get('category', expense.category)
    expense.description = data.get('description', expense.description)

    db.session.commit()

    return jsonify({"message": "Expense updated"})



@main.route('/expenses/summary', methods=['GET'])
@jwt_required()
def expense_summary():
    user_id = int(get_jwt_identity())

    summary = db.session.query(
        Expense.category,
        func.sum(Expense.amount)
    ).filter_by(user_id=user_id).group_by(Expense.category).all()

    result = {category: total for category, total in summary}

    return jsonify(result)

import csv
from flask import Response

@main.route('/expenses/export', methods=['GET'])
@jwt_required()
def export_csv():
    user_id = int(get_jwt_identity())

    expenses = Expense.query.filter_by(user_id=user_id).all()

    def generate():
        yield 'Amount,Category,Description,Date\n'
        for e in expenses:
            yield f"{e.amount},{e.category},{e.description},{e.date}\n"

    return Response(generate(), mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=expenses.csv"})


# ---------------- PAGES ---------------- #

@main.route('/')
def home():
    return render_template('login.html')


@main.route('/signup-page')
def signup_page():
    return render_template('signup.html')


@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')