from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Gmail credentials
GMAIL_USER = 'yogaastri0902@gmail.com'  # Ganti dengan email Gmail kamu
GMAIL_PASS = 'ensp qvfh kakk xuqw'   # Ganti dengan password Gmail kamu

@app.route('/send/email', methods=['POST'])
def send_email():
    data = request.get_json()

    # Menarik parameter dari request body
    from_email = data.get('from')  # Email pengirim
    to_email = data.get('to')  # Email penerima
    subject = data.get('subject', 'Testing Command')  # Subjek email (default: 'Testing Command')
    content = data.get('content')  # Konten email

    # Validasi input
    if not from_email or not to_email or not content:
        return jsonify({'status': 'error', 'message': 'From, To, and content are required'}), 400

    # Set up the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    body = f"Hello,\n\n{content}\n\nThank You!"
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        
        return jsonify({'status': 'success', 'message': 'Email sent successfully'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Failed to send email', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=3000)
