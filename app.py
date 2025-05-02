from flask import Flask, request, jsonify, render_template
from models import db, Record
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/records', methods=['POST'])
def add_record():
    data = request.get_json()
    new_record = Record(content=data['content'])
    db.session.add(new_record)
    db.session.commit()
    return jsonify({'id': new_record.id, 'content': new_record.content}), 201

@app.route('/records/<int:id>', methods=['GET'])
def get_record(id):
    record = Record.query.get_or_404(id)
    return jsonify({'id': record.id, 'content': record.content})

@app.route('/records/view/<int:id>', methods=['GET'])
def view_record(id):
    record = Record.query.get_or_404(id)
    return render_template('record.html', record=record)
