from flask import Flask
from config_info import create_response

app = Flask(__name__)


@app.route("/<name>", methods=["GET"])
def get_information(name):
    if name == "favicon.ico":
        return "this is "
    
    response = create_response(name)
    return response
    # return json.dumps(response)

if __name__=="__main__":
    app.run(port=5001,host="0.0.0.0")
