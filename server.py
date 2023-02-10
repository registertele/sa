from fastapi import FastAPI
import requests
import json
import multiprocessing
import asyncio


app = FastAPI()

@app.get("/get_phone/{country}/{service}")
async def get_phone(country: str, service: str):
    url = f'https://sms-acktiwator.ru/api/getnumber/21bfd5f290e58f628155cea2a90f00b1213a?id={service}&code={country}'
    response = requests.get(url)
    result = json.loads(response.text)
    if "number" in result:
        if result["number"] != "":
            return {"phone" : result["number"], "id" : result["id"]}
        else:
            return {"phone" : ""}
    else:
        return {"phone" : ""}


@app.get("/get_code/{id}")
async def get_code(id: str):
    url = f'https://sms-acktiwator.ru/api/getlatestcode/21bfd5f290e58f628155cea2a90f00b1213a?id={id}'
    response = requests.get(url)

    if response.text != "":
        return {"code" : response.text}
    else:
        return {"code" : ""}

@app.get("/get_balance")
async def get_balance():
    url = 'https://sms-acktiwator.ru/api/getbalance/21bfd5f290e58f628155cea2a90f00b1213a'
    response = requests.get(url)
    result = json.loads(response.text)
    return {"balance" : result}

@app.get("/get_services")
async def get_services():
    url = 'https://sms-acktiwator.ru/api/getservices/21bfd5f290e58f628155cea2a90f00b1213a'
    response = requests.get(url)
    result = json.loads(response.text)
    return {"services" : result}

@app.get("/get_countries")
async def get_countries():
    url = 'https://sms-acktiwator.ru/api/getcountries/21bfd5f290e58f628155cea2a90f00b1213a'
    response = requests.get(url)
    result = json.loads(response.text)
    return {"countries" : result}
    
@app.get("/cancel_order/{id}")
async def cancel_order(id: str):
    url = f'https://sms-acktiwator.ru/api/cancel/21bfd5f290e58f628155cea2a90f00b1213a?id={id}'
    response = requests.get(url)
    result = json.loads(response.text)
    return result

def main():
    multiprocessing.freeze_support()
    from hypercorn.asyncio import serve
    from hypercorn.config import Config
    config = Config()
    config.bind = ["0.0.0.0:8080"]
    asyncio.run(serve(app, config))

if __name__ == "__main__":
    main()