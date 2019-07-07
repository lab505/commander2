import socketserver, logging, threading,math
def bin_to_int(bin):
    bin=list(bin)
    int1=0
    if(bin[0]=='0'):
        int1=int(''.join(bin),2)
    else:
        for i in range(len(bin)):
            if(bin[i]=='0'):
                bin[i]='1'
            else:
                bin[i]='0'
        for i in range(len(bin)):
            if(bin[len(bin)-i-1]=='0'):
                bin[len(bin)-i-1]='1'
                break
            else:
                bin[len(bin)-i-1]='0'
        int1=int(''.join(bin),2)
        int1=-int1
    return int1

class FlyDataServer():
    _instance = None

    @staticmethod
    def get_instance():
        assert FlyDataServer._instance is not None
        return FlyDataServer._instance

    def __init__(self, ):
        #self.rc = rc
        FlyDataServer._instance = self
        #ip, port = rc.cfg['fly_data_server_ip'], int(rc.cfg['fly_data_server_port'])
        ip, port='127.0.0.1',7062

        self._server = socketserver.ThreadingUDPServer((ip, port), FlyDataServer.Handler_Class)
        self._server.serve_forever()
        #self._server_thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        #self._server_thread.start()
        print('ok')

    class Handler_Class(socketserver.BaseRequestHandler):
        def handle(self):
            data = self.request[0].strip()
            print(data)
            print(str(data, encoding = "utf-8"))
            data=str(data, encoding = "utf-8")
            text=[]
            for i in range(int(len(data)/2)):
                text.append(data[2*i]+data[2*i+1])
                text[i]=bin(int(text[i], 16))[2:]
                text[i]=(8-len(text[i]))*'0'+text[i]
            text_len = len(text)
            print(text)
            now=0
            while (text[now] != '11101011' or text[now + 1] != '10010000'):
                now = now + 1
                if (now + 21 >= text_len):
                    break
            fly_num = text[now+3]
            fly_num = '0'* 3 * 4 + fly_num
            print(fly_num)
            fly_num=int(fly_num,2)
            lon = text[now + 7] + text[now + 6]+text[now + 5] + text[now + 4]
            lat = text[now + 11] + text[now + 10]+text[now + 9] + text[now + 8]
            height = text[now + 13]+text[now + 12]
            if height[0] == '1':
                height = '1' * 16 + height
            else:
                height = '0' * 16 + height
            lon = float(bin_to_int(lon)) / 1000000
            lat = float(bin_to_int(lat)) / 1000000
            height = float(bin_to_int(height))
            print([fly_num, lon, lat, height])
            return [fly_num, lon, lat, height]

a=FlyDataServer()