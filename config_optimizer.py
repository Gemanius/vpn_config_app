from server_class import Server

class Config_Optimizer():
    def __init__(self,server_ip,server_port,username,password,start_server_url,start_server_port):
        self.server=Server(server_ip=server_ip,server_port=server_port,password=password,username=username)
        self.start_server_url=start_server_url
        self.start_server_port=start_server_port
        self.update_configs()
        
    def optimize_config_json(self):
        def optimize(config):
            config["listen"]=self.start_server_url
            config["port"]=self.start_server_port
            return config
        return list(map(optimize,self.configs))
        
    def update_configs(self):
        self.configs=self.server.get_configs()
        self.configs= self.optimize_config_json()
        
    def get_configs(self):
        return self.configs
        
        
        
    
    