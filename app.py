from flask import Flask, render_template, redirect, url_for,request,Response
import threading
from bot import open_browser
from backend import get_ballance,buy,sell
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time,datetime,random,threading,datetime,requests,json
from backend import trade_executor
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from flask import Response, stream_with_context

# from flask_socketio import SocketIO
app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins="*")
bot_thread = None



# app.secret_key = "cok_gizli_key"

# Basit user database
USERS = {"admin": "secret123"}

# Login control decorator
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login_form'))
        return f(*args, **kwargs)
    return decorated

# Form based login
@app.route("/login_form", methods=["GET", "POST"])
def login_form():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if USERS.get(username) == password:
            session['username'] = username
            return redirect(url_for('panel'))
        else:
            flash("Username or password is incorrect!")
    return render_template("login.html")

# Form based register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username in USERS:
            flash("This username is taken!")
        else:
            USERS[username] = password
            flash("Registration successful! You can log in.")
            return redirect(url_for('login_form'))
    return render_template("register.html")

# API login endpoint (JSON)
@app.route("/login", methods=["POST"])
def login_api():
    creds = request.get_json()
    username = creds.get("username")
    password = creds.get("password")
    if USERS.get(username) == password:
        session['username'] = username  # Otomatik session
        return jsonify({"status": "success", "message": "Automatic login done"})
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

# Panel sayfası
@app.route("/")
@login_required
def panel():
    return render_template("panel.html", username=session['username'])
# Dummy endpoints



# @app.route("/")
# def index():
#     return render_template("login.html")

@app.route("/start")
@login_required
def start():
    global bot_thread
    if open_browser.running:  # 
        return render_template("start.html", message="Bot has already started .")
    
    bot_thread = threading.Thread(target=open_browser.run)  # 
    bot_thread.start()
    return render_template("start.html", message="Bot started.")

@app.route("/stop")
@login_required
def stop():
    if open_browser.running:
        open_browser.stop()  # 
        return render_template("stop.html", message="Bot stoped.")
    return render_template("stop.html", message="The bot has already stoppedr.")
from flask import jsonify

@app.route("/get_balance")
@login_required
def get_balance():
    try:
        balance = get_ballance.get_bl()  # Backend 
        return jsonify({"status": "success", "balance": balance})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/market")
@login_required
def market():
    if hasattr(open_browser, "running") and open_browser.running:
        msg = "You are ready for market transactions."
    else:
        msg = "Please start the bot first (/start)."

    return render_template("market.html", message=msg)



@app.route("/trade", methods=["POST"])
@login_required
def trade():
    try:
        pair = request.json.get("pair")
        action = request.json.get("action")
        
        if action == "buy":
            result = buy.run_buy(pair)
        elif action == "sell":
            result = sell.run_sell(pair)
        else:

            return jsonify({"status": "error", "message": "Invalid action"})
        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    

@app.route("/execute_trade", methods=["POST"])
@login_required
def execute_trade():
    try:
        pair = request.json.get("pair")
        action = request.json.get("action")
        amount = request.json.get("amount")
        #market_data = trade_executor.search()
        if action == "buy":
            result = trade_executor.execute_buy(pair, amount)
            
        elif action == "sell":
            result = trade_executor.execute_sell(pair, amount)
            
        else:
            return jsonify({"status": "error", "message": "Invalid action"})

        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
    
@app.route("/get_market_data", methods=["GET"])
@login_required
def get_market_data():
    try:
        market_data = trade_executor.search()
        return jsonify({"status": "success", "market_data": market_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/get_close_open", methods=["GET"])
@login_required
def get_close_open():
    try:
        market_data = trade_executor.search()
        return jsonify({"status": "success", "market_data": market_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})




# --- Mock data ---

_trade_history = []
_trade_lock = threading.Lock()

# --- Endpoints ---

@app.route("/charts", methods=["POST"])
def start_chart():
    data = request.get_json()
    identifier = data.get("identifier", f"id-{random.randint(1,1000)}")
    # Mock response:
    response = {
        "message": f"Chart {identifier} started",
        "identifier": identifier,
        "running": True
    }
    return jsonify(response), 201


@app.route("/charts/<identifier>/status", methods=["GET"])
def chart_status(identifier):
    # Mock chart status
    i=0
    for i in range(3):
        try:
            data=trade_executor.getcloseopen()
            if data.get("s") != "ok" or not data.get("c"):
                print("No data could be received, possibly the interval is too short or the bar has not formed yet")
                return None
            
            ts = data["t"][-1]  #  timestamp
            nxt_ts=int(ts)+60
            # Milisaniyeyi to second
            nxt_ts=int(nxt_ts)/1000
            ts_seconds = int(ts) / 1000  

            # UTC time
            dt_nxt_utc=datetime.datetime.utcfromtimestamp(nxt_ts)
            dt_utc = datetime.datetime.utcfromtimestamp(ts_seconds)

            
           

            print("UTC:", dt_utc.strftime("%Y-%m-%d %H:%M:%S"))
            break
        except:
            print("close and open price not found")
        time.sleep(1)
        i+=1
        
    # print(data)
    
    response = {
        "running": True,
        "opens_seen": data["o"][-1],
        "closes_seen": data["c"][-1],
        "last_event_ts": dt_utc,
        "chart_url": "https://www.tradingview.com/chart/...",
        "interval": "1m",
        "next_refresh_at": dt_nxt_utc,
        "refresh_enabled": True
    }
    return jsonify(response)


@app.route("/charts/<identifier>/events", methods=["GET"])
def chart_events(identifier):
    # Mock SSE-like event data (JSON list)
    events = [
        {"kind": "open", "trade": {"id": 1, "entry_type": "long", "entry_signal": "buy", "entry_price": 2000, "entry_time": int(time.time())}},
        {"kind": "close", "trade": {"id": 1, "exit_price": 2020, "exit_time": int(time.time())}},
        {"kind": "alive", "activated_at": int(time.time()), "chart": identifier}
    ]
    return jsonify(events)


@app.route("/charts/<identifier>/closed/events", methods=["GET"])
def chart_closed_events(identifier):
    events = [
        {"kind": "close", "trade": {"id": 1, "exit_price": 2020, "exit_time": int(time.time())}}
    ]
    return jsonify(events)


@app.route("/debug/executor", methods=["GET"])
def debug_executor():
    # Mock webhook buffer
    data = {
        "count": 2,
        "events": [
            {"kind": "dead", "stopped_at": int(time.time())},
            {"kind": "alive", "activated_at": int(time.time())}
        ]
    }
    return jsonify(data)


@app.route("/charts/<identifier>", methods=["DELETE"])
def stop_chart(identifier):
    # Mock stop chart
    return jsonify({"message": f"Chart {identifier} stopped"})



### end point fe
# Global dictionary chart_id -> events
chart_events_buffer = {}

def generate_event(identifier, kind, trade=None, raw=None):
    """Event payload generator, Event Payloads standardına uygun"""
    event = {
        "identifier": identifier,
        "kind": kind,
        "chart": {
            "url": f"https://www.tradingview.com/chart/{identifier}",
            "interval": "1m"
        }
    }
    if trade:
        event["trade"] = trade
    if raw:
        event["raw"] = raw
    if kind == "alive":
        event["activated_at"] = datetime.datetime.utcnow().isoformat()
    if kind == "dead":
        event["stopped_at"] = datetime.datetime.utcnow().isoformat()
    return event

def push_event(identifier, kind, trade=None, raw=None, executor_url=None):
    """Add the created event to the buffer and send it to the webhook"""
    event = generate_event(identifier, kind, trade, raw)
    
    # SSE için buffer
    if identifier not in chart_events_buffer:
        chart_events_buffer[identifier] = []
    chart_events_buffer[identifier].append(event)
    
    # Eğer executor_url verilmişse POST yap
    if executor_url:
        try:
            requests.post(executor_url, json=event)
        except Exception as e:
            print(f"Executor'a didint send: {e}")
    
    return event

@app.route("/charts/<identifier>/events_stream")
def events_stream(identifier):
    def event_stream():
        last_index = 0
        while True:
            events = chart_events_buffer.get(identifier, [])
            while last_index < len(events):
                ev = events[last_index]
                yield f"data: {json.dumps(ev)}\n\n"
                last_index += 1
            time.sleep(1)
    return Response(stream_with_context(event_stream()), mimetype="text/event-stream")



# if __name__ == "__main__":
#     app.run(debug=True,host="0.0.0.0", port=5000)
if __name__ == "__main__":
    app.run(debug=True)
