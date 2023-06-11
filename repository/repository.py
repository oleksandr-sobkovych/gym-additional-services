import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from datetime import datetime
from domain.domain import ServiceType, ServiceProvider, Service, PyObjectId


class MongoRepository:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017,localhost:28017,localhost:29017/?replicaSet=services_set")
        self.services_db = self.client.services
        self.catalogue = self.services_db.catalogue
        self.services = self.services_db.services
        self.providers = self.services_db.providers

    async def add_service_type(self, service_type: ServiceType):
        
        new_type = await self.catalogue.insert_one(jsonable_encoder(service_type))
        return await self.catalogue.find_one({"_id": new_type.inserted_id})

    async def get_catalogue(self):
        return await self.catalogue.find().to_list(1000)

    async def add_service_provider(self, service_provider: ServiceProvider):
        
        for service_type in service_provider.types:
            if (existing_type := await self.catalogue.find_one({"type_name": service_type.type_name,
                                                                "type_descr": service_type.type_descr})) is not None:
                service_type.id = existing_type["_id"]
            else:
                await self.add_service_type(service_type)
        new_provider = await self.providers.insert_one(jsonable_encoder(service_provider))
        return await self.providers.find_one({"_id": new_provider.inserted_id})

    async def get_service_provider(self, id: str):
        return await self.providers.find_one({"_id": id})

    async def get_providers_info(self):
        return await self.providers.find({}, {"provider_name", "email", "types"}).to_list(1000)

    async def add_service(self, service: Service):
        
        if (existing_type := await self.catalogue.find_one({"type_name": service.type.type_name,
                                                            "type_descr": service.type.type_descr})) is not None:
            service.type.id = existing_type["_id"]
        else:
            raise HTTPException(status_code=400, detail=f"No {service.type} service type allowed")

        if (provider := await self.providers.find_one({"_id": str(service.provider_id)})) is None:
            raise HTTPException(status_code=400, detail=f"No {service.provider_id} provider found")

        if jsonable_encoder(service.type) not in provider["types"]:
            raise HTTPException(status_code=400, detail=f"Provider {service.provider_id} cannot provide this service type")

        new_service = await self.services.insert_one(jsonable_encoder(service))
        return await self.services.find_one({"_id": new_service.inserted_id})

    async def get_services(self, start_date: datetime, end_date: datetime):
        if end_date < start_date:
            raise HTTPException(status_code=400, detail="Datetimes are invalid")
        return await self.services.find({"start": {"$gte": jsonable_encoder(start_date)}, "end": {"$lte": jsonable_encoder(end_date)}}).to_list(1000)

    async def update_service(self, id: str, client_id: str):
        
        await self.services.update_one({"_id": id}, {"$set": {"booked_by": client_id}})

    async def get_service_price(self, id: str):
        return await self.services.find_one({"_id": id}, {"price"})

    async def close(self):
        self.client.close()
