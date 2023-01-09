from flask_app import app
from flask_app.controllers import users, songs

if __name__ == ('__main__'):
    app.run(debug=False, host = '0.0.0.0', port= 5000)