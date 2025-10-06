from flask import Flask, render_template_string, request, redirect, url_for
from LED_IR_Control.Send_CMD import send_cmd

app = Flask(__name__)

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>LED Remote Control</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 600px; margin: 0 auto; }
        h1 { color: #333; }
        .button { 
            background: #007bff; 
            color: white; 
            padding: 20px 40px; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer; 
            font-size: 18px;
        }
        .button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>LED Remote Control</h1>
        
        <a href="/power" class="button">Power</a>
        
        <div style="margin-top: 30px;">
            <p><em>Simple web interface for LED control</em></p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/power')
def power():
    try:
        send_cmd(0x40)  # Power command
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == '__main__':
    print("Starting LED Remote Web Interface...")
    print("Access it at: http://10.25.8.14:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
