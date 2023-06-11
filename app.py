from datetime import datetime
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from domain.domain import ServiceType, ServiceProvider, Service, Invoice
from repository.repository import MongoRepository
from fastapi.encoders import jsonable_encoder
from cryptography.hazmat.primitives.asymmetric import rsa

import uvicorn


app = FastAPI()
repo = MongoRepository()


@app.post("/catalogue", response_description="Add new service type", response_model=ServiceType)
async def create_service_type(service_type: ServiceType = Body(...)):
    new_service_type = await repo.add_service_type(service_type)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_service_type)


@app.get("/catalogue", response_description="Get the catalogue of all services")
async def get_catalogue():
    return JSONResponse(status_code=status.HTTP_200_OK, content=await repo.get_catalogue())


@app.post("/providers", response_description="Add new service provider", response_model=ServiceProvider)
async def create_provider(service_provider: ServiceProvider = Body(...)):
    new_service_provider = await repo.add_service_provider(service_provider)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_service_provider)


@app.get("/providers", response_description="Get all providers' brief information")
async def get_providers():
    return JSONResponse(status_code=status.HTTP_200_OK, content=await repo.get_providers_info())


@app.get("/providers/{id}", response_description="Get a single service provider information", response_model=ServiceProvider)
async def get_provider(id: str):
    if (provider := await repo.get_service_provider(id)) is not None:
        return provider
    raise HTTPException(status_code=404, detail=f"Provider {id} not found")


@app.post("/services", response_description="Create a new service", response_model=Service)
async def create_service(service: Service = Body(...)):
    new_service = await repo.add_service(service)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_service)


@app.get("/services", response_description="Get all services between dates")
async def get_services(start_date: str, end_date: str):
    return JSONResponse(status_code=status.HTTP_200_OK, content=await repo.get_services(datetime.strptime(start_date, r"%Y-%m-%dT%H:%M:%S"),
                                                                                        datetime.strptime(end_date, r"%Y-%m-%dT%H:%M:%S")))


@app.get("/services/{id}", response_description="Book the service", response_model=Invoice)
async def book_service(id: str, booked_by: str):
    await repo.update_service(id, booked_by)
    price = await repo.get_service_price(id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(Invoice(price=price["price"])))


@app.post("/invoices", response_description="Finish booking service")
async def verify_invoice(invoice: Invoice = Body(...)):
    return JSONResponse(status_code=status.HTTP_200_OK)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
