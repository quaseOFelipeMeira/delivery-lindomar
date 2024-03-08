from fastapi import FastAPI
from core.database import engine
from core.models import Base
from routers import v1

description = """

### API METHODS 
#### Account
* Login
* Get current account
* Create user account
* Create transport company account

#### Order
* Create order
* Get orders
* Increase order status
* Decrease order status

#### Product
* Create product
* Get products
* Update products
* Delete products
"""

app = FastAPI(
    title="Delivery API",
    # description="api to serve a mobile delivery app",
    version="1.0.0 - Launching",
    contact={
        "name": "Felipe Meira",
        "email": "felipecmeira2004@gmail.com",
        "url": "https://github.com/quaseOFelipeMeira",
    },
    docs_url="/docs",
    redoc_url=None,
    description=description,
)

app.include_router(v1.router)

Base.metadata.create_all(engine)

# uvicorn main:app --reload --port 8000

# To do:
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
