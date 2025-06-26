from pasteshare.api import api_v1
from pasteshare.core.application import create_app

app = create_app()

app.include_router(api_v1)