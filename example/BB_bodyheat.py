import websocket
import threading
import time
import json
import Adafruit_BBIO.UART as UART
import serial

broke_data = 0xffff
r = [0xA5, 0x15, 0xBA]

def bodyHeat():

    def getval():
        counter = 0
        Re_buf = []
        while (counter < 9):
            Re_buf.append(ser.read())
            if(counter==0 and Re_buf[0]!=0x5A):
                exit 0                  // 检查帧头         
            counter++ 
            if(counter==9):             //接收到数据
                counter=0               //重新赋值，准备下一帧数据的接收 
                sign=1;

        return Re_buf

    def GetResult():
        if(sign):
            sign=0;
        for i in range(7):
            sum = sum + Re_buf[i]; 
        if(sum==Re_buf[i])        //检查帧头，帧尾

           TO=(Re_buf[4]<<8|Re_buf[5])/100;
           ser.print("TO:");
           Serial.println(TO);  
           TA=(Re_buf[6]<<8|Re_buf[7])/100;
           Serial.print("TA:");
           Serial.println(TA);           
            
        return TO, TA

    TO, TA = GetResult()
    return TO, TA

def GetCurrentTime():
    TimeStruct = time.localtime(time.time())
    LocalTime = time.strftime("%Y-%m-%d %H:%M:%S",TimeStruct)
    return LocalTime

def Connect_to_server(ws):
    ws.connect("ws://47.92.48.100:9000/")
    Auth = {"api_key": "b41b53ea325d49e7b970fc56238bce8a", "device_id": "430000", "data": "Hi I'm BH", "time": GetCurrentTime()}
    ws.send(json.dumps(Auth))

def SendMessage(ws):
    while(True):
        TO,TA = bodyHeat()
        if hum == broke_data:
            time.sleep(2)
            continue
        data = {"TO": TO, "TA": TA}
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
    UART.setup("UART4")
    ser = serial.Serial(port = "/dev/ttyS4", baudrate=115200)
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
