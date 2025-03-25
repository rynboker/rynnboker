from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests  # Untuk mengirimkan log ke Discord webhook

app = Flask(__name__)

# Gmail credentials
GMAIL_USER = 'yogaastri0902@gmail.com'  # Ganti dengan email Gmail kamu
GMAIL_PASS = 'ensp qvfh kakk xuqw'   # Ganti dengan password Gmail kamu

# URL webhook Discord untuk logging
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1353984087156588564/QrThblkHMruq7yt0jZ852SX7Lyc4b9thSpwieETZ-fVn8KSqSSmijuo04NbMz8iDXW3M'  # Ganti dengan webhook URL kamu

def send_log_to_discord(message):
    """Fungsi untuk mengirimkan log ke Discord Webhook"""
    data = {
        "content": message
    }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=data)
    except Exception as e:
        print(f"Failed to send log to Discord: {e}")

@app.route('/send/email', methods=['POST'])
def send_email():
    data = request.get_json()

    # Menarik parameter dari request body
    to_email = data.get('to')  # Email penerima
    subject = data.get('subject', 'Testing Command')  # Subjek email (default: 'Testing Command')
    content = data.get('content')  # Konten email

    # Validasi input
    if not from_email or not to_email or not content:
        send_log_to_discord(f"Error: Missing parameters (To or Content).")
        return jsonify({'status': 'error', 'message': 'To and content are required'}), 400

    # Set up the email
    msg = MIMEMultipart()
    msg['To'] = to_email
    msg['Subject'] = subject

    body = f"Hello,\n\n{content}\n\nThank You!"
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(msg['To'], msg.as_string())
        server.quit()

        # Kirim log ke Discord setelah email terkirim
        send_log_to_discord(f"Email sent successfully to **{to_email}** with subject **{subject}**.\n```Content : {content}```")

        return jsonify({'status': 'success', 'message': 'Email sent successfully'}), 200
    except Exception as e:
        send_log_to_discord(f"Error: Failed to send email. Error: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Failed to send email', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=3000)
