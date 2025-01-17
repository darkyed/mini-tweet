# Mini-Tweet 
Mini-Tweet is a Command Line Interface based Twitter in which you can register/login, post tweets, follow/unfollow others, get updates, read followed tweets and search tweets based on hashtag. 

For this to run, you need

1) Mininet 
2) WinSCP 
3) Xming, PuTTY (for Windows users)
   

## Project Structure

### tcp_utills
`tcp_utills` contains the main code for the client and the server in `tcp_client.py` and `tcp_server_sc_thread.py` respectively.

### UtilFuncs
The package `UtilFuncs` contains the utility programs used indirectly by client and server.

#### User
- User class and some methods to facilitate the workflow

#### manageDB
- Contains all the basic functionality required to interact with the database defined in form of a class

#### screens
Contains two classes used frequently by both the client and the server
- Interaction
  - This class has static methods to present the user interface at the client side at every point of time until client logs-out
  - It also contains some basic functionalities which are used by the server under the hood
- Authenticate
  - The methods defined under this class are also static, thus they do not need any initialization
  - It contains methods which are used by the server for authenticating a client by check his/her credentials


### PuTTY Command Line for mininet in Windows
Command "xterm" in mininet helps in giving hosts seperate command terminals. But for Windows, xterm command is not possible. So, to make xterm work, we need to do the following. 

Before starting in Mininet (in Virtual Box), open Settings for Mininet, and in the Network section, select any disabled adapter, enable it and select Bridged Adapter and click "Ok".

Now, open Mininet, login using username and password as mininet and run the following command to get the eth0's inet address.
```
mininet@mininet-vm:~$ ifconfig
```
Now, 
1) Open Xming and PuTTY
2) In the left nav bar of PuTTY, expand SSH and select X11 and check X11 forwarding
3) Click on Session, and type the inet address shown by the mininet and click "Ok".

Now, PuTTY opens a command line prompt with the host address specified in the host address in the session. Login using mininet as username and password. In this xterm command is possible. This command line prompt is used to make topologies, run server and client.

### Sending files to Mininet
For this we need to open WinSCP, and in the host name, fill the eth0's inet address in the host name, mininet as username and password. Now, you'll have access to mininet's files.

Now, send the whole folder "mini-tweet" to mininet from your computer using WinSCP and now the whole setup process is done.

If the folder is already present, then it is not required to send again via WinSCP. 

### Run mini-tweet
Open the folder mini-tweet and PuTTY command line, you can create any topology which contain 2 or more hosts (one for server and others for clients)
```  
mininet@mininet-vm:~$ sudo mn --topo=tree,5,2
```

This creates mininet hosts, switches, and links. Now, to open hosts h1 and h2,
```
mininet> xterm h1 h2
```

A command line opens for each of the hosts. To run the server, open the host which you wanted to make as server and type
```
root@mininet-vm:~# python3 tcp_utils\tcp_server_sc_thread.py
```
To open a host as a client, in its respective command line, type
```
root@mininet-vm:~# mininet_client_test.py
```
You can have muliple clients running on a single server.


### Finite State Machine for Server
If you are interested in checking out thow the server functions, and how it proceeds as the client requests something from it, then see the file at [FSM Server](server_fsm.pdf)


### Running without Mininet
If you want You can run the code even without mininet with following command. 

- Run the server in one terminal
```
python3 tcp_utils\tcp_server_sc_thread.py
```

- Open a seperate terminal for every time you want to add a new client

```
python3 client_test.py
```

Note: Notice how we are using `client_test.py` here instead of `mininet_client_test.py`



### Dependencies

- Mininet VM
- Python 3.6
- sqlite3 Library for Python3.6 (Builtin)
- threading Library for Python3.6 (Builtin)
- getpass Library for Python3.6 (Builtin)
- logging library for Python3.6 (Builtin)
