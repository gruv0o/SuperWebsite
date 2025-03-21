from flask import Flask
app = Flask(__name__, template_folder='templates')



if __name__ == '__main__':
    app.run()
