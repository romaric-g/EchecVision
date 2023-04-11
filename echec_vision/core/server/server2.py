import socketio

sio = socketio.Server(async_mode='eventlet')


@sio.on("connect")
def connected():
    """event listener when client connects to the server"""
    # print(request.sid)
    print("client has connected")
    sio.emit("connect", {"data": f"id: is connected"})


@sio.on('data')
def handle_message(data):
    """event listener when client types a message"""
    print("data from the front end: ", str(data))
    sio.emit("data", {'data': data, 'id': "request.sid"}, broadcast=True)


@sio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    sio.emit("disconnect", f"user request.sid disconnected", broadcast=True)


if __name__ == '__main__':
    app = socketio.WSGIApp(sio)
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('', 5001)), app)
