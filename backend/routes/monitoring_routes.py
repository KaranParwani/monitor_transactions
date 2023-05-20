from fastapi import status, APIRouter
from fastapi.responses import JSONResponse

from services.monitoring import get_transaction_data, monitor_transactions

transaction_router = APIRouter()

monitoring_enabled = False

@transaction_router.post('/start/{transaction_address}')
def start_processing(transaction_address):
    global monitoring_enabled
    
    print('was called')
    if not monitoring_enabled:
        monitoring_enabled = True
        response = monitor_transactions(transaction_address, monitoring_enabled)
        if not response:
            return JSONResponse({'message': f'Invalid account address : {transaction_address}'})
    else:
        response = monitor_transactions(transaction_address, monitoring_enabled)
        if not response:
            return JSONResponse({'message': f'Invalid account address : {transaction_address}'})
        
        
@transaction_router.get('/stop')
def stop_processing():
    global monitoring_enabled

    if monitoring_enabled:
        account_number = None
        monitoring_enabled = False
        # print('called')
        return monitor_transactions(account_number, monitoring_enabled)        


@transaction_router.get('/seen/{transaction_address}')
def monitored_transactions(transaction_address):
    return get_transaction_data(transaction_address)


