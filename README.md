## This is a Client-Server chat application by which two user can connect with each other directly without any outer means.

## HOW TO USE :
Start Server by calling .\server.py if you are in same directory.
Start client by calling .\client.py if you are in same directory.

## DESCRIPTION

In this project, I have developed a super secure communication system to build custom terminals to communicate with each other.
The communication is peer-to-peer between the peers, but they communicate with the server to log into the system and to get information.
Once the communication between  terminals is established, the server is idle.
The most important is the communication between the client and the server.
As the client-server interaction progresses, the client moves through several states.

![image](https://user-images.githubusercontent.com/68592197/115954670-d3b6d800-a50f-11eb-929f-aff1656a1fd1.png)

#### Typical session
Both users must first log into the system. Each sends an Authentication Request to the server,
including the user ID and passcode. The server replies with an Authentication Reply granting them access, 
in the case of a passcode match, or denying access otherwise. When a user is logged in, the server remembers that user’s IP address. 
After logging in successfully, each terminal opens a socket to listen for incoming connections on port 65000.
A typical session begins by user A (Ali) at one terminal wishing to communicate with user B (Bianca) at her terminal.
Ali sends a Lookup Request to the server asking for Bianca’s address. If encryption is implemented, the server also gives Ali the encryption key for Bianca.
Next, Ali’s terminal attempts to socket.connect(ADDRESS) a TCP connection to Bianca’s address on port 65000. 
If Bianca is logged in and her terminal is "socket.accept()" -ing connections, Ali’s terminal sends a Connect Request. 
Bianca must make sure that the connection request is legitimate. Bianca sends a Lookup Request to the server to verify Ali’s IP address and  Ali’s encryption key.
Once Bianca has verified Ali’s connection request, Bianca sends a Connection Reply to Ali. Finally, the communication proceeds. 
Each terminal goes through an infinite loop of input()send() and recv()print().
The communication ends when either user types CTRL-C to end the chat session. After the end, each terminal continues to listen for 
connection requests to begin another chat session.
A typical session session might look like this. Here ali talks to bianca then types CTRL-C to end the connection

    Login: ali
    Enter passcode on keypad. Logged in.
    Enter destination user ID: bianca Connection established, type your messages Hello, how are you today?
    I am fine, how about you?
    I am well. Goodbye.
    CTRL-C connection ended Enter destination user ID:
    
In another session, ali is logged in and receives a connection request from bianca who then types CTRL-C to end the connection (what ali types is in italics).

    Login: ali
    Enter passcode on keypad. Logged in.
    Enter destination user ID:
    Connection received from user bianca, type your messages Hello, how are you today?
    I am fine, how about you?
    I am well. Goodbye. Connection ended
    Enter destination user ID:
    
### Communications protocol
The chat session must start with several phases to log in to the system, request user information and request a chat connection before any messages can be exchanged. The chat client goes through several states during the phases of the connection.
Information exchange between server and client is done with JSON formatted messages. Each message is a sequence of name:value pairs. Message types are identified with the msgtype key present in all messages.
### Authentication phase
Each client sends an Authentication Request to the server. The authentication request includes the user ID and the hashed passcode. The server looks up the user ID and compares the hashed passcode to the hashed passcode it has stored. If the hashed passcodes match, the server returns an Authentication Reply message and also stores the current IP address of the user who has just authenticated.
The client sends an Authentication Request message to the server (Listing 1).

    1. userid: string as entered by the user making the request;
    2. passcode: the user’s passcode entered by the user on the keypad, then salted and hashed (see passcode hashing section).

The server sends the Authentication Reply message to the client telling the client if the user is authenticated or not

    status: “GRANTED” if the credentials were accepted, “REFUSED” otherwise.
    
### Lookup phase
The initiating client sends a Lookup Request to the server. The request includes the user ID of the initiator and the user ID of the person the initiator wishes to contact. The server replies with a Lookup Reply message giving information about the person, or no information if that person is not logged in. As a precaution against requests by users not logged in, the server also replies with no information if the user making the request is not logged in. The server replies with a Lookup Reply message. The reply includes the user ID of the person the initiator wishes to contact, the IP address of her/his client and (optional) the encryption key to be used when communicating with that person.
The client sends the Lookup Request message to the server

    lookup: the user ID of the person that the user is calling.
    
 The server sends the Lookup Reply message to the client, with “status”:“SUCCESS” and information if found (Listing 5), or “status”:“NOTFOUND” and empty information fields otherwise
  
### Connection phase
The initiating terminal sends a Connection Request to the destination terminal. The request includes the user ID of the initiator. The destination terminal performs a Lookup Request of its own to the server and, if the address of the initiating user’s terminal matches the one registered with the server, the destination terminal replies with a Connect Reply “accepted” message to go ahead with the chat session, otherwise it sends a Connect Reply “refused” message.
The initiator sends the Connect Request message to the destination terminal

    initiator: the user ID of the person making the request.
    
### Chat phase
No special messaging format is required in the chat phase. The two-way connection is established between terminals and the main loop can simply read from the open connection as if it was a stream of bytes. Each client can “catch” the CTRL-C KeyboardInterrupt to end the chat at any time. No special protocol is needed to end a session.

## STATECHART

![image](https://user-images.githubusercontent.com/68592197/115954884-07dec880-a511-11eb-88eb-11546f68b279.png)

