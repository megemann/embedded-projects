from flask import Flask, render_template_string, request, redirect, url_for
from Send_CMD import send_cmd
from Remote import Remote, rgb_cmds, picture_cmds

app = Flask(__name__)

# Initialize two Remote instances - one for LED, one for Picture
# GPIO 18 for LED control, GPIO 19 for Picture control
# Start states: LED="power", Picture="off"
led_remote = Remote(gpio=18, instructions=rgb_cmds, start_state="power")
picture_remote = Remote(gpio=19, instructions=picture_cmds, start_state="off")

# HTML template with buttons and color selector
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>LED Remote Control</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 40px; 
            background: #f5f5f5;
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { 
            color: #333; 
            text-align: center;
            margin-bottom: 30px;
        }
        .button-row {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin-bottom: 30px;
        }
        .button { 
            background: #007bff; 
            color: white; 
            padding: 15px 25px; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            font-size: 16px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: background 0.3s;
        }
        .button:hover { background: #0056b3; }
        .power-btn { background: #dc3545; }
        .power-btn:hover { background: #c82333; }
        .bright-btn { background: #28a745; }
        .bright-btn:hover { background: #218838; }
        .dim-btn { background: #ffc107; color: #333; }
        .dim-btn:hover { background: #e0a800; }
        
        .color-section {
            text-align: center;
            margin-top: 30px;
        }
        .color-controls {
            display: flex;
            gap: 15px;
            justify-content: center;
            align-items: center;
            margin-bottom: 20px;
        }
        .color-btn {
            background: #6c757d;
            color: white;
            padding: 15px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
        }
        .color-btn:hover { background: #5a6268; }
        .music-btn {
            background: #17a2b8;
            color: white;
            padding: 15px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: background 0.3s;
        }
        .music-btn:hover { background: #138496; }
        .cycle-btn {
            background: #e83e8c;
            color: white;
            padding: 15px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: background 0.3s;
        }
        .cycle-btn:hover { background: #d91a72; }
        
        .color-wheel {
            position: relative;
            width: 300px;
            height: 300px;
            margin: 20px auto;
            border-radius: 50%;
            background: #f0f0f0;
            border: 3px solid #ddd;
            cursor: pointer;
            transition: transform 0.3s ease;
        }
        .color-wheel:hover {
            transform: scale(1.05);
        }
        .color-wheel::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 60px;
            height: 60px;
            background: white;
            border-radius: 50%;
            transform: translate(-50%, -50%);
            box-shadow: inset 0 0 10px rgba(0,0,0,0.2);
            border: 2px solid #ddd;
        }
        .color-dots {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
        }
        .color-dot {
            position: absolute;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            cursor: pointer;
            pointer-events: auto;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .color-dot:hover {
            transform: scale(1.2);
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        }
        .color-label {
            position: absolute;
            font-size: 8px;
            font-weight: bold;
            color: white;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
            transform: translate(-50%, -50%);
            pointer-events: auto;
            cursor: pointer;
            padding: 1px 3px;
            border-radius: 2px;
            background: rgba(0,0,0,0.5);
            white-space: nowrap;
        }
        .hidden { display: none; }
        
        /* Section styles */
        .control-section {
            margin-bottom: 40px;
        }
        .section-title {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        /* Picture control styles */
        .picture-row {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin-bottom: 20px;
        }
        .timer-btn {
            background: #6f42c1;
            color: white;
            padding: 12px 18px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: background 0.3s;
        }
        .timer-btn:hover { background: #5a32a3; }
        .white-light-btn {
            padding: 12px 18px;
            border: 3px solid white;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            font-weight: bold;
            color: #333;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
        }
        .white-light-btn:hover { 
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        }
        .warm-btn {
            background: #fff8dc; /* Warm yellowish white */
        }
        .neutral-btn {
            background: #ffffff; /* Pure white */
        }
        .cool-btn {
            background: #f0f8ff; /* Cool bright white */
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Remote Control</h1>
        
        <!-- LED Control Section -->
        <div class="control-section">
            <div class="section-title">LED Control</div>
            
            <div class="button-row">
                <a href="/bright_up" class="button bright-btn">
                    +🔅
                </a>
                <a href="/dim_down" class="button dim-btn">
                    -🔅
                </a>
                <a href="/power" class="button power-btn">
                    ⏻
                </a>
            </div>
            
            <div class="color-section">
                <div class="color-controls">
                    <a href="/music1" class="button music-btn">
                        🎵
                    </a>
                    <button class="color-btn" onclick="toggleColorGrid()">
                        🎨
                    </button>
                    <a href="/fade" class="button cycle-btn">
                        🌈
                    </a>
                </div>
                
                <div id="colorWheel" class="color-wheel hidden">
                    <div class="color-dots" id="colorDots">
                        <!-- Color dots will be populated by JavaScript -->
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Picture Control Section -->
        <div class="control-section">
            <div class="section-title">Picture Control</div>
            
            <!-- On/Off Row -->
            <div class="picture-row">
                <a href="/picture_on" class="button bright-btn">
                    💡 On
                </a>
                <a href="/picture_off" class="button power-btn">
                    ⏻ Off
                </a>
            </div>
            
            <!-- Timer Row -->
            <div class="picture-row">
                <a href="/timer_5min" class="timer-btn">
                    ⏰ 5min
                </a>
                <a href="/timer_15min" class="timer-btn">
                    ⏰ 15min
                </a>
                <a href="/timer_30min" class="timer-btn">
                    ⏰ 30min
                </a>
            </div>
            
            <!-- Brightness Row -->
            <div class="picture-row">
                <a href="/picture_bright_up" class="button bright-btn">
                    +🔅
                </a>
                <a href="/picture_bright_down" class="button dim-btn">
                    -🔅
                </a>
            </div>
            
            <!-- White Light Temperature Row -->
            <div class="picture-row">
                <a href="/warm" class="white-light-btn warm-btn">
                    Warm
                </a>
                <a href="/neutral" class="white-light-btn neutral-btn">
                    Neutral
                </a>
                <a href="/cool" class="white-light-btn cool-btn">
                    Cool
                </a>
            </div>
        </div>
    </div>

    <script>
        const colors = {{ colors|tojson }};
        
        function toggleColorGrid() {
            const wheel = document.getElementById('colorWheel');
            wheel.classList.toggle('hidden');
            
            if (!wheel.classList.contains('hidden') && document.getElementById('colorDots').children.length === 0) {
                populateColorWheel();
            }
        }
        
        function populateColorWheel() {
            const dotsContainer = document.getElementById('colorDots');
            dotsContainer.innerHTML = '';
            
            const colorNames = Object.keys(colors);
            const angleStep = 360 / colorNames.length;
            
            colorNames.forEach((colorName, index) => {
                const angle = index * angleStep;
                
                // Create color dot
                const dot = document.createElement('div');
                dot.className = 'color-dot';
                dot.style.backgroundColor = getColorHex(colorName);
                dot.style.left = '50%';
                dot.style.top = '50%';
                
                // Position dots around the circle
                const radius = 120; // Distance from center
                const radians = (angle - 90) * Math.PI / 180; // Start from top
                const x = Math.cos(radians) * radius;
                const y = Math.sin(radians) * radius;
                
                dot.style.transform = `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`;
                dot.onclick = (e) => {
                    e.stopPropagation();
                    selectColor(colorName);
                };
                
                // Add tooltip with color name
                dot.title = colorName;
                
                dotsContainer.appendChild(dot);
            });
        }
        
        function selectColor(colorName) {
            window.location.href = `/color/${encodeURIComponent(colorName)}`;
        }
        
        function getColorHex(colorName) {
            const colorMap = {
                'white': '#ffffff',
                'blue': '#0000ff',
                'green': '#00ff00',
                'red': '#ff0000',
                'orange': '#ffa500',
                'light green': '#90ee90',
                'mid-blue': '#4169e1',
                'red-orange': '#ff4500',
                'blue-green': '#008b8b',
                'blue-purple': '#8a2be2',
                'green-yellow': '#adff2f',
                'aquamarine': '#7fffd4',
                'light-purple': '#dda0dd',
                'yellow': '#ffff00',
                'green-blue': '#00ced1',
                'purple': '#800080'
            };
            return colorMap[colorName] || '#666666';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, colors=rgb_cmds, picture_commands=picture_cmds)

@app.route('/power')
def power():
    try:
        led_remote.change_state("power")
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/bright_up')
def bright_up():
    try:
        led_remote.change_state("bright up")
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/dim_down')
def dim_down():
    try:
        led_remote.change_state("bright down")
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/color/<color_name>')
def set_color(color_name):
    try:
        if color_name in rgb_cmds:
            led_remote.change_state(color_name)
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/music1')
def music1():
    try:
        led_remote.change_state("music1")
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/fade')
def fade():
    try:
        led_remote.change_state("fade")
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {e}", 500

# Picture control routes
@app.route('/picture_on')
def picture_on():
    try:
        picture_remote.change_state("static")
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/picture_off')
def picture_off():
    try:
        picture_remote.change_state("off")
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/timer_5min')
def timer_5min():
    try:
        picture_remote.change_state("5-min")
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/timer_15min')
def timer_15min():
    try:
        picture_remote.change_state("15-min")
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/timer_30min')
def timer_30min():
    try:
        picture_remote.change_state("30-min")
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/picture_bright_up')
def picture_bright_up():
    try:
        picture_remote.change_state("brighter")
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/picture_bright_down')
def picture_bright_down():
    try:
        picture_remote.change_state("darker")
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/warm')
def warm():
    try:
        picture_remote.change_state("warm")
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/neutral')
def neutral():
    try:
        picture_remote.change_state("neutral")
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/cool')
def cool():
    try:
        picture_remote.change_state("darker")
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == '__main__':
    print("Starting LED Remote Web Interface...")
    print("Access it at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)