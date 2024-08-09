from flask import Flask, request # type: ignore
import requests
import os
import json

app = Flask(__name__)

def get_api_key() -> str:
    secret = os.environ.get("OCI_API_KEY")
    if secret:
        return secret
    else:
        # local testing
        with open('.key') as f:
            return f.read().strip()
      
@app.route("/")
def hello():
    return "Add workers to the Spark cluster with a POST request to add"

@app.route("/test")
def test():
    # return "Test" # testing 
    return get_api_key()

@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return "Use POST to add"  # replace with form template
    else:
        token = get_api_key()
        ret = addWorker(token, request.form['num'])
        return ret

def addWorker(token, num):
    with open('payload.json') as p:
        tdata = json.load(p)
    
    tdata['displayName'] = 'slave' + str(num)
    
    data = json.dumps(tdata)
    url = 'https://iaas.uk-london-1.oraclecloud.com/20160918/instances'
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    resp = requests.post(url, headers=headers, data=data)
    if resp.status_code == 200:
        return "Done"
    else:
        print(resp.content)
        return f"Error\n{resp.content.decode('utf-8')}\n\n\n{data}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
