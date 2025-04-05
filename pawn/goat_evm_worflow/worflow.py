import os

from web3 import Web3
from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from goat_adapters.langchain import get_on_chain_tools
from goat_plugins.uniswap import uniswap, UniswapPluginOptions
from goat_wallets.web3 import Web3EVMWalletClient
from goat_wallets.evm import send_eth
from goat_wallets.crossmint import crossmint

from pawn.agentic_worlflow import AgenticWorkflow


class EVMAgenticWorkflow(AgenticWorkflow):
    
    def _load_env(self):
        self.RPC_PROVIDER_URL = os.getenv("RPC_PROVIDER_URL")
        self.WALLET_PRIVATE_KEY = os.getenv("WALLET_PRIVATE_KEY")
        self.CROSSMINT_API_KEY = os.getenv("CROSSMINT_API_KEY")
        self.UNISWAP_API_KEY = os.getenv("UNISWAP_API_KEY")
        self.UNISWAP_BASE_URL = os.getenv("UNISWAP_BASE_URL", "https://trade-api.gateway.uniswap.org/v1")

    def _compile(self):
        # Initialize the web3 client for EVM chains and wallet client using GOAT framework
        w3 = Web3(Web3.HTTPProvider(self.RPC_PROVIDER_URL))
        wallet_client = Web3EVMWalletClient(w3)
        # Initialize the language model
        model = ChatOpenAI(model="gpt-4o")

        # 1. Agent for swapping tokens on EVM chains using the Uniswap plugin
        def swap_tokens():
            """Swap tokens on EVM chains using Uniswap."""
            tools = get_on_chain_tools(
                wallet=wallet_client,
                plugins=[
                    uniswap(options=UniswapPluginOptions(
                        api_key=self.UNISWAP_API_KEY,
                        base_url=self.UNISWAP_BASE_URL
                    )),
                ],
            )
            return tools

        token_swapping_agent = create_react_agent(
            model=model,
            tools=[swap_tokens],
            name="token_swapping_expert",
            prompt="You are a token swapping expert. Use the swap_tokens tool to exchange tokens on EVM chains."
        )
        
        # 2. Agent for sending and receiving tokens on EVM chains using the send_eth tool
        def send_receive_tokens():
            """Send and receive tokens on EVM chains."""
            tools = get_on_chain_tools(
                wallet=wallet_client,
                plugins=[
                    send_eth()  # Assumes the send_eth tool handles token transfers.
                ],
            )
            return tools

        token_transfer_agent = create_react_agent(
            model=model,
            tools=[send_receive_tokens],
            name="token_transfer_expert",
            prompt="You are a token transfer expert. Use the send_receive_tokens tool to send and receive tokens on EVM chains."
        )

        # 3. Agent for minting NFTs on EVM chains using the Crossmint plugin
        def mint_nft():
            """Mint NFT on EVM chains using Crossmint."""
            crossmint_factory = crossmint(self.CROSSMINT_API_KEY)
            tools = get_on_chain_tools(
                wallet=wallet_client,
                plugins=[crossmint_factory["mint"]()],
            )
            return tools

        nft_minting_agent = create_react_agent(
            model=model,
            tools=[mint_nft],
            name="nft_minting_expert",
            prompt="You are an NFT minting expert. Use the mint_nft tool to mint NFTs on EVM chains."
        )

        # Create the supervisor workflow with the three agents
        workflow = create_supervisor(
            [token_swapping_agent, token_transfer_agent, nft_minting_agent],
            model=model,
            prompt=(
                "You are a team supervisor managing three experts: "
                "for token swaps, use token_swapping_expert; "
                "for token transfers, use token_transfer_expert; "
                "for NFT minting, use nft_minting_expert."
            )
        )
        self.workflow = workflow
        self.app = workflow.compile()
