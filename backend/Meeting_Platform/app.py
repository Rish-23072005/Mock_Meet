from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config["SECRET_KEY"] = "AIzaSyDJzrCK38avtgjfEHa1vEbPRFG-43qqojc"
socketio = SocketIO(app)


rooms = {}


@app.route("/mockmeet")
def index():
    return render_template("mockmeet.html")


@app.route("/create_room", methods=["GET"])
def create_room():
    room_id = request.args.get("room")
    username = request.args.get("username")
    if room_id not in rooms:
        rooms[room_id] = {"users": [], "messages": []}
    # Use the correct route to redirect to the room
    return redirect(url_for("meeting_page", room_id=room_id, username=username))


@app.route("/room")
def meeting_page():
    room_id = request.args.get("roomid")
    username = request.args.get("username")
    return render_template("room.html", room_id=room_id, username=username)


@socketio.on("connect")
def connect():
    print("Client connected")


@socketio.on("join_room")
def join_room_handler(data):
    room_id = data["room_id"]
    user_name = data["user_name"]
    join_room(room_id)
    rooms[room_id]["users"].append(user_name)
    emit("user_joined", user_name, room=room_id)


@socketio.on("send_message")
def send_message_handler(data):
    room_id = data["room_id"]
    user_name = data["user_name"]
    message = data["message"]
    rooms[room_id]["messages"].append({"user_name": user_name, "message": message})
    emit("new_message", {"user_name": user_name, "message": message}, room=room_id)


@socketio.on("disconnect")
def disconnect():
    print("Client disconnected")


if __name__ == "__main__":
    socketio.run(app, debug=True)
