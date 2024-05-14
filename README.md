# CipherComm (DESKTOP APPLICATION)

```
By: Vaibhav Aggarwal(2021UIT3043)
```
```
Khushi (2021UIT3046)
```
## (using socket programming in python)

Our Python-based server-client application, enhanced with intuitive Tkinter GUIs for both the
server and client interfaces, provides a secure platform for communication within organizations.
The server oversees user database management, enabling authorized users to engage in text-
based messaging. Utilizing RSA encryption ensures data confidentiality during message

## transmission, while SHA256 authentication guarantees user security.

In the upcoming phases, we plan to enhance functionality by enabling file sharing capabilities,
empowering clients to upload and share files seamlessly. Additionally, we aim to integrate
features such as private chatrooms and client-level constraints, allowing for more tailored
communication experiences within the organization. Also will be working on the GUI part for
both client and server application in the upcoming days.

Through these advancements, our project strives to offer a comprehensive solution for secure and
efficient intra-organizational communication, promoting collaboration and productivity while
upholding stringent security standards.

## Getting Started

To run the SecureComm application, follow these steps:

```
 Clone this repository to your local machine.
 Install the required dependencies (pip install -r requirements.txt).
 Run the server script (python server.py).
 Run the client script (python client.py).
```
## Contact Information

For questions or feedback, please contact:

Vaibhav Aggarwal
Khushi

Email: aggarwalvaibhav11022003@gmail.com
Email: khushi.ug21@nsut.ac.in

GitHub: Vaibhav11022003 (github.com)


Feel free to customize the README file with your specific project details, contact information,
and any additional information you'd like to include. This will help others understand your
project and easily reach out to you if needed.

https://drive.google.com/file/d/10aPvFtVx4iw0qIQmzzFzDxbleH0LXaXu/view?usp=drive_link


# server.py

(server.drawio - draw.io (diagrams.net) for flow charts)

https://drive.google.com/file/d/10aPvFtVx4iw0qIQmzzFzDxbleH0LXaXu/view?usp=drive_link

## Wireshark(software)

Wireshark is a network protocol analyzer that captures and displays packet data transmitted over
a network. When it comes to encrypted versus non-encrypted packets, Wireshark can indeed
capture both types of packets, but there are differences in what you can see and interpret.

1.Non-Encrypted Packets:

For non-encrypted packets, Wireshark can fully analyze and display the contents of the packets.
This includes details such as source and destination IP addresses, port numbers, protocol
information, and the payload data.


2.Encrypted Packets:

With encrypted packets, Wireshark can capture the packets as they are transmitted over the
network, but the payload data is encrypted and appears as ciphertext.

## Ngrok (software)

Ngrok creates a secure tunnel between a public endpoint and a local IP address and port on your
computer. This means that it takes the data sent to the public endpoint and forwards it to the
specified local IP address and port, and vice versa. Essentially, it allows external traffic from the
internet to access your locally hosted server or application running on your computer through a
secure connection. Similarly, responses from your local server are sent back through Ngrok to the
requester on the internet. This enables you to share and test your locally hosted services with others
over the internet without exposing your local machine directly.

(ONLY FOR TESTING PHASE)

Local IP and PORT adress of server:

IP=127.0.0.1 PORT=

Public IP and PORT adress of server:

IP=3.6.115.182 PORT=
