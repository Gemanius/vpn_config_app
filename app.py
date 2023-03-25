from config_info import create_response
from flask import Flask

app = Flask(__name__)


@app.route("/<name>", methods=["GET"])
def get_information(name):
    if name == "favicon.ico":
        return "this is "
    print(name)
    response = create_response(name)
    return response
    # return json.dumps(response)


app.run(port=5000,host="0.0.0.0")
