import datetime
import json
import time
from . import get_db_connection
from web3 import Web3, WebsocketProvider
from config import API_KEY


API_KEY = API_KEY

web3 = Web3(WebsocketProvider(f'wss://mainnet.infura.io/ws/v3/{API_KEY}'))


def get_timestamp(timestamp):
    timestamp_datetime = datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)

    local_timezone = datetime.now().astimezone().tzinfo
    timestamp_local = timestamp_datetime.astimezone(local_timezone)
    return timestamp_local


def insert_transaction_data(tx_hash, block_number, timestamp, 
                            sender, receiver, value, 
                            gas_price, gas_limit, nonce, status):
    try:
        conn = get_db_connection.get_db_conn()
        cursor = conn.cursor()
        cursor.execute('''INSERT OR IGNORE INTO transactions (
                            transaction_hash, block_number, 
                            timestamp, sender, receiver, 
                            value, gas_price, gas_limit, 
                            nonce, status
                        ) VALUES (?, ?, 
                        ?, ?, ?, 
                        ?, ?, ?, 
                        ?, ?)''',
                        (tx_hash.hex(), block_number, timestamp, 
                        sender, receiver, value, 
                        gas_price, gas_limit, nonce, status))
        conn.commit()
    
    except Exception as e:
        print(e)

    finally:
        conn.close()


def monitor_transactions(account_address, monitoring_enabled):
    
    if not web3.is_address(account_address):
        return False
    else:
        while monitoring_enabled:
            try:        
                latest_block = web3.eth.block_number

                for block_number in range(latest_block - 1, latest_block + 1):
                    block = web3.eth.get_block(block_number)
                    if block:
                        for tx_hash in block['transactions']:
                            tx_receipt = web3.eth.get_transaction_receipt(tx_hash)

                            if tx_receipt:
                                block_number = tx_receipt['blockNumber']
                                block = web3.eth.get_block(block_number)
                                timestamp = block['timestamp']
                                
                                transaction = web3.eth.get_transaction(tx_hash)
                                sender = transaction['from']
                                receiver = transaction['to']

                                if sender or receiver is not None:
                                    if account_address.lower() in [sender.lower(), receiver.lower()]:
                                        block_number = tx_receipt['blockNumber']
                                        timestamp = web3.eth.get_block(block_number)['timestamp']
                                        
                                        insert_transaction_data(
                                            tx_hash.hex(),
                                            block_number,
                                            get_timestamp(timestamp),
                                            transaction['from'],
                                            transaction['to'],
                                            transaction['value'],
                                            transaction['gasPrice'],
                                            transaction['gas'],
                                            transaction['nonce'],
                                            tx_receipt['status']
                                        )

            except Exception as e:
                print('Error occurred:', str(e))

            time.sleep(10)
            


def get_transaction_data(address):
    try:
        conn = get_db_connection.get_db_conn()
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM transactions
                        WHERE sender = ? OR receiver = ?
                        ORDER BY block_number DESC''', (address, address))
        transactions = cursor.fetchall()

        if transactions:
            
            transaction_list = []
            
            for transaction in transactions:

                transaction_obj = {
                    "transaction_hash": transaction[0],
                    "block_number": transaction[1],
                    "timestamp": transaction[2],
                    "sender": transaction[3],
                    "receiver": transaction[4],
                    "value": transaction[5],
                    "gas_price": transaction[6],
                    "gas_limit": transaction[7],
                    "nonce": transaction[8],
                    "status": transaction[9]
                }

                transaction_list.append(transaction_obj)

            response = {
                "address": address,
                "transactions": transaction_list
            }

            return json.dumps(response)
        else:
            return json.dumps({"message": "No transactions found for the address"})        
        
    except Exception as e:
        return json.dumps({"message": e})
    