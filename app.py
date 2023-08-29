from flask import Flask
from views import views

# Initializing flask app

app = Flask(__name__)
# Registering blueprint views
app.register_blueprint(views,url_prefix='/')
# Secret Key
app.secret_key = 'qwertyuiopasdfghjklzxcvbnm'



if __name__ == '__main__':
    app.run(debug=True)