from flask import Flask, request, send_file, redirect
import datetime
import os

app = Flask(__name__)

TRACK_IMAGE_PATH = "track.png"

def log_event(log_file, event_type, email_id, remote_addr):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{event_type} by {email_id}: {remote_addr} - {timestamp}\n"
    with open(log_file, "a") as f:
        f.write(log_entry)

#  Create the log files if they don't exist
if not os.path.exists("email_opens.log"):
    open("email_opens.log", 'a').close()

if not os.path.exists("link_clicks.log"):
    open("link_clicks.log", 'a').close()


@app.route('/track_email/<email_id>')
def track_email(email_id):
    log_event("email_opens.log", "Email opened", email_id, request.remote_addr)
    return send_file(TRACK_IMAGE_PATH, mimetype="image/png")

@app.route('/track_link/<email_id>')
def track_link(email_id):
    log_event("link_clicks.log", "Link clicked", email_id, request.remote_addr)
    destination_url = os.environ.get("DESTINATION_URL", "https://yourfinaldestination.com")
    return redirect(destination_url)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")