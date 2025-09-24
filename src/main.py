from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from stock_service import StockService
import uvicorn

app = FastAPI(title="Stock Market API", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

stock_service = StockService()

@app.get("/")
async def root():
    return {"message": "Stock Market API - Práctica 3 DevOps"}

@app.get("/stock/{symbol}")
async def get_stock_price(symbol: str):
    """Obtiene el precio actual de una acción"""
    try:
        price = stock_service.get_stock_price(symbol.upper())
        return {
            "symbol": symbol.upper(),
            "price": price,
            "currency": "USD"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.get("/stocks/multiple")
async def get_multiple_stocks(symbols: str):
    """Obtiene precios de múltiples acciones"""
    try:
        symbol_list = [s.strip().upper() for s in symbols.split(",")]
        results = {}
        
        for symbol in symbol_list:
            try:
                price = stock_service.get_stock_price(symbol)
                results[symbol] = {
                    "price": price,
                    "currency": "USD"
                }
            except ValueError:
                results[symbol] = {"error": "Símbolo no encontrado"}
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)