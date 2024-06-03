from typing import Dict
import json
from echo_quic import EchoQuicConnection, QuicStreamEvent
import pdu

# Function for user registration
async def register_client(conn: EchoQuicConnection, username: str, password: str):
    registration_data = {
        "action": "register",
        "username": username,
        "password": password
    }
    datagram = pdu.Datagram(pdu.MSG_TYPE_DATA, json.dumps(registration_data))
    new_stream_id = conn.new_stream()
    qs = QuicStreamEvent(new_stream_id, datagram.to_bytes(), True)
    await conn.send(qs)
    response: QuicStreamEvent = await conn.receive()
    dgram_resp = pdu.Datagram.from_bytes(response.data)
    print('[cli] Registration response: ', dgram_resp.msg)

# Function for user login
async def login_client(conn: EchoQuicConnection, username: str, password: str):
    login_data = {
        "action": "login",
        "username": username,
        "password": password
    }
    datagram = pdu.Datagram(pdu.MSG_TYPE_DATA, json.dumps(login_data))
    new_stream_id = conn.new_stream()
    qs = QuicStreamEvent(new_stream_id, datagram.to_bytes(), True)
    await conn.send(qs)
    response: QuicStreamEvent = await conn.receive()
    dgram_resp = pdu.Datagram.from_bytes(response.data)
    print('[cli] Login response: ', dgram_resp.msg)
    return dgram_resp.msg.strip() == "Login successful"

# Function for user logout
async def logout_client(conn: EchoQuicConnection, username: str):
    logout_data = {
        "action": "logout",
        "username": username
    }
    datagram = pdu.Datagram(pdu.MSG_TYPE_DATA, json.dumps(logout_data))
    new_stream_id = conn.new_stream()
    qs = QuicStreamEvent(new_stream_id, datagram.to_bytes(), True)
    await conn.send(qs)
    response: QuicStreamEvent = await conn.receive()
    dgram_resp = pdu.Datagram.from_bytes(response.data)
    print('[cli] Logout response: ', dgram_resp.msg)
    return dgram_resp.msg.strip() == "Logout successful"

# Function for client protocol 
async def echo_client_proto(scope: Dict, conn: EchoQuicConnection):
    print('[cli] starting client')
    
    # User registration
    username = input('Enter your username for registration: ')
    password = input('Enter your password for registration: ')
    await register_client(conn, username, password)

    # User login 
    while True:
        username = input('Enter your username for login: ')
        password = input('Enter your password for login: ')
        if await login_client(conn, username, password):
            break
        else:
            print("Login failed. Please try again.")
    
    # Client sending message or choose to logout
    while True:
        action = input('Enter "msg" to send a message or "logout" to logout: ')
        if action == "msg":
            user_message = input('Enter the message to send to the server: ')
            datagram = pdu.Datagram(pdu.MSG_TYPE_DATA, user_message)
            new_stream_id = conn.new_stream()
            qs = QuicStreamEvent(new_stream_id, datagram.to_bytes(), False)
            await conn.send(qs)
            message: QuicStreamEvent = await conn.receive()
            dgram_resp = pdu.Datagram.from_bytes(message.data)
            print('[cli] got message: ', dgram_resp.msg)
            print('[cli] msg as json: ', dgram_resp.to_json())
        elif action == "logout":
            # Handle logout
            print("Logged out successfully.")
            break
        else:
            print("Invalid action. Please enter 'msg' or 'logout'.")
