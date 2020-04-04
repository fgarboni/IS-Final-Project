from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import tensorflow as tf
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer


def activate_model():
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    # add the EOS token as PAD token to avoid warnings
    model = TFGPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)
    return tokenizer, model
    # encode context the generation is conditioned on


def predict(words, num_pred, tokenizer, model):
    word_amount = len(words.split())
    predicted_words = word_amount+num_pred
    input_ids = tokenizer.encode(words, return_tensors='tf')
    # generate text until the output length (which includes the context length) reaches 50
    greedy_output = model.generate(input_ids, max_length=predicted_words)
    complete_sentence = tokenizer.decode(greedy_output[0], skip_special_tokens=True)
    predicted_part = complete_sentence.replace(words, '')
    return predicted_part


token, model_test = activate_model()


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


@app.route('/predict', methods=['POST'])
def process():
    text = request.form['name']
    if text:
        new_text = predict(text, 1, token, model_test)
        return jsonify({'name': new_text})

    return jsonify({'error': 'Missing data!'})


@app.route('/admin', methods=['POST', 'GET'])
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

