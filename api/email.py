from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests  # Untuk mengirimkan log ke Discord webhook

app = Flask(__name__)

# Gmail credentials
GMAIL_USER = 'siastri.api@gmail.com'  # Ganti dengan email Gmail kamu
GMAIL_PASS = 'vgqb pcqs hswo yrfs'   # Ganti dengan password Gmail kamu

# Menyimpan API key dan webhook Discord yang sesuai
API_KEYS = {
    'ghost9094': 'https://discord.com/api/webhooks/1353984087156588564/QrThblkHMruq7yt0jZ852SX7Lyc4b9thSpwieETZ-fVn8KSqSSmijuo04NbMz8iDXW3M',  # Ganti dengan webhook URL untuk apikey_1
    'astrianjay': 'https://discord.com/api/webhooks/1353999735467278346/EiwefvJokLoPh0AB9VGMrs9gpSqjgoV_45hpJQGqE6b5ojlRixoIJ4islsvhlf9BB0Zo',  # Ganti dengan webhook URL untuk apikey_2
}

def send_log_to_discord(message, api_key):
    """Fungsi untuk mengirimkan log ke Discord Webhook berdasarkan API Key"""
    webhook_url = API_KEYS.get(api_key)
    
    if not webhook_url:
        print(f"No webhook found for API Key: {api_key}")
        return

    data = {
        "content": message
    }
    try:
        requests.post(webhook_url, json=data)
    except Exception as e:
        print(f"Failed to send log to Discord: {e}")

@app.route('/send/email', methods=['POST'])
def send_email():
    data = request.get_json()

    # Menarik parameter dari request body
    api_key = data.get('api_key')  # API Key untuk memilih webhook
    from_email = data.get('from')  # Email pengirim
    to_email = data.get('to')  # Email penerima
    subject = data.get('subject', 'Testing Command')  # Subjek email (default: 'Testing Command')
    content = data.get('content')  # Konten email

    # Validasi input
    if not api_key or not from_email or not to_email or not content:
        return jsonify({'status': 'error', 'message': 'API key, From, To, and content are required'}), 400

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

        # Kirim log ke Discord setelah email terkirim
        send_log_to_discord(f"Email sent successfully to **{to_email}**", api_key)

        return jsonify({'status': 'success', 'message': 'Email sent successfully'}), 200
    except Exception as e:
        send_log_to_discord(f"Error: Failed to send email. Error: {str(e)}", api_key)
        return jsonify({'status': 'error', 'message': 'Failed to send email', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=3000)
