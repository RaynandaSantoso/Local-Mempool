from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.rpc import rpc

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/mempool")
def get_mempool():
    return rpc("getmempoolinfo")

@app.get("/api/node/info")
def get_node_info():
    data = rpc("getblockchaininfo")
    node_info = {
        "chain": data["chain"],
        "blocks": data["blocks"],
        "difficulty": data["difficulty"],
        "pruned": data["pruned"],
        "pruneheight": data.get("pruneheight", None),
        "size_on_disk": data["size_on_disk"],
        "initialblockdownload": data["initialblockdownload"]
    }
    return node_info

@app.get("/api/blocks/latest")
def get_latest_blocks():
    current_height = rpc("getblockcount")

    blocks = []

    for num in range(10):
        blocks.append({
            "height": current_height - num,
            "hash": rpc("getblockhash", [current_height - num])
        })
    return blocks

@app.get("/api/block/{block_hash}")
def get_block_data(block_hash):
    block_data = rpc("getblock", [block_hash])

    return {
        "height": block_data["height"], 
        "time": block_data["time"], 
        "nTx": block_data["nTx"], 
        "size": block_data["size"], 
        "difficulty": block_data["difficulty"]
    }