# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A local reimplementation of [mempool.space](https://mempool.space) that connects to a locally running Bitcoin node (`bitcoind`) via JSON-RPC. The goal is to expose Bitcoin mempool and blockchain data through a web interface.

## Commands

### Backend

```bash
# Activate virtual environment (venv is at project root)
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Start the FastAPI dev server (from project root)
uvicorn backend.main:app --reload

# Test RPC connection to bitcoind directly
python backend/rpc.py
```

### Environment Setup

Copy and configure `backend/.env` (not committed):
```
RPC_USER=<bitcoind rpc user>
RPC_PASSWORD=<bitcoind rpc password>
RPC_HOST=127.0.0.1
RPC_PORT=8332
```

## Architecture

```
frontend/           ← not yet implemented
backend/
  main.py           ← FastAPI app; defines HTTP endpoints
  rpc.py            ← Bitcoin JSON-RPC client; all bitcoind calls go through rpc()
```

**Data flow:** HTTP request → FastAPI endpoint (`main.py`) → `rpc(method, params)` in `rpc.py` → local `bitcoind` node over JSON-RPC 1.0.

### RPC Module (`rpc.py`)

`rpc(method, params=[])` is the single generic function for all bitcoind calls. It reads connection config from `.env` at load time. The `dotenv_path` is set to `"backend/.env"` — this assumes the working directory is the project root.

### Adding New Endpoints

1. Import and call `rpc()` from `rpc.py` inside the endpoint handler in `main.py`.
2. Use standard Bitcoin RPC method names (e.g., `getmempoolinfo`, `getrawmempool`, `getrawtransaction`).
