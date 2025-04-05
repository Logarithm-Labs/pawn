import os

from pprint import pprint
from pawn.hyperliquid_trader_worflow import HyperliquidWorkflow


if __name__ == "__main__":
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    assert OPENAI_API_KEY, "Please set the OPENAI_API_KEY environment variable."

    workflow: HyperliquidWorkflow = HyperliquidWorkflow()

    result = workflow.invoke('What is bitcoin price now?')
    pprint(result)

    result = workflow.invoke('Send me HYPE klines history for last 7 days?')
    pprint(result)

    result = workflow.invoke('Make a trade for 0.1 BTC')
    pprint(result)
