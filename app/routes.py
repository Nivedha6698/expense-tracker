from flask import Blueprint, request, jsonify, render_template, current_app
from .models import db, User, Expense
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from app.utils.s3_utils import upload_csv_to_s3, generate_download_url

main = Blueprint('main', __name__)

# ---------------- AUTH ---------------- #

@main.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()

        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Invalid input"}), 400

        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "User already exists"}), 400

        user = User(
            username=data['username'],
            password=generate_password_hash(data['password'])
        )

        db.session.add(user)
        db.session.commit()

        current_app.logger.info(f"User created: {data['username']}")
        return jsonify({"message": "User created"}), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Signup error: {str(e)}")
        return jsonify({"error": "Signup failed"}), 500


@main.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()

        if user and check_password_hash(user.password, data['password']):
            token = create_access_token(identity=str(user.id))
            current_app.logger.info(f"User logged in: {data['username']}")
            return jsonify(access_token=token)

        return jsonify({"message": "Invalid credentials"}), 401

    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return jsonify({"error": "Login failed"}), 500


# ---------------- EXPENSE ---------------- #

@main.route('/expenses', methods=['POST'])
@jwt_required()
def add_expense():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()

        expense = Expense(
            amount=float(data['amount']),
            category=data.get('category'),
            notes=data.get('notes'),
            user_id=user_id
        )

        db.session.add(expense)
        db.session.commit()

        current_app.logger.info(f"Expense added for user {user_id}")
        return jsonify({"message": "Expense added"}), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Add expense error: {str(e)}")
        return jsonify({"error": "Failed to add expense"}), 500


@main.route('/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    try:
        user_id = int(get_jwt_identity())
        expenses = Expense.query.filter_by(user_id=user_id).all()

        result = []
        for e in expenses:
            result.append({
                "id": e.id,
                "amount": e.amount,
                "category": e.category,
                "notes": e.notes,
                "created_at": e.created_at.strftime("%Y-%m-%d %H:%M")
            })

        return jsonify(result)

    except Exception as e:
        current_app.logger.error(f"Fetch expenses error: {str(e)}")
        return jsonify({"error": "Failed to fetch expenses"}), 500


@main.route('/expenses/<int:id>', methods=['PUT'])
@jwt_required()
def update_expense(id):
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()

        expense = Expense.query.filter_by(id=id, user_id=user_id).first()

        if not expense:
            return jsonify({"message": "Not found"}), 404

        expense.amount = float(data.get('amount', expense.amount))
        expense.category = data.get('category', expense.category)
        expense.notes = data.get('notes', expense.notes)

        db.session.commit()

        current_app.logger.info(f"Expense updated: {id}")
        return jsonify({"message": "Updated"})

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update error: {str(e)}")
        return jsonify({"error": "Update failed"}), 500


@main.route('/expenses/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_expense(id):
    try:
        user_id = int(get_jwt_identity())

        expense = Expense.query.filter_by(id=id, user_id=user_id).first()

        if not expense:
            return jsonify({"message": "Not found"}), 404

        db.session.delete(expense)
        db.session.commit()

        current_app.logger.info(f"Expense deleted: {id}")
        return jsonify({"message": "Deleted"})

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Delete error: {str(e)}")
        return jsonify({"error": "Delete failed"}), 500


# ---------------- SUMMARY ---------------- #

@main.route('/expenses/summary', methods=['GET'])
@jwt_required()
def summary():
    try:
        user_id = int(get_jwt_identity())

        data = db.session.query(
            Expense.category,
            func.sum(Expense.amount)
        ).filter_by(user_id=user_id).group_by(Expense.category).all()

        return jsonify({c: float(a) for c, a in data})

    except Exception as e:
        current_app.logger.error(f"Summary error: {str(e)}")
        return jsonify({"error": "Summary failed"}), 500


# ---------------- EXPORT ---------------- #

@main.route('/expenses/export', methods=['GET'])
@jwt_required()
def export_csv():
    try:
        user_id = int(get_jwt_identity())
        expenses = Expense.query.filter_by(user_id=user_id).all()

        csv_data = 'Amount,Category,Notes,Date\n'
        for e in expenses:
            csv_data += f"{e.amount},{e.category},{e.notes},{e.created_at}\n"

        file_key = upload_csv_to_s3(csv_data, user_id)
        download_url = generate_download_url(file_key)

        current_app.logger.info(f"CSV exported for user {user_id}")

        return jsonify({
            "message": "File uploaded to S3",
            "download_url": download_url
        })

    except Exception as e:
        current_app.logger.error(f"Export error: {str(e)}")
        return jsonify({"error": "Export failed"}), 500


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