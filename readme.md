## QUIC Chat Protocol

In order to run the server and client app built over QUIC chat protocol, the following command lines need to be run:
For Windows:
	1. run `python echo.py server` using cmd to start the server
	2. run `python echo.py client` using cmd to start the client

For Linux/MacOS:
	1. run `python3 echo.py server` to start the server
	2. run `python3 echo.py client` to start the client
	
All the dependencies listed in the requirements.txt needs to be installed using pip.

The expected output have already been provided in a folder called "output_screenshot".


The output for server:
```
[svr] Server starting...
[svr] received message: {"action": "register", "username": "bob", "password": "123"}
[svr] received message: {"action": "login", "username": "bob", "password": "123"}
[svr] received message: Hello, I am Bob..

```


The output for client:
```
[cli] starting client
Enter your username for registration: bob
Enter your password for registration: 123
[cli] Registration response:  Registration successful.
Enter your username for login: bob
Enter your password for login: 123
[cli] Login response:  Login successful
Enter "msg" to send a message or "logout" to logout: msg
Enter the message to send to the server: Hello, I am Bob..
```
