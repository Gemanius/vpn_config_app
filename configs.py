from config_customizer import Config_customizer
import json
from math import pow
from datetime import datetime
import base64

class Configs_service:
    def __init__(self,server_details):
        print("instance created",self)
        self.config_customizers=[]
        self.initial_configs(server_details=server_details)
        self.all_configs=[]
        self.get_all_configs()
            
    def initial_configs(self,server_details):
        for config in server_details["data"]:
            new_customizer=Config_customizer(username=config["username"],password=config["password"],                       
                server_ip=config["ip"],server_port=config["port"],start_server_port=config["start_server_port"],
                start_server_url=config["start_server_url"])
            self.config_customizers.append(new_customizer)
    
    def get_all_configs(self):
        for customizer in self.config_customizers:
            configs=customizer.get_configs()
            self.all_configs=[*self.all_configs,*configs]
        return self.all_configs
            
    def update_configs(self):
        print("it is called to be updated ")
        for customizer in self.config_customizers:
            customizer.update_configs()
        self.all_configs=[]
        self.get_all_configs()

    
    def find_config_by_remark(self,remark):
        result= next((config for config in self.all_configs if config["remark"]==remark ),None)
        return Config_formater(result)
        
    
    def find_config_by_id(self,id):
        iter_configs=iter(self.all_configs)
        while True:
            data=next(iter_configs,None)
            if data == None:
                return "not found"
            data_id=json.loads(data["settings"])["clients"][0]["id"]
            if data_id == id:
                return Config_formater(data)
    
    def find_config_by_uri(self,config_uri):
        id=""
        if config_uri.find("vmess://")>-1:
            config_uri=config_uri[8:]
            convertbytes = config_uri.encode("ascii")
            convertedbytes = base64.b64decode(convertbytes)
            config_json =convertedbytes.decode("ascii")
            config_json=json.loads(config_json)
            id=config_json["id"]
        elif config_uri.find("vless://")>-1:
            id=config_uri[8:config_uri.find("@")]
            
        return self.find_config_by_id(id)
        
    

        
class Config_formater():
    def __init__(self,config):
        self.config=config
    def usage_detail(self):
        config=self.config
        byte_to_gig=pow(1000,3)
        used=round((config["up"]+config["down"])/byte_to_gig,2)
        result=[]
        remained= round((config["total"] / pow(1024,3)) - used,2) 
        remained=remained if remained > 0 else 0
        result.append( '  مقدار حجم  استفاده شده   ' + str(used))
        result.append( '  مقدار حجم  باقی مانده   '  + str(remained))
        result.append( datetime.utcfromtimestamp(config["expiryTime"]/1000).strftime('%B %d')  +' تا تاریخ   ')
        return result
    
    def config_name(self):
        return self.config["remark"]
    
    def vmess_config_uri(self):
        config_json=self.generate_share_json()
        encoded_config = "vmess://"+str(base64.b64encode(
            str.encode(json.dumps(config_json))))[2:-1]
        return encoded_config
    
    ## not dynamic as vmess 
    def vless_config_uri(self):
        config_json=self.generate_share_json()
        uri=f'vless://{config_json["id"]}@{config_json["add"]}:{config_json["port"]}?security=none&encryption=none&type=ws&path={config_json["path"]}#{config_json["ps"]}'
        return uri
        
    
    def send_config_details(self):
        result=[]
        uri=""
        if self.config["protocol"]== "vmess":
            uri=self.vmess_config_uri()
        elif self.config["protocol"]=="vless":
            uri=self.vless_config_uri()
        usage_details=self.usage_detail()
        result=[uri,*usage_details]
        return result 
    
    def generate_share_json(self):
        config_json={
            "v": "2",
            "ps": "",
            "add": "",
            "port": 9002,
            "id": "",
            "net": "ws",
            "type": "none",
            "tls": "none",
            "path": "",
            } 
        config=self.config
        config_json["ps"]=config["remark"]
        config_json["add"]=config["listen"]
        config_json["port"]=config["port"]
        config_client_setting=json.loads(config["settings"])["clients"][0]
        config_json["id"]=config_client_setting["id"]
        config_path=json.loads(config["streamSettings"])["wsSettings"]["path"]
        config_json["path"]=config_path
        return config_json