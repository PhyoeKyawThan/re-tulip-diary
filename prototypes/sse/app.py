from flask import Flask, Response, render_template
import time
import json
from random import randint

app = Flask(__name__)

# Function to generate dynamic notifications
def generate_notification():
    notification_type = randint(1, 3)  # Random notification type
    if notification_type == 1:
        return {"type": "info", "message": "New info notification"}
    elif notification_type == 2:
        return {"type": "warning", "message": "Warning: Something happened"}
    else:
        return {"type": "error", "message": "Error: Critical issue occurred"}
@app.route("/")
def index():
    return render_template("index.html")
# SSE endpoint for dynamic notifications
@app.route('/notifications')
def notifications():
    def generate_events():
        while True:
            notification = generate_notification()
            yield "data: {}\n\n".format(json.dumps(notification))
            time.sleep(5)  # Introduce a delay before sending the next notification

    return Response(generate_events(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
