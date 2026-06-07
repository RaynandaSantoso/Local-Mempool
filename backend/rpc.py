from requests import auth
import os
import requests
from dotenv import load_dotenv

# load from .env
load_dotenv(dotenv_path="backend/.env")

# bitcoin RPC variables
host = os.getenv("RPC_HOST")
password = os.getenv("RPC_PASSWORD")
user = os.getenv("RPC_USER")
port = os.getenv("RPC_PORT")
url = f"http://{host}:{port}"


def rpc(method, params= []):
    payload = {
        "jsonrpc": "1.0",
        "method": method, 
        "params": params,
        "id": 1
    }
    data = requests.post(url, json=payload, auth=(user, password))
    return data.json()["result"]

if __name__ == "__main__":
    print(rpc("getblockchaininfo"))