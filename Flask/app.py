from flask import Flask

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/doctor')
def doctor():
    return "Doctor Page"

@app.route('/client')
def patient():
    return "client Page"

if __name__ == "__main__":
    #db.create_all()
    app.run(debug=True)