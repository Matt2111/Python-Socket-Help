def AddHeader(Message):
    if len(str(len(Message))) < 11:
        Header = "".join(["0" for k in range(11 - len(str(len(Message))))]) + str(len(Message))
    else:
        Header = len(str(len(Message)))
    return Header + Message

def SendMessage(Client, Message):
    if not isinstance(Client, tuple):
        Client = [Client, ""]
    Client[0].send(bytes(AddHeader(Message), encoding="utf-8"))

def ReceiveMessage(Client):
    if not isinstance(Client, tuple):
        Client = [Client, ""]
    MsgLength = Client[0].recv(11).decode("utf-8")
    if MsgLength == "":
        print("Nothing")
        return ""
    Total = int(MsgLength) // 64
    Spare = int(MsgLength) % 64
    Message = str()
    for x in range(Total):
        Message += Client[0].recv(64).decode("utf-8")
    if Spare:
        Message += Client[0].recv(Spare).decode("utf-8")
    return Message

def GetMessageHeader(Message):
    if len(str(len(Message))) < 11:
        Header = "".join(["0" for k in range(11 - len(str(len(Message))))]) + str(len(Message))
    else:
        Header = str(len(str(len(Message))))
    return Header

def SendMessageB(Client, Message):
    if not isinstance(Client, tuple):
        Client = [Client]
    Client[0].send(bytes(GetMessageHeader(Message), encoding="utf-8"))
    Client[0].send(Message)

def SendFile(Client, FileLocation, FileName):
    SendMessage(Client, FileName)
    with open(FileLocation+FileName, "rb") as File:
        Lines = File.readlines()
    SendMessage(Client, str(len(Lines)))
    for Line in Lines:
        SendMessageB(Client, Line)

def ReceiveFile(Client, FileLocation):
    FileName = ReceiveMessage(Client)
    Lines = int(ReceiveMessage(Client))
    with open(FileLocation+FileName, "wb") as File:
        for Line in range(Lines):
            if not isinstance(Client, tuple):
                Client = [Client]
            MsgLength = Client[0].recv(11).decode("utf-8")
            Total = int(MsgLength) // 64
            Spare = int(MsgLength) % 64
            for x in range(Total):
                File.write(Client[0].recv(64))
            if Spare:
                File.write(Client[0].recv(Spare))
