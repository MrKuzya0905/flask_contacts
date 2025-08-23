import random

from flask import Flask, render_template
from faker import Faker


app = Flask(__name__)
fake = Faker("uk_UA")

data = []

@app.get('/')
def index():
    context = dict(
        title='Home Page', 
          title_h1='Welcome to the Home Page', 
          content='This is the main page of our Flask application.'
          )
    return render_template('index.html',**context)

@app.get('/context/')
def test_context():
    numbers = [random.randint(1, 10) for _ in range(10)]
    return render_template('context.html', numbers=numbers)

if __name__ == '__main__':
    app.run(debug=True)