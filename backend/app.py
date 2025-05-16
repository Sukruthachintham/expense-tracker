from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS so your frontend JS can call the API
@app.route('/')
def home():
    return "Expense Tracker API is running!"
# In-memory expenses list
expenses = [
    
]




@app.route('/expenses', methods=['GET'])
def get_expenses():
    return jsonify(expenses)

@app.route('/add-expense', methods=['POST'])
def add_expense():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data received"}), 400
    # Validate required fields
    if 'amount' not in data or 'category' not in data or 'date' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        amount = float(data['amount'])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount"}), 400

    new_id = max([e['id'] for e in expenses], default=0) + 1
    new_expense = {
        "id": new_id,
        "amount": amount,
        "category": data['category'],
        "date": data['date'],
        "note": data.get('note', '')
    }
    expenses.append(new_expense)
    return jsonify(new_expense), 201

@app.route('/update-expense/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data received"}), 400
    for expense in expenses:
        if expense['id'] == expense_id:
            # Update only provided fields
            if 'amount' in data:
                try:
                    expense['amount'] = float(data['amount'])
                except (ValueError, TypeError):
                    return jsonify({"error": "Invalid amount"}), 400
            if 'category' in data:
                expense['category'] = data['category']
            if 'date' in data:
                expense['date'] = data['date']
            if 'note' in data:
                expense['note'] = data['note']
            return jsonify(expense)
    return jsonify({"error": "Expense not found"}), 404

@app.route('/delete-expense/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    global expenses
    expenses = [e for e in expenses if e['id'] != expense_id]
    return jsonify({"message": "Deleted"}), 200

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # default to 5000 for local testing
    app.run(host='0.0.0.0', port=port)

