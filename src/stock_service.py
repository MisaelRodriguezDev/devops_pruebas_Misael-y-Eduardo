import random

class StockService:
    def __init__(self):
        # Datos simulados para pruebas
        self.mock_data = {
            "AAPL": 180.50,
            "GOOGL": 135.75,
            "MSFT": 330.20,
            "TSLA": 240.80,
            "AMZN": 145.60
        }
    
    def get_stock_price(self, symbol: str) -> float:
        """
        Obtiene el precio de una acción.
        En un entorno real, aquí se conectaría a una API como Alpha Vantage, Yahoo Finance, etc.
        """
        # Simular llamada a API externa con posibilidad de fallo
        if random.random() < 0.1:  # 10% de probabilidad de error
            raise Exception("Error simulado de conexión")
        
        if symbol in self.mock_data:
            # Simular pequeña variación en el precio
            base_price = self.mock_data[symbol]
            variation = random.uniform(-2.0, 2.0)
            return round(base_price + variation, 2)
        else:
            raise ValueError(f"Símbolo de acción no encontrado: {symbol}")
    
    def get_available_symbols(self) -> list:
        """Retorna la lista de símbolos disponibles"""
        return list(self.mock_data.keys())