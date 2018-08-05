# BBB_UART_demo
body heat and heart beat demo based on BeagbleBone using uart

## License
> LGPL

## 功能实现
- 长连接 *Websocket*
- 单词发送 *HTTP POST*
- 硬件开发 *BeagbleBone/BeagbleBone-Black for Python*

## 使用提示
- 本模块仅支持 Python 3.x 版本
- 本模块目前仅测试于 *Github* 提供的 webscoket-client 模块环境
- 本模块为了适配服务器时间，建议使用时将其时间调至上海时区时间（非UTC）并进行校准


#### `LocalTime` 系统时间封装类
> 此类无需初始化
- `get_current_time` 获得系统当前时间
#### `HTTPPost` HTTP协议POST至服务器封装类定义（只可单向）：
```
    def __init__(self, ip_address = "127.0.0.1", port = 9006,
                 api_key = None, device_id = None,
                 user_data = "Hi I'm Python",
                 dev_num = None,sleep_time = 3):
```
- `messages_send_to_server` 定义POST到服务器的数据包
- `post_forever` 循环POST数据包至服务器，失败仍重发
#### `Websocket` Websocket协议与服务保持长连接封装类定义：
```
    def __init__(self, ip_address = "127.0.0.1",
                 port = 9000, api_key = None, dev_id = None,
                 data = 'Hi I,m Python',sleep_time = 3):
        """
        :param ws: websocket object
        :param ip_address: the default value is "127.0.0.1"
        :param port: the default value is 9006
        """
```
- `connect_to_server` 与服务器建立长连接
- `send_message` 向服务器发送数据
- `recv_from_server` 接受服务器数据，并对心跳包进行处理
- `run_forever` 断线重连，一直保持连接

## 注意事项
若出现无法运行错误，可将项目中包含的*websocket*包拷贝至本机python链接库中
```
Path In Debian Release:
/usr/local/lib/dist-packages/python3.x
```

需要安装*dafruit-beaglebone-io-python*库
将adafruit-beaglebone-io-python拷贝至本机，或从github仓库下载
<https://github.com/adafruit/adafruit-beaglebone-io-python>

```
sudo ntpdate pool.ntp.org
sudo apt-get update
sudo apt-get install build-essential python-dev python-pip python-smbus -y
git clone git://github.com/adafruit/adafruit-beaglebone-io-python.git
cd adafruit-beaglebone-io-python
sudo python setup.py install
cd ..
sudo rm -rf adafruit-beaglebone-io-python
```
