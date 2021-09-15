from website import create_app

# This if statement is designed block the creation of the flask app
# The app will only run if the app.py is the main file that is executed
# __name__ is a global variable that will be set to "__main__" if this file is the first to run in the app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
