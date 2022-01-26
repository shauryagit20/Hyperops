import socket
import json
import threading

Socket =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Port =  1981
TIME = ['07:00:00-07:05:30', '07:06:30-07:12:00', '07:13:00-07:18:30', '07:19:30-07:25:00', '07:26:00-07:31:30', '07:32:30-07:38:00', '07:39:00-07:44:30', '07:45:30-07:51:00', '07:52:00-07:57:30', '07:58:30-08:04:00', '08:05:00-08:10:30', '08:11:30-08:17:00', '08:18:00-08:23:30', '08:24:30-08:30:00', '08:31:00-08:36:30', '08:37:30-08:43:00', '08:44:00-08:49:30', '08:50:30-08:56:00', '08:57:00-09:02:30', '09:03:30-09:09:00', '09:10:00-09:15:30', '09:16:30-09:22:00', '09:23:00-09:28:30', '09:29:30-09:35:00', '09:36:00-09:41:30', '09:42:30-09:48:00', '09:49:00-09:54:30', '09:55:30-10:01:00', '10:02:00-10:07:30', '10:08:30-10:14:00', '10:15:00-10:20:30', '10:21:30-10:27:00', '10:28:00-10:33:30', '10:34:30-10:40:00', '10:41:00-10:46:30', '10:47:30-10:53:00', '10:54:00-10:59:30', '11:00:30-11:06:00', '11:07:00-11:12:30', '11:13:30-11:19:00', '11:20:00-11:25:30', '11:26:30-11:32:00', '11:33:00-11:38:30', '11:39:30-11:45:00', '11:46:00-11:51:30', '11:52:30-11:58:00', '11:59:00-12:04:30', '12:05:30-12:11:00', '12:12:00-12:17:30', '12:18:30-12:24:00', '12:25:00-12:30:30', '12:31:30-12:37:00', '12:38:00-12:43:30', '12:44:30-12:50:00', '12:51:00-12:56:30', '12:57:30-13:03:00', '13:04:00-13:09:30', '13:10:30-13:16:00', '13:17:00-13:22:30', '13:23:30-13:29:00', '13:30:00-13:35:30', '13:36:30-13:42:00', '13:43:00-13:48:30', '13:49:30-13:55:00', '13:56:00-14:01:30', '14:02:30-14:08:00', '14:09:00-14:14:30', '14:15:30-14:21:00', '14:22:00-14:27:30', '14:28:30-14:34:00', '14:35:00-14:40:30', '14:41:30-14:47:00', '14:48:00-14:53:30', '14:54:30-15:00:00', '15:01:00-15:06:30', '15:07:30-15:13:00', '15:14:00-15:19:30', '15:20:30-15:26:00', '15:27:00-15:32:30', '15:33:30-15:39:00', '15:40:00-15:45:30', '15:46:30-15:52:00', '15:53:00-15:58:30', '15:59:30-16:05:00', '16:06:00-16:11:30', '16:12:30-16:18:00', '16:19:00-16:24:30', '16:25:30-16:31:00', '16:32:00-16:37:30', '16:38:30-16:44:00', '16:45:00-16:50:30', '16:51:30-16:57:00', '16:58:00-17:03:30', '17:04:30-17:10:00', '17:11:00-17:16:30', '17:17:30-17:23:00', '17:24:00-17:29:30', '17:30:30-17:36:00', '17:37:00-17:42:30', '17:43:30-17:49:00', '17:50:00-17:55:30', '17:56:30-18:02:00', '18:03:00-18:08:30', '18:09:30-18:15:00', '18:16:00-18:21:30', '18:22:30-18:28:00', '18:29:00-18:34:30', '18:35:30-18:41:00', '18:42:00-18:47:30', '18:48:30-18:54:00', '18:55:00-19:00:30', '19:01:30-19:07:00', '19:08:00-19:13:30', '19:14:30-19:20:00', '19:21:00-19:26:30', '19:27:30-19:33:00', '19:34:00-19:39:30', '19:40:30-19:46:00', '19:47:00-19:52:30', '19:53:30-19:59:00', '20:00:00-20:05:30', '20:06:30-20:12:00', '20:13:00-20:18:30', '20:19:30-20:25:00', '20:26:00-20:31:30', '20:32:30-20:38:00', '20:39:00-20:44:30', '20:45:30-20:51:00', '20:52:00-20:57:30', '20:58:30-21:04:00', '21:05:00-21:10:30', '21:11:30-21:17:00', '21:18:00-21:23:30', '21:24:30-21:30:00', '21:31:00-21:36:30', '21:37:30-21:43:00', '21:44:00-21:49:30', '21:50:30-21:56:00', '21:57:00-22:02:30', '22:03:30-22:09:00', '22:10:00-22:15:30', '22:16:30-22:22:00', '22:23:00-22:28:30', '22:29:30-22:35:00', '22:36:00-22:41:30', '22:42:30-22:48:00', '22:49:00-22:54:30', '22:55:30-23:01:00', '23:02:00-23:07:30', '23:08:30-23:14:00', '23:15:00-23:20:30', '23:21:30-23:27:00', '23:28:00-23:33:30', '23:34:30-23:40:00', '23:41:00-23:46:30', '23:47:30-23:53:00', '23:54:00-23:59:30', '1900-01-01 00:00:30-1900-01-01 00:06:00']
Socket.bind(("192.168.1.31",Port))

def Handle_Client(conn,addr):
    print(f"New Client: {addr}")
    while True:
        connected = True
        msg = conn.recv(1024).decode()
        o = ""
        while msg:
            if(msg == "TotalPassengers"):
                with open("Portal_Details.json","r+") as f:
                    data =  json.load(f)
                d =  str(data["Total_Passengers"])
                o = d
                data_to_send =  d + (" " * (30-len(d)))
                conn.send(data_to_send.encode())
                break
            elif(msg == "Platform1"):
                with open("Portal_Details.json", "r+") as f:
                    data = json.load(f)
                d = str(data["Platform 1"]["Total Passengers"])
                data_to_send = d + (" " * (30 - len(d)))
                conn.send(data_to_send.encode())
                break
            elif (msg == "Platform2"):
                with open("Portal_Details.json", "r+") as f:
                    data = json.load(f)
                d = str(data["Platform 2"]["Total Passengers"])
                data_to_send = d + (" " * (30 - len(d)))
                conn.send(data_to_send.encode())
                break
            elif (msg == "Platform3"):
                with open("Portal_Details.json", "r+") as f:
                    data = json.load(f)
                d = str(data["Platform 3"]["Total Passengers"])
                data_to_send = d + (" " * (30 - len(d)))
                conn.send(data_to_send.encode())
                break
            elif (msg == "Platform4"):
                with open("Portal_Details.json", "r+") as f:
                    data = json.load(f)
                d = str(data["Platform 4"]["Total Passengers"])
                data_to_send = d + (" " * (30 - len(d)))
                conn.send(data_to_send.encode())
                break
            elif (msg == "Platform5"):
                with open("Portal_Details.json", "r+") as f:
                    data = json.load(f)
                d = str(data["Platform 5"]["Total Passengers"])
                data_to_send = d + (" " * (30 - len(d)))
                conn.send(data_to_send.encode())
                break
            elif (msg == "Platform6"):
                with open("Portal_Details.json", "r+") as f:
                    data = json.load(f)
                d = str(data["Platform 6"]["Total Passengers"])
                data_to_send = d + (" " * (30 - len(d)))
                conn.send(data_to_send.encode())
                break
            elif (msg == "Platform7"):
                with open("Portal_Details.json", "r+") as f:
                    data = json.load(f)
                d = str(data["Platform 7"]["Total Passengers"])
                data_to_send = d + (" " * (30 - len(d)))
                conn.send(data_to_send.encode())
                break
            elif (msg == "Platform8"):
                with open("Portal_Details.json", "r+") as f:
                    data = json.load(f)
                d = str(data["Platform 8"]["Total Passengers"])
                data_to_send = d + (" " * (30 - len(d)))
                conn.send(data_to_send.encode())
                break


def start():
    Socket.listen()
    while True:
        conn, addr = Socket.accept()
        print(f"New Connection -- {conn}")
        thread =  threading.Thread(target = Handle_Client,args=(conn,addr) )
        thread.start()


start()
