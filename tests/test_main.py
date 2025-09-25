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
        # Aceptar int o float
        assert isinstance(data["price"], (int, float))
        assert data["currency"] == "USD"
    
    def test_get_stock_price_invalid(self):
        """Prueba obtener precio de acción inválida"""
        response = client.get("/stock/INVALID")
        assert response.status_code == 404
        # Verificar que el detalle sea un string no vacío
        detail = response.json()["detail"]
        assert isinstance(detail, str)
        assert len(detail) > 0
    
    def test_get_multiple_stocks(self):
        """Prueba obtener múltiples acciones"""
        response = client.get("/stocks/multiple?symbols=AAPL,GOOGL,INVALID")
        assert response.status_code == 200
        data = response.json()
        
        assert "AAPL" in data
        assert "GOOGL" in data
        assert "INVALID" in data
        assert isinstance(data["AAPL"]["price"], (int, float))
        assert data["INVALID"]["error"] == "Símbolo no encontrado"
    
    def test_get_multiple_stocks_empty(self):
        """Prueba obtener múltiples acciones sin parámetros"""
        response = client.get("/stocks/multiple")
        # FastAPI devuelve 422 cuando falta un parámetro obligatorio
        assert response.status_code == 422
