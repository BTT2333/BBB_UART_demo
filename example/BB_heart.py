import websocket
import threading
import time
import json
import Adafruit_BBIO.UART as UART
import serial

broke_data = 0xffff
r = [0xFD, 0x00, 0x00, 0x00, 0x00, 0x00]

def heart():

    def getval():
        counter = 0
        Re_buf = []
        while (counter < 6):
            Re_buf.append(ser.read())
            if(counter==0 and Re_buf[0]!=0x5A):
                exit 0                  // 检查帧头         
            counter++ 
            if(counter==6):             //接收到数据
                counter=0               //重新赋值，准备下一帧数据的接收 
                sign=1;

        return Re_buf

    def GetResult():
        if(sign):
            sign=0
        HBP=Re_buf[1]
        LBP=Re_buf[2]
        HB=Re_buf[3]
            
        return HBP,LBP,HB

    HBP,LBP,HB = GetResult()
    return HBP,LBP,HB

def GetCurrentTime():
    TimeStruct = time.localtime(time.time())
    LocalTime = time.strftime("%Y-%m-%d %H:%M:%S",TimeStruct)
    return LocalTime

def Connect_to_server(ws):
    ws.connect("ws://47.92.48.100:9000/")
    Auth = {"api_key": "b41b53ea325d49e7b970fc56238bce8a", "device_id": "430000", "data": "Hi I'm Heart", "time": GetCurrentTime()}
    ws.send(json.dumps(Auth))

def SendMessage(ws):
    while(True):
        HBP,LBP,HB = heart()
        if hum == broke_data:
            time.sleep(2)
            continue
        data = {"HBP": HBP, "LBP": LBP, "HB": HB}
        data = json.dumps(data)
        Auth = {"api_key": "b41b53ea325d49e7b970fc56238bce8a", "device_id": "430000", "data": data, "time": GetCurrentTime()}
        Json_Send = json.dumps(Auth)
        ws.send(Json_Send)
        time.sleep(3)

def RecvFromServer(ws):
    while(True):
        jsondata = ws.recv()
        if jsondata == 'HEART_BEAT':
            time = GetCurrentTime()
            print('Heart Is Beating %s' % (time))
        else:
            print("Receive From Server: %s" % jsondata)


if __name__=='__main__':
    UART.setup("UART1")
    ser = serial.Serial(port = "/dev/ttyS1", baudrate=115200)
    ser.open()
    if ser.isOpen():
	   print "Serial is open!"
    ser.write(r)
    ws = websocket.WebSocket()
    while(True):
        try:
            Connect_to_server(ws)
            send_thread = threading.Thread(target = SendMessage, args=(ws,))
            recv_thread = threading.Thread(target = RecvFromServer, args=(ws,))
        except:
            print("Restart connecting...")
            time.sleep(3)
            continue
        send_thread.start()
        recv_thread.start()
        send_thread.join()
        recv_thread.join()
