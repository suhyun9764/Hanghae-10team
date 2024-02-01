from flask import Flask, render_template, request,redirect,url_for
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

class Member(db.Model):
    member_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    pwd = db.Column(db.String, nullable=False)
    memos = relationship('Memo', backref='member', lazy=True)
    todo_lists = relationship('ToDoList', backref='member', lazy=True)
    address_books = relationship('AddressBook', backref='member', lazy=True)
    diaries = relationship('Diary', backref='member', lazy=True)

class Memo(db.Model):
    memo_id = db.Column(db.Integer, primary_key=True)
    main_text = db.Column(db.Text, nullable=False)
    edit_time = db.Column(db.String, default=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'), nullable=False)
    member_id = db.Column(db.String, db.ForeignKey('member.member_id'), nullable=False)

class ToDoList(db.Model):
    todolist_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    deadline = db.Column(db.Date, nullable=True)
    is_complete = db.Column(db.Boolean, nullable=False, default=False)
    member_id = db.Column(db.String, db.ForeignKey('member.member_id'), nullable=False)

class AddressBook(db.Model):
    address_id = db.Column(db.Integer, primary_key=True)
    team_member_name = db.Column(db.String, nullable=False)
    project = db.Column(db.String, nullable=False)
    realization = db.Column(db.Text, nullable=True)
    member_id = db.Column(db.String, db.ForeignKey('member.member_id'), nullable=False)

class Diary(db.Model):
    diary_id = db.Column(db.Integer, primary_key=True)
    main_text = db.Column(db.Text, nullable=False)
    edit_time = db.Column(db.String, default=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    member_id = db.Column(db.String, db.ForeignKey('member.member_id'), nullable=False)

@app.route("/memo/",methods=["GET"])
def memo():
    print("memo")
    member_id_to_query = 'suhyun9764'
    memo_data = Memo.query.filter_by(member_id=member_id_to_query).order_by(Memo.edit_time.desc()).all()

    if memo_data:
        memo_per_page = 6
        page = request.args.get('page', 1, type=int)
        start_index = (page - 1) * memo_per_page
        end_index = start_index + memo_per_page

        current_page_memo = memo_data[start_index:end_index]

        total_memos = len(memo_data)
        total_pages = (total_memos + memo_per_page - 1) // memo_per_page

        return render_template('memo.html', data=current_page_memo, page_num=total_pages)
    else:
        return "No memo data found for the given member ID."
    

@app.route("/memo/", methods=["POST"])
def handle_memo():
    if request.form.get("_method") == "POST":
        return create_memo()
    elif request.form.get("_method") == "PUT":
        return update_memo()
    else:
        return "Invalid request"

def create_memo():
    print("create")
    text = request.form.get("content")
    edit_time = request.form.get("current_time")
    memo_data = Memo(main_text=text, edit_time=edit_time, member_id='suhyun9764')
    db.session.add(memo_data)
    db.session.commit()
    return redirect(url_for('memo'))

def update_memo():
    print("update")
    text_receive = request.form.get("content")
    edit_time_receive = request.form.get("current_time")
    memo_id_receive = request.form.get("memo_id")
    memo_data = Memo.query.filter_by(memo_id=memo_id_receive).first()
    memo_data.main_text = text_receive
    memo_data.edit_time = edit_time_receive
    db.session.add(memo_data)

    db.session.commit()  
    return redirect(url_for('memo'))

@app.route("/memo/delete/<id>")
def delete_memo(id):
    print("delete")
    print(id)
    memo = Memo.query.filter_by(memo_id=id).first()
    if memo:
        db.session.delete(memo)
        db.session.commit()
        return redirect(url_for('memo'))
    else:
        return 'Memo not found', 404




if __name__ == '__main__':
    app.run()
