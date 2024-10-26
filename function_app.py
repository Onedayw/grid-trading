import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ADMIN)

# Access environment variables
API_KEY = os.getenv('BINANCE_API_KEY', 'default_api_key')
API_SECRET = os.getenv('BINANCE_API_SECRET', 'default_secret_key')

@app.route(route="initStrategy")
def initStrategy(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.route(route="test")
def test(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("This is a test route.")

    from binance.um_futures import UMFutures

    client = UMFutures(key=API_KEY, secret=API_SECRET)

    # get server time
    print(client.time())

    # Get account information
    # print(cm_futures_client.account())

    # Post a new order
    params = {
        'symbol': 'DOGEUSDT',
        'side': 'BUY',
        'type': 'LIMIT',
        'timeInForce': 'GTC',
        'quantity': 50,
        'price': 0.120
    }

    try:
        response = client.new_order(**params)
        logging.info(response)

        if response.status_code == 200:
            return func.HttpResponse("Order placed successfully.")
        else:
            return func.HttpResponse("Error code: {response.status_code}, message: {response.text}, headers: {response.headers}")
    except Exception as e:
        return func.HttpResponse(f"Error: {e}")
