#run.py

from app import app, db

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='192.168.1.106')