from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Final_Texts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_text = db.Column(db.Text, nullable=False)
    num_of_offers = db.Column(db.Integer)
    num_of_accepts = db.Column(db.Integer)
    gadget = db.Column(db.String(10))
    submit_time = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Text %r>' % self.id

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        text_content = request.form['text_content']
        new_text = Final_Texts(full_text=text_content)

        try:
            db.session.add(new_text)
            db.session.commit()
            return 'Thanks For Participating'
        except:
            return 'There was an issue with adding your text'

    else:
        return render_template('index.html')

@app.route('/admin', methods=['POST','GET'])
def admin_index():
    if request.method == 'POST':
        text_content = request.form['text_content']
        new_text = Final_Texts(full_text=text_content)
    else:
        texts = Final_Texts.query.order_by(Final_Texts.id).all()
        return render_template('admin.html',texts=texts)

def get_text(id):
    if request.method == 'POST':
        text = Final_Texts.query.filter_by(id=id).first()
        return f"Text for id {Final_Texts.id} is: {text.full_text}"

@app.route('/admin/delete/<int:id>')
def delete(id):
     text_to_delete = Final_Texts.query.get_or_404(id)
     try:
         db.session.delete(text_to_delete)
         db.session.commit()
         return redirect('/admin')
     except:
         return 'There seems to be a problem deleting'

if __name__ == "__main__":
    app.run(debug=True)

