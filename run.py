#run.py

from app import app, db

if __name__ == '__main__':
    # Replace 'your_server_ip' with your actual server's IP address
    server_ip = '192.168.1.106'  # Example IP address
    
    # Run the Flask app with debug mode enabled
    app.run(host=server_ip, port=5000, debug=True)
