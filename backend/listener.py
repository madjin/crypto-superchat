import os
from dotenv import load_dotenv
import asyncio
import aiohttp
from typing import Any, Callable, Dict

load_dotenv()

AI16Z_MINT = os.getenv('AI16Z_MINT', 'HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC')
HELIUS_BASE = 'https://api.helius.xyz/v0'
RPC_BASE = 'https://mainnet.helius-rpc.com'
MEMO_PID = 'MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr'

API_KEY = os.getenv('HELIUS_API_KEY', '')
PRIZE_WALLET = os.getenv('PRIZE_WALLET_ADDRESS', '')

async def _fetch_json(session: aiohttp.ClientSession, url: str):
    async with session.get(url, timeout=30) as r:
        r.raise_for_status()
        return await r.json()

async def _post_json(session: aiohttp.ClientSession, url: str, payload: Dict[str, Any]):
    async with session.post(url, json=payload, timeout=30) as r:
        r.raise_for_status()
        return await r.json()

async def _get_ata(session: aiohttp.ClientSession, wallet: str) -> str | None:
    payload = {"jsonrpc": "2.0", "id": 1, "method": "getTokenAccountsByOwner", "params": [wallet, {"mint": AI16Z_MINT}, {"encoding": "jsonParsed"}]}
    data = await _post_json(session, f"{RPC_BASE}/?api-key={API_KEY}", payload)
    value = data.get('result', {}).get('value', [])
    return value[0]['pubkey'] if value else None

async def start_listener_task(broadcast: Callable[[Dict[str, Any]], Any]):
    if not (API_KEY and PRIZE_WALLET):
        return
    before = None
    ata = None
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                if ata is None:
                    ata = await _get_ata(session, PRIZE_WALLET)
                base = f"{HELIUS_BASE}/addresses/{PRIZE_WALLET}/transactions?api-key={API_KEY}&limit=50"
                url = f"{base}&before={before}" if before else base
                page = await _fetch_json(session, url)
                for tx in page or []:
                    # filter for AI16Z token transfers to our wallet or ATA
                    for t in tx.get('tokenTransfers', []):
                        if t.get('mint') == AI16Z_MINT and (t.get('toUserAccount') in {PRIZE_WALLET, ata}):
                            memo = None
                            if isinstance(tx.get('memos'), list) and tx['memos']:
                                memo = str(tx['memos'][0]).strip()
                            elif isinstance(tx.get('memo'), str):
                                memo = tx['memo'].strip()
                            if memo:
                                await broadcast({
                                    'type': 'memo',
                                    'memo': memo,
                                    'amount': t.get('tokenAmount'),
                                    'signature': tx.get('signature'),
                                    'from': t.get('fromUserAccount'),
                                })
                            break
                before = (page[-1]['signature'] if page else before)
                await asyncio.sleep(3)
            except Exception:
                await asyncio.sleep(5)