import os

from solana.rpc.api import Client as SolanaClient
from goat_wallets.solana import solana
from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from goat_adapters.langchain import get_on_chain_tools
from goat_plugins.jupiter import jupiter, JupiterPluginOptions
from goat_plugins.spl_token import spl_token, SplTokenPluginOptions
from goat_wallets.crossmint import crossmint

from pawn.agentic_worlflow import AgenticWorkflow


class SolanaAgenticWorkflow(AgenticWorkflow):
    
    def _load_env(self):
        self.SOLANA_RPC_ENDPOINT = os.getenv("SOLANA_RPC_ENDPOINT")
        self.SOLANA_WALLET_SEED = os.getenv("SOLANA_WALLET_SEED")
        self.CROSSMINT_API_KEY = os.getenv("CROSSMINT_API_KEY")
        self.JUPITER_API_KEY = os.getenv("JUPITER_API_KEY")
        self.SPL_TOKEN_NETWORK = os.getenv("SPL_TOKEN_NETWORK", "mainnet")
        # You can add environment variables for USDC yield deposit if needed.

    def _compile(self):
        # Initialize Solana client and wallet using GOAT framework
        client = SolanaClient(self.SOLANA_RPC_ENDPOINT)
        wallet = solana(client, self.SOLANA_WALLET_SEED)
        model = ChatOpenAI(model="gpt-4o")

        # Agent 1: Swap tokens in Solana using Jupiter aggregator plugin
        def swap_tokens():
            """Swap tokens on Solana using the Jupiter aggregator."""
            tools = get_on_chain_tools(
                wallet=wallet,
                plugins=[jupiter(JupiterPluginOptions(api_key=self.JUPITER_API_KEY))]
            )
            return tools

        solana_swap_agent = create_react_agent(
            model=model,
            tools=[swap_tokens],
            name="solana_token_swap_expert",
            prompt="You are an expert in swapping tokens on Solana. Use the swap_tokens tool to execute token swaps."
        )

        # Agent 2: Send and receive tokens in Solana using SPL token plugin
        def send_receive_tokens():
            """Send and receive tokens on Solana using SPL token operations."""
            tools = get_on_chain_tools(
                wallet=wallet,
                plugins=[spl_token(SplTokenPluginOptions(network=self.SPL_TOKEN_NETWORK))]
            )
            return tools

        solana_transfer_agent = create_react_agent(
            model=model,
            tools=[send_receive_tokens],
            name="solana_token_transfer_expert",
            prompt="You are an expert in token transfers on Solana. Use the send_receive_tokens tool to send and receive tokens."
        )
        
        # Agent 3: Mint NFT in Solana using Crossmint
        def mint_nft():
            """Mint an NFT on Solana using Crossmint."""
            crossmint_factory = crossmint(self.CROSSMINT_API_KEY)
            tools = get_on_chain_tools(
                wallet=wallet,
                plugins=[crossmint_factory["mint"]()]
            )
            return tools

        solana_nft_agent = create_react_agent(
            model=model,
            tools=[mint_nft],
            name="solana_nft_minting_expert",
            prompt="You are an NFT minting expert on Solana. Use the mint_nft tool to mint NFTs."
        )

        # Agent 4: Provide USDC yield deposit on Solana
        def deposit_usdc_yield():
            """Deposit USDC for yield on Solana.
            
            This tool is a placeholder for a USDC yield deposit operation.
            Replace with actual logic or plugin when available.
            """
            # Here we simulate a yield deposit operation. In a real implementation,
            # you would integrate with a DeFi protocol on Solana.
            tools = get_on_chain_tools(
                wallet=wallet,
                plugins=[lambda: "usdc_yield_deposit_tool"]
            )
            return tools

        solana_yield_agent = create_react_agent(
            model=model,
            tools=[deposit_usdc_yield],
            name="solana_yield_deposit_expert",
            prompt="You are an expert in USDC yield deposit on Solana. Use the deposit_usdc_yield tool to deposit USDC and earn yield."
        )

        # Create the supervisor workflow with all four agents
        workflow = create_supervisor(
            [solana_swap_agent, solana_transfer_agent, solana_nft_agent, solana_yield_agent],
            model=model,
            prompt=(
                "You are a team supervisor managing four experts: "
                "for token swaps on Solana, use solana_token_swap_expert; "
                "for token transfers, use solana_token_transfer_expert; "
                "for NFT minting, use solana_nft_minting_expert; "
                "for USDC yield deposits, use solana_yield_deposit_expert."
            )
        )
        self.workflow = workflow
        self.app = workflow.compile()
