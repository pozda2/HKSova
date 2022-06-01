from hksova.factory import create_flask_app

if __name__ == "__main__":  
    host="::"
    host="0.0.0.0"
    flask_app=create_flask_app()
    flask_app.run(host)
