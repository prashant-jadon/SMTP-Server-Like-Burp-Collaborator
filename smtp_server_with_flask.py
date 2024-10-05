import asyncio
from aiosmtpd.controller import Controller
from flask import Flask, jsonify, render_template
from threading import Thread

# Initialize Flask app
app = Flask(__name__, template_folder='templates')

# Global list to store captured emails
captured_emails = []

# Custom SMTP handler
class CustomSMTPHandler:
    async def handle_DATA(self, server, session, envelope):
        email = {
            "peer": session.peer,
            "from": envelope.mail_from,
            "to": envelope.rcpt_tos,
            "data": envelope.content.decode('utf8', errors='replace')
        }
        print(f"Captured email from {envelope.mail_from} to {envelope.rcpt_tos}")
        captured_emails.append(email)  # Append the captured email to the global list
        return '250 Message accepted for delivery'

# Flask route to serve the main HTML page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Flask route to return captured emails in JSON format
@app.route("/emails", methods=["GET"])
def get_emails():
    return jsonify(captured_emails)

# Function to run the Flask web app
def start_flask_app():
    app.run(host="0.0.0.0", port=1000)

# Function to run the SMTP server
def start_smtp_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    handler = CustomSMTPHandler()
    controller = Controller(handler, hostname='0.0.0.0', port=1025)
    controller.start()
    print("SMTP Collaborator server started on port 1025...")
    loop.run_forever()

# Main function to run both SMTP server and Flask app concurrently
if __name__ == "__main__":
    smtp_thread = Thread(target=start_smtp_server)
    flask_thread = Thread(target=start_flask_app)
    
    smtp_thread.start()
    flask_thread.start()
    
    smtp_thread.join()
    flask_thread.join()
