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
    submit_time = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return 'Thanks for Participating'

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        text_content = request.form['text_content']
        new_text = Final_Texts(content=text_content)

        try:
            db.session.add(new_text)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue with adding your text'

    else:
        return render_template('index.html')

# @app.route('/delete/<int:id>')
# def delete(id):
#     text_to_delete = Final_Texts.query.get_or_404(id)

if __name__ == "__main__":
    app.run(debug=True)

