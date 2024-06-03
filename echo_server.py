import asyncio
from typing import Dict
import json
from echo_quic import EchoQuicConnection, QuicStreamEvent
import pdu

# Stores connected clients
clients = {}

# Stores registered users
registered_users = {}

# Function for server protocol
async def echo_server_proto(scope: Dict, conn: EchoQuicConnection):
    while True:
        # Receive a message from the client
        message: QuicStreamEvent = await conn.receive()
        dgram_in = pdu.Datagram.from_bytes(message.data)
        print("[svr] received message:", dgram_in.msg)
        
        # Attempt to parse the received message as JSON
        try:
            data = json.loads(dgram_in.msg)
        except json.JSONDecodeError:
            print("")
            continue
        
        # Extract the action from the parsed JSON data
        action = data.get("action")
        
        # Handle user registration
        if action == "register":
            username = data.get("username")
            password = data.get("password")
            if username in registered_users:
                response = "Username already taken."
            else:
                registered_users[username] = password
                response = "Registration successful."
            dgram_out = pdu.Datagram(pdu.MSG_TYPE_DATA, response)
            rsp_msg = dgram_out.to_bytes()
            rsp_evnt = QuicStreamEvent(message.stream_id, rsp_msg, True)
            await conn.send(rsp_evnt)

        # Handle user login
        elif action == "login":
            username = data.get("username")
            password = data.get("password")
            if registered_users.get(username) == password:
                clients[username] = conn
                response = "Login successful"
            else:
                response = "Invalid username or password"
            dgram_out = pdu.Datagram(pdu.MSG_TYPE_DATA, response)
            rsp_msg = dgram_out.to_bytes()
            rsp_evnt = QuicStreamEvent(message.stream_id, rsp_msg, True)
            await conn.send(rsp_evnt)
        
        # Handle message sent to the recipient
        else:
            recipient = data.get("recipient")
            if recipient is None:
                print("[svr] Recipient not found.")
                return

            print("[svr] Recipient:", recipient)

            recipient_conn = clients.get(recipient)
            if recipient_conn:
                dgram_out = pdu.Datagram(pdu.MSG_TYPE_DATA, dgram_in.msg)
                new_stream_id = recipient_conn.new_stream()
                stream_event = QuicStreamEvent(new_stream_id, dgram_out.to_bytes(), False)
                await recipient_conn.send(stream_event)
            else:
                print("[svr] Recipient is not connected.")

            # Send message acknowledgment back to the sender
            dgram_out = dgram_in
            dgram_out.mtype |= pdu.MSG_TYPE_DATA_ACK
            dgram_out.msg = "SVR-ACK: " + dgram_out.msg
            rsp_msg = dgram_out.to_bytes()
            rsp_evnt = QuicStreamEvent(message.stream_id, rsp_msg, False)
            await conn.send(rsp_evnt)
