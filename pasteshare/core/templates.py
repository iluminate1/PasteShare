from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader

from pasteshare.core.constants import TEMPLATE_DIR

TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=True,
    enable_async=True,
)
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))
