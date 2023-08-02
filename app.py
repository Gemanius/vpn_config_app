from flask import Flask
from config_info import create_response
from server_class import Server
import telegram
import json
from configs import Configs_service


server_details=open("./server_details.json")
server_details=json.load(server_details)
config_service=Configs_service(server_details=server_details)
app = Flask(__name__)
bot=telegram.Bot(token="6372238157:AAFesiFi15vJC7EaBveXqImnpBCbVyWxB50")

@app.route("/", methods=["GET"])
def get_information():  
    return config_service.get_all_configs()
@app.route("/remark/<remark>", methods=["GET"])
def get_information_by_remark(remark):  
    return config_service.find_config_by_remark(remark=remark).generate_share_json()
@app.route("/id/<id>", methods=["GET"])
def get_information_by_id(id):  
    return config_service.find_config_by_id(id).send_config_details()
@app.route("/conf/<conf>", methods=["GET"])
def get_information_by_conf(conf):  
    return config_service.find_config_by_uri(conf).send_config_details()


if __name__=="__main__":
    app.run(port=5001,host="0.0.0.0")
