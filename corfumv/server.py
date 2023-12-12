from fastapi import FastAPI
from CorfuMV.routers import exp_router, md_router


app = FastAPI()


app.include_router(router=exp_router)
app.include_router(router=md_router)