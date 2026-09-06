"""
Example usage of the transaction-analysis skill with SpoonReactSkill agent.
"""

from spoon_ai.agents import SpoonReactSkill
from spoon_ai.chat import ChatBot
import asyncio


class TransactionAnalysisAgent(SpoonReactSkill):
    """
    A specialized agent for blockchain transaction analysis.
    Automatically loads and uses transaction-analysis skill scripts.
    """

    def __init__(self, **kwargs):
        kwargs.setdefault('name', 'transaction_analysis_agent')
        kwargs.setdefault('description', 'AI agent for analyzing blockchain transactions')
        kwargs.setdefault('skill_paths', ['.agent/skills'])
        kwargs.setdefault('scripts_enabled', True)
        kwargs.setdefault('auto_trigger_skills', True)
        kwargs.setdefault('max_steps', 10)
        super().__init__(**kwargs)

    async def initialize(self):
        """Initialize and activate the transaction-analysis skill."""
        await super().initialize()

        # Activate the transaction-analysis skill
        if "transaction-analysis" in self.list_skills():
            await self.activate_skill("transaction-analysis")
            print("✓ Transaction Analysis skill activated")
        else:
            print("⚠ Transaction Analysis skill not found. Please check skill_paths.")


async def example_1_basic_analysis():
    """Example 1: Basic transaction history analysis."""
    print("\n" + "="*60)
    print("Example 1: Basic Transaction History Analysis")
    print("="*60)

    agent = TransactionAnalysisAgent(
        llm=ChatBot(llm_provider="openai", model_name="gpt-4o")
    )
    await agent.initialize()

    result = await agent.run(
        "Analyze the transaction history for address 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb on Ethereum"
    )
    print(result)


async def example_2_token_analysis():
    """Example 2: Token transfer analysis."""
    print("\n" + "="*60)
    print("Example 2: Token Transfer Analysis")
    print("="*60)

    agent = TransactionAnalysisAgent(
        llm=ChatBot(llm_provider="openai", model_name="gpt-4o")
    )
    await agent.initialize()

    result = await agent.run(
        "Show me all USDC token transfers for 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
    )
    print(result)


async def example_3_pattern_detection():
    """Example 3: Pattern detection."""
    print("\n" + "="*60)
    print("Example 3: Pattern Detection")
    print("="*60)

    agent = TransactionAnalysisAgent(
        llm=ChatBot(llm_provider="openai", model_name="gpt-4o")
    )
    await agent.initialize()

    result = await agent.run(
        "Detect any unusual patterns or anomalies in transactions for 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
    )
    print(result)


async def example_4_gas_analysis():
    """Example 4: Gas usage analysis."""
    print("\n" + "="*60)
    print("Example 4: Gas Usage Analysis")
    print("="*60)

    agent = TransactionAnalysisAgent(
        llm=ChatBot(llm_provider="openai", model_name="gpt-4o")
    )
    await agent.initialize()

    result = await agent.run(
        "Analyze gas usage and provide optimization recommendations for 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
    )
    print(result)


async def example_5_fund_flow():
    """Example 5: Fund flow tracking."""
    print("\n" + "="*60)
    print("Example 5: Fund Flow Tracking")
    print("="*60)

    agent = TransactionAnalysisAgent(
        llm=ChatBot(llm_provider="openai", model_name="gpt-4o")
    )
    await agent.initialize()

    result = await agent.run(
        "Track fund flows for 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb over the last 30 days"
    )
    print(result)


async def example_6_counterparty_analysis():
    """Example 6: Counterparty analysis."""
    print("\n" + "="*60)
    print("Example 6: Counterparty Analysis")
    print("="*60)

    agent = TransactionAnalysisAgent(
        llm=ChatBot(llm_provider="openai", model_name="gpt-4o")
    )
    await agent.initialize()

    result = await agent.run(
        "Who are the most frequent counterparties for 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb?"
    )
    print(result)


async def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("Transaction Analysis Skill - Example Usage")
    print("="*60)

    # Run examples (uncomment the ones you want to test)
    await example_1_basic_analysis()
    # await example_2_token_analysis()
    # await example_3_pattern_detection()
    # await example_4_gas_analysis()
    # await example_5_fund_flow()
    # await example_6_counterparty_analysis()


if __name__ == "__main__":
    asyncio.run(main())
