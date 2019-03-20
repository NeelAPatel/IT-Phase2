# IT-Phase2

Expanding on IT-Phase1 project, now uses two TS servers (.com server and .edu server), an RS server, and a client server. 

- Root Server (RS) has 3 sockets now. One for client, one for .com server, and one for .edu server.
- Root Server operates in Recursive mode. 
- If RS does not find Client's host name, it will recursively contact the two TS servers. 

---------
- Class project for Rutgers University's Internet Technology class
