from .interface import WalletBalanceInput, WalletBalanceOutput


async def run_wallet_check_balance(
    input_data: WalletBalanceInput
) -> WalletBalanceOutput:
    """
    STUB: Real implementation will:
    1. Use MCP + Coinbase AgentKit to query balance
    2. Convert values to USDC if needed
    3. Apply low-balance threshold logic
    """
    raise NotImplementedError("wallet_check_balance skill implementation pending")