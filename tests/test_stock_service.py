import pytest
from src.stock_service import StockService
from unittest.mock import patch, MagicMock

class TestStockService:
    def setup_method(self):
        self.service = StockService()
    
    def test_get_stock_price_valid_symbol(self):
        """Prueba obtener precio de símbolo válido"""
        price = self.service.get_stock_price("AAPL")
        assert isinstance(price, float)
        assert price > 0
    
    def test_get_stock_price_invalid_symbol(self):
        """Prueba obtener precio de símbolo inválido"""
        with pytest.raises(ValueError):
            self.service.get_stock_price("INVALID")
    
    @patch('random.random')
    def test_get_stock_price_connection_error(self, mock_random):
        """Prueba error de conexión simulado"""
        mock_random.return_value = 0.05  # Forzar error (10% probabilidad)
        
        with pytest.raises(Exception) as exc_info:
            self.service.get_stock_price("AAPL")
        assert "Error simulado" in str(exc_info.value)
    
    def test_get_available_symbols(self):
        """Prueba obtener lista de símbolos disponibles"""
        symbols = self.service.get_available_symbols()
        assert isinstance(symbols, list)
        assert len(symbols) > 0
        assert "AAPL" in symbols