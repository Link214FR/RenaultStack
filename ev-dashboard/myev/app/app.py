from __future__ import with_statement
from fastapi import FastAPI
import uvicorn
import json
import aiohttp
import asyncio
from renault_api.renault_client import RenaultClient
import time


# Init
app = FastAPI(debug=True)

# Data


async def expandCredential(credential):
    print(f"expandCredential : {credential}")
    expandedCredential = [];
    try:
        async with aiohttp.ClientSession() as websession:
            client = RenaultClient(websession=websession, locale='fr_FR')
            await client.session.login(credential['login'], credential['password'])
            accounts = await client.get_person()
            for account in accounts.accounts:
                accountId = account.accountId
                APIaccount = await client.get_api_account(accountId)
                vehiclesResponse = await APIaccount.get_vehicles()
                for vehicleLink in vehiclesResponse.vehicleLinks:
                    expandedCredential.append({**credential, "accountId": accountId, "VIN": vehicleLink.vin})
    except:
        print(f"Invalid credentials for : {credential['login']}")
    print(f"expandCredential : RETURNING")
    return expandedCredential




async def expandCredentials(credentials):
    expandedCredentials = [];
    for credential in credentials:
        expandedCredentials = expandedCredentials + await expandCredential(credential)
    print(f"expandCredentialS : RETURNING : {expandedCredentials}")
    return expandedCredentials

vehicleCredentials = {}
with open("vehicleCredentials.json") as f:
    vehicleCredentials = asyncio.run(expandCredentials(json.load(f)))


async def pullData(locale, credential):
    async with aiohttp.ClientSession() as websession:
        client = RenaultClient(websession=websession, locale=locale)
        await client.session.login(credential['login'], credential['password'])
        #print(f"Accounts: {await client.get_person()}") # List available accounts, make a note of kamereon account id

        account_id = credential["accountId"]
        account = await client.get_api_account(account_id)
        #print(f"Vehicles: {await account.get_vehicles()}") # List available vehicles, make a note of vehicle VIN

        vin = credential["VIN"]
        vehicle = await account.get_api_vehicle(vin)
        cockpitData = (await vehicle.get_cockpit()).raw_data
        batteryData = (await vehicle.get_battery_status()).raw_data
        locationData = (await vehicle.get_location()).raw_data
        #cockpitObject = json.loads(cockpitData)
        #batteryObject = json.loads(batteryData)
        vehicleDataset = dict()
        vehicleDataset.update(cockpitData)
        vehicleDataset.update(batteryData)
        vehicleDataset.update(locationData)
        vehicleDataset.update({"vin": vin})

        #print(f"Cockpit information: {await vehicle.get_cockpit()}")
        #print(f"Battery status information: {await vehicle.get_battery_status()}")i
        return vehicleDataset


# Route
@app.get('/api/v1/vehicle/{vin}')
async def get_vehicle(vin):
    maxRetry = 3
    retryDelay = 15
    retryCount = 0
    credential = [credential for credential in vehicleCredentials if credential["VIN"] == vin ][0]
    while True:
        try:
            vehicleDataset = await pullData('fr_FR', credential)
            return vehicleDataset;
        except Exception as e:
            retryCount += 1
            print(f"Error while fetching Data from Kamereon on try {retryCount}")
            if (retryCount <= 3) :
                print(f"Waiting a {retryDelay} befor retry")
                time.sleep(retryDelay)
                print(f"retrying...")
                continue
            print(f"Too many retries")
            raise e
        break


if __name__ == '__main__':
    print("hello!!!")
    uvicorn.run(app, host="0.0.0.0", port=8181)
    
