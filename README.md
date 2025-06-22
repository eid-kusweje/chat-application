TCP Chat Application Documentation
Overview
This TCP Chat Application is a real-time messaging system built with Python and Tkinter, consisting of a server component and a client component. The application supports both public messaging (broadcast to all users) and private messaging (direct messages between specific users).
Table of Contents
1.	Features
2.	Architecture
3.	Requirements
4.	Installation & Setup
5.	Usage Guide
6.	Server Component
7.	Client Component
8.	Message Protocol
9.	Error Handling
10.	Troubleshooting
Features
Server Features
•	Multi-client Support: Handles multiple simultaneous client connections
•	Real-time Message Broadcasting: Distributes messages to all connected clients
•	Private Message Routing: Facilitates direct messaging between users
•	Username Management: Prevents duplicate usernames and manages user sessions
•	GUI Interface: User-friendly interface for server management
•	Connection Monitoring: Real-time display of connected clients
•	Server Messages: Ability to send messages from server to all clients
•	Graceful Shutdown: Proper cleanup of connections and resources
Client Features
•	User-friendly GUI: Intuitive interface for chatting
•	Dual Message Modes: Support for both public and private messaging
•	Real-time Updates: Instant message delivery and display
•	Message Type Indicators: Visual distinction between different message types
•	Connection Management: Easy connect/disconnect functionality
•	Message History: Scrollable chat history with timestamps
•	Error Feedback: Clear error messages and status updates
Architecture
The application follows a client-server architecture:
┌─────────────────┐    TCP Socket    ┌─────────────────┐
│   Chat Server   │ ←───────────────→ │  Chat Client 1  │
│                 │                   └─────────────────┘
│  - Multi-thread │    TCP Socket    ┌─────────────────┐
│  - GUI Interface│ ←───────────────→ │  Chat Client 2  │
│  - Message      │                   └─────────────────┘
│    Routing      │        ...        
│                 │    TCP Socket    ┌─────────────────┐
│                 │ ←───────────────→ │  Chat Client N  │
└─────────────────┘                   └─────────────────┘
Key Components
1.	Server (ChatServer class)
o	Main server socket for accepting connections
o	Thread pool for handling multiple clients
o	Message broadcasting system
o	Client management and routing
2.	Client (ChatClient class)
o	Connection management
o	Message sending/receiving
o	GUI for user interaction
o	Message type handling
Requirements
•	Python 3.6+
•	tkinter (usually included with Python)
•	socket (built-in module)
•	threading (built-in module)
•	json (built-in module)
•	datetime (built-in module)
Installation & Setup
1.	Download the Files
2.	# Save the server code as 'chat_server.py'
3.	# Save the client code as 'chat_client.py'
4.	No Additional Dependencies
o	All required modules are part of Python's standard library
5.	File Structure
6.	tcp_chat_app/
7.	├── chat_server.py
8.	├── chat_client.py
9.	└── README.md (this file)
Usage Guide
Starting the Server
1.	Run the Server Application
2.	python chat_server.py
3.	Configure Server Settings
o	Host: Default is "localhost" (change for network access)
o	Port: Default is "12345" (ensure port is available)
4.	Start the Server
o	Click "Start Server" button
o	Server status will change to "Running"
o	Server will begin accepting client connections
Connecting Clients
1.	Run the Client Application
2.	python chat_client.py
3.	Configure Connection
o	Server: Enter server IP address (default: "localhost")
o	Port: Enter server port (default: "12345")
o	Username: Choose a unique username
4.	Connect to Server
o	Click "Connect" button
o	Status will change to "Connected"
o	You can now send and receive messages
Sending Messages
Public Messages
1.	Select "📢 Public (All Users)" radio button
2.	Type your message in the text field
3.	Press Enter or click "📤 SEND TO ALL"
4.	Message will be broadcast to all connected users
Private Messages
1.	Select "🔒 Private Message" radio button
2.	Enter recipient's username in the "To:" field
3.	Type your message in the text field
4.	Press Enter or click "📤 SEND PRIVATE"
5.	Message will be sent only to the specified user
Server Component
Class: ChatServer
Key Methods
•	__init__(): Initializes the server with GUI setup
•	start_server(): Starts the server socket and begins accepting connections
•	stop_server(): Gracefully shuts down the server and closes all connections
•	accept_clients(): Continuously accepts new client connections
•	handle_client(): Manages individual client communication in separate threads
•	broadcast_message(): Sends messages to all connected clients
•	handle_private_message(): Routes private messages between users
•	disconnect_client(): Handles client disconnection cleanup
GUI Elements
•	Server Controls: Host/Port configuration, Start/Stop buttons
•	Status Display: Real-time server status indicator
•	Client List: Shows all currently connected users
•	Message Log: Displays all server activities and messages
•	Server Message Input: Allows server to send messages to all clients
Data Structures
self.clients = {
    socket_object: {
        'username': 'user123',
        'address': ('127.0.0.1', 54321)
    }
}
Client Component
Class: ChatClient
Key Methods
•	__init__(): Initializes the client with GUI setup
•	connect_to_server(): Establishes connection to the server
•	disconnect_from_server(): Closes connection and updates GUI
•	listen_for_messages(): Continuously listens for incoming messages
•	send_message(): Sends public or private messages based on selection
•	display_message(): Adds messages to the chat display with proper formatting
GUI Elements
•	Connection Panel: Server details, username input, connect/disconnect buttons
•	Message Type Selection: Radio buttons for public/private message modes
•	Chat Display: Scrollable message history with color-coded message types
•	Private Message Panel: Target user selection for private messages
•	Message Input: Text field and send button for composing messages
Message Display Types
•	System Messages: Gray italic text for status updates
•	Server Messages: Red bold text for server announcements
•	Own Messages: Blue bold text for user's own public messages
•	Other Users: Green bold text for other users' public messages
•	Private Sent: Purple bold text for sent private messages
•	Private Received: Orange bold text for received private messages
Message Protocol
The application uses JSON-formatted messages over TCP sockets:
Message Types
1. Join Message (Client → Server)
{
    "type": "join",
    "username": "user123"
}
2. Public Message (Client → Server)
{
    "type": "message",
    "content": "Hello everyone!"
}
3. Private Message (Client → Server)
{
    "type": "private_message",
    "target": "recipient_username",
    "content": "Hello privately!"
}
4. Broadcast Message (Server → Clients)
{
    "type": "message",
    "username": "sender_username",
    "content": "Hello everyone!",
    "timestamp": "14:30:25"
}
5. Private Message Delivery (Server → Client)
{
    "type": "private_message",
    "sender": "sender_username",
    "content": "Hello privately!",
    "timestamp": "14:30:25"
}
6. Private Message Confirmation (Server → Sender)
{
    "type": "private_confirmation",
    "target": "recipient_username",
    "content": "Hello privately!",
    "delivered": true,
    "timestamp": "14:30:25"
}
7. System Message (Server → Clients)
{
    "type": "system",
    "message": "user123 joined the chat",
    "timestamp": "14:30:25"
}
8. Server Message (Server → Clients)
{
    "type": "server",
    "message": "Server announcement",
    "timestamp": "14:30:25"
}
9. Error Message (Server → Client)
{
    "type": "error",
    "message": "Username already taken"
}
Error Handling
Server-Side Error Handling
•	Socket Errors: Graceful handling of connection failures
•	Duplicate Usernames: Rejection of duplicate username attempts
•	Client Disconnections: Automatic cleanup of disconnected clients
•	Message Routing Errors: Error responses for failed private messages
•	JSON Parsing: Handling of malformed message data
Client-Side Error Handling
•	Connection Failures: User-friendly error messages for connection issues
•	Invalid Input: Validation of user inputs before sending
•	Server Disconnections: Automatic detection and GUI state updates
•	Message Send Failures: Error feedback for failed message attempts
•	JSON Parsing: Handling of malformed server messages
Troubleshooting
Common Issues
1. "Connection Refused" Error
•	Cause: Server is not running or wrong host/port
•	Solution: Ensure server is started and check host/port settings
2. "Username Already Taken" Error
•	Cause: Another user is already using the same username
•	Solution: Choose a different username
3. Private Message Not Delivered
•	Cause: Target username doesn't exist or user is disconnected
•	Solution: Verify the recipient's username and connection status
4. Server Won't Start
•	Cause: Port is already in use or insufficient permissions
•	Solution: Try a different port number or check for other applications using the port
5. Messages Not Appearing
•	Cause: Network connectivity issues or client disconnection
•	Solution: Check connection status and try reconnecting
Performance Considerations
•	Maximum Clients: Limited by system resources and socket limits
•	Message Size: Current implementation handles up to 1024 bytes per message
•	Threading: Each client uses a separate thread on the server
•	Memory Usage: Message history is stored in GUI components (not persistent)
Security Considerations
•	No Authentication: Basic implementation without user authentication
•	No Encryption: Messages are sent in plain text
•	No Input Validation: Limited validation of user inputs
•	Local Network: Designed for trusted local network environments
Future Enhancements
•	User authentication and authorization
•	Message encryption (SSL/TLS)
•	File transfer capabilities
•	Persistent message history
•	User roles and permissions
•	Chat rooms/channels
•	Message search functionality
•	Emoji and rich text support
License
This application is provided as-is for educational and development purposes.

