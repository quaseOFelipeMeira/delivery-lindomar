from fastapi import FastAPI
from core.database import engine
from core.models import Base
from routers import account, login, product

# from routers import product, sale, seller, login

app = FastAPI(
    title="Delivery API",
    description="api to serve a mobile delivery app",
    # terms_of_service="http://google.com",
    # contact={
    #     "Developer name": "Felipe Meira",
    #     "email": "felipecmeira2004@gmail.com",
    # },
    # license_info={
    #     "name": "XZY",
    #     "url": "http://google.com",
    # },
    # docs_url="/docs",
    redoc_url=None,
)

app.include_router(account.router)
app.include_router(login.router)
app.include_router(product.router)

Base.metadata.create_all(engine)

# uvicorn main:app --reload --port 8000
