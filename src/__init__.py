# Api/Modules/__init__.py

from .file_handler import router as file_handler_router
from .parse_segments import parse_segments
from .pricat_parser import parse_pricat
from .orders_parser import parse_orders
from .invoic_parser import parse_invoic

# Se desejar, você pode expondo esses componentes para fácil importação
__all__ = ["file_handler_router", "parse_segments", "parse_pricat", "parse_orders", "parse_invoic"]
