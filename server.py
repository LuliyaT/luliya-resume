from flask import Flask, render_template, request, redirect, url_for
from smtplib import SMTP
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/redirect')
def redirect_to():
    return render_template("success.html")


@app.route('/contact-me', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return redirect(url_for('redirect_to'))
    return render_template("contact.html")


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message:\n\nName: {name}\nEmail: {email}\nPhone Number: {phone}\nMessage: {message}"
    with SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        from_email = os.getenv("FROM_EMAIL")
        from_email_pass = os.getenv("FROM_EMAIL_PASS")
        to_email = os.getenv("TO_EMAIL")
        connection.login(from_email, from_email_pass)
        connection.sendmail(from_addr=from_email, to_addrs=to_email, msg=email_message)


if __name__ == "__main__":
    app.run(debug=True)
