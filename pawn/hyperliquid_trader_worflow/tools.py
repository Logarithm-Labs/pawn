import requests
import time

from typing import Dict, List, Type
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool

#
# Schemas
#


class CryptoPriceInput(BaseModel):
    symbol_id: str = Field(
        ..., description="The CoinGecko ID of the cryptocurrency (e.g., 'bitcoin', 'ethereum', 'solana')"
    )


class CryptoPriceOutput(BaseModel):
    result: str = Field(..., description="The price of the cryptocurrency in USD or an error message")


class KlinesInput(BaseModel):
    symbol: str = Field(..., description="The Hyperliquid symbol (e.g., 'BTC', 'ETH', 'SOL')")


class KlinesOutput(BaseModel):
    klines: List[Dict] = Field(
        ..., description="List of 1-day klines with keys: timestamp, open, high, low, close, volume"
    )


#
# Tools
#
class GetCryptoPriceUSD(StructuredTool):
    name: str = "GetCryptoPriceUSD"
    description: str = (
        "Get the current price of any cryptocurrency in USD using CoinGecko API by CoinGecko ID (e.g., 'bitcoin', 'ethereum', 'solana'). Returns a string with the price or an error message."
    )
    args_schema: Type[CryptoPriceInput] = CryptoPriceInput
    base_url: str = Field(default="https://api.coingecko.com/api/v3", description="Base URL for CoinGecko API")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self, symbol_id: str) -> str:
        """Fetches the current price of a cryptocurrency in USD by its CoinGecko ID.

        Args:
        ----
            symbol_id (str): The CoinGecko ID (e.g., 'bitcoin', 'ethereum')

        Returns:
        -------
            str: Price in USD or error message

        """
        symbol_id = symbol_id.lower()  # CoinGecko IDs are lowercase

        try:
            url = f"{self.base_url}/simple/price"
            params = {"ids": symbol_id, "vs_currencies": "usd", "include_last_updated_at": "true"}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            if symbol_id not in data:
                output = CryptoPriceOutput(
                    result=f"Error: Cryptocurrency '{symbol_id}' not found in CoinGecko database"
                )
                return output.result

            price_usd = data[symbol_id]["usd"]
            output = CryptoPriceOutput(result=f"{price_usd}")
            return output.result

        except requests.exceptions.RequestException as e:
            output = CryptoPriceOutput(result=f"Error fetching price for {symbol_id}: {str(e)}")
            return output.result
        except Exception as e:
            output = CryptoPriceOutput(result=f"Unexpected error: {str(e)}")
            return output.result


class GetHyperliquidKlines(StructuredTool):
    name: str = "GetHyperliquidKlines"
    description: str = (
        "Fetches 1-h klines history for a cryptocurrency from Hyperliquid Perp DEX using its symbol (e.g., 'BTC', 'ETH', 'SOL'). Returns a list of dictionaries containing timestamp, open, high, low, close, and volume."
    )
    args_schema: Type[KlinesInput] = KlinesInput
    base_url: str = Field(default="https://api.hyperliquid.xyz", description="Base URL for Hyperliquid API")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self, symbol: str) -> List[Dict]:
        try:
            end_time = int(time.time() * 1000)
            # end time - 300 hours
            start_time = end_time - 300 * 60 * 60 * 1000
            url = f"{self.base_url}/info"
            payload = {
                "type": "candleSnapshot",
                "req": {
                    "coin": symbol.upper(),
                    "interval": "1h",
                    "startTime": start_time,
                    "endTime": end_time,
                },
            }
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            if not data or not isinstance(data, list):
                return [{"error": f"No klines data found for '{symbol}'"}]

            klines = [
                {
                    "timestamp": int(kline["t"] / 1000),
                    "open": float(kline["o"]),
                    "high": float(kline["h"]),
                    "low": float(kline["l"]),
                    "close": float(kline["c"]),
                    "volume": float(kline["v"]),
                }
                for kline in data
            ]
            return klines

        except requests.exceptions.RequestException as e:
            return [{"error": f"Error fetching klines for '{symbol}': {str(e)}"}]
        except Exception as e:
            return [{"error": f"Unexpected error: {str(e)}"}]
