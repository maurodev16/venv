# Api/Modules/__init__.py

from .orders_parser import parse_orders

# Se desejar, você pode expondo esses componentes para fácil importação
__all__ = ["parse_orders"]
