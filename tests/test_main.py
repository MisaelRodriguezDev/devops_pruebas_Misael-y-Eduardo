import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

class TestStockAPI:
    def test_root_endpoint(self):
        """Prueba el endpoint raíz"""
        response = client.get("/")
        assert response.status_code == 200
        assert "Stock Market API" in response.json()["message"]
    
    def test_get_stock_price_valid(self):
        """Prueba obtener precio de acción válida"""
        response = client.get("/stock/AAPL")
        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "AAPL"
        assert isinstance(data["price"], float)
        assert data["currency"] == "USD"
    
    def test_get_stock_price_invalid(self):
        """Prueba obtener precio de acción inválida"""
        response = client.get("/stock/INVALID")
        assert response.status_code == 404
        assert "Símbolo no encontrado" in response.json()["detail"]
    
    def test_get_multiple_stocks(self):
        """Prueba obtener múltiples acciones"""
        response = client.get("/stocks/multiple?symbols=AAPL,GOOGL,INVALID")
        assert response.status_code == 200
        data = response.json()
        
        assert "AAPL" in data
        assert "GOOGL" in data
        assert "INVALID" in data
        assert isinstance(data["AAPL"]["price"], float)
        assert data["INVALID"]["error"] == "Símbolo no encontrado"
    
    def test_get_multiple_stocks_empty(self):
        """Prueba obtener múltiples acciones sin parámetros"""
        response = client.get("/stocks/multiple")
        assert response.status_code == 500