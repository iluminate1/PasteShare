from pasteshare.api import api_v1
from pasteshare.core.application import create_app
from pasteshare.web import router as web_router

app = create_app()

app.include_router(api_v1)
app.include_router(web_router)
