from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

API_URL = "http://127.0.0.1:8000/predict"

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>POWERGRID IT Support Chatbot</title>
<style>
body {
    background:#eef2f7;
    font-family: Arial, sans-serif;
}

.container {
    width: 700px;
    margin: 40px auto;
    background: white;
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(0,0,0,0.1);
    padding: 20px;
}

.header {
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    color: #003366;
    margin-bottom: 20px;
}

.chat {
    max-height: 350px;
    overflow-y: auto;
    margin-bottom: 20px;
}

.bot, .user {
    padding: 10px 15px;
    margin: 10px 0;
    border-radius: 10px;
    width: fit-content;
    max-width: 80%;
}

.bot {
    background: #f1f5fb;
}

.user {
    background: #003366;
    color: white;
    margin-left: auto;
}

input, textarea, button {
    width: 100%;
    padding: 10px;
    margin-top: 10px;
}

button {
    background: #003366;
    color: white;
    border: none;
    cursor: pointer;
    font-size: 16px;
}
</style>

<script>
function validateForm() {
    const phone = document.querySelector('input[name="phone"]').value;
    if (phone.length !== 10) {
        alert("Phone number must be exactly 10 digits.");
        return false;
    }
    return true;
}
</script>

</head>

<body>
<div class="container">
    <div class="header">🤖 POWERGRID IT Support Chatbot</div>

    <div class="chat">
        <div class="bot">
            Hello! Please enter your details and describe your IT issue.
        </div>

        {% if result %}
        <div class="user">
            {{ subject }} <br><br> {{ body }}
        </div>

        <div class="bot">
            <b>Ticket Type:</b> {{ result.ticket_type }} <br>
            <b>Language:</b> {{ result.language }} <br>
            <b>Assigned Team:</b> {{ result.queue }} <br>
            <b>Priority:</b> {{ result.priority }} <br><br>
            <b>Suggested Resolution:</b><br>
            {{ result.solution }}
        </div>
        {% endif %}
    </div>

    <form method="post" onsubmit="return validateForm()">
        <input name="name" placeholder="Employee Name" required>
        <input name="emp_id" placeholder="Employee ID" required>
        <input 
        name="email" 
        placeholder="Email Address" 
        required
        type="email"
        pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$">

        <input 
        name="phone" 
        placeholder="Phone (10-digit)" 
        required
        type="tel"
        pattern="[0-9]{10}"
        maxlength="10"
        oninput="this.value=this.value.replace(/[^0-9]/g,'')">

        <input name="subject" placeholder="Issue Subject" required>
        <textarea name="body" placeholder="Describe your issue" required></textarea>
        <button type="submit">Submit</button>
    </form>
</div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        response = requests.post(API_URL, json={
            "name": request.form["name"],
            "emp_id": request.form["emp_id"],
            "email": request.form["email"],
            "phone": request.form["phone"],
            "subject": request.form["subject"],
            "body": request.form["body"]
        })
        result = response.json()

    return render_template_string(
        HTML,
        result=result,
        subject=request.form.get("subject"),
        body=request.form.get("body"))


if __name__ == "__main__":
    app.run(port=5000, debug=True)
