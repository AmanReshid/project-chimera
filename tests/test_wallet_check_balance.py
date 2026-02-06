"""
Tests for the wallet_check_balance skill.

Goals:
- Validate input model constraints
- Verify output model structure
- Keep execution contract test failing/skipped until impl.py is done

Run with:  pytest tests/test_wallet_check_balance.py -v
"""

import pytest
from pydantic import ValidationError
from datetime import datetime

from skills.wallet_check_balance.interface import (
    WalletBalanceInput,
    WalletBalanceOutput,
)

# Try to import the real implementation
try:
    from skills.wallet_check_balance.impl import run_wallet_check_balance
except ImportError:
    run_wallet_check_balance = None


# Enable asyncio support
pytestmark = pytest.mark.asyncio


# ────────────────────────────────────────────────
# Input model validation (these should PASS)
# ────────────────────────────────────────────────

def test_wallet_balance_input_minimal_valid():
    """Minimal valid input"""
    inp = WalletBalanceInput(
        agent_id="chimera-eth-fashion-001",
        address="0x1234567890abcdef1234567890abcdef12345678"
    )
    assert inp.agent_id == "chimera-eth-fashion-001"
    assert inp.address.startswith("0x")
    assert inp.primary_currency == "USDC"
    assert inp.include_pending is True


def test_wallet_balance_input_custom_currency():
    """Input with different currency and pending=false"""
    inp = WalletBalanceInput(
        agent_id="agent-wallet-777",
        address="0xabcdef1234567890abcdef1234567890abcdef12",
        primary_currency="ETH",
        include_pending=False
    )
    assert inp.primary_currency == "ETH"
    assert inp.include_pending is False


def test_wallet_balance_input_missing_required():
    """Missing agent_id or address → should fail"""
    with pytest.raises(ValidationError):
        WalletBalanceInput(
            address="0x123..."  # missing agent_id
        )

    with pytest.raises(ValidationError):
        WalletBalanceInput(
            agent_id="agent-123"  # missing address
        )


# ────────────────────────────────────────────────
# Output model structure (these should PASS)
# ────────────────────────────────────────────────

def test_wallet_balance_output_success_shape():
    """Minimal success case"""
    out = WalletBalanceOutput(
        success=True,
        address="0x1234567890abcdef1234567890abcdef12345678",
        confirmed_balance=142.75,
        pending_balance=5.25,
        total_balance=148.0,
        currency="USDC",
        low_balance_warning=False
    )
    assert out.success is True
    assert out.total_balance == 148.0
    assert out.low_balance_warning is False
    assert isinstance(out.last_checked, datetime)


def test_wallet_balance_output_low_balance():
    """Low balance warning case"""
    out = WalletBalanceOutput(
        success=True,
        address="0xabc...",
        confirmed_balance=1.25,
        total_balance=1.25,
        currency="USDC",
        low_balance_warning=True
    )
    assert out.low_balance_warning is True


def test_wallet_balance_output_failure_shape():
    """Failure case shape"""
    out = WalletBalanceOutput(
        success=False,
        address="0xabc...",
        error_message="Wallet query timeout"
    )
    assert out.success is False
    assert out.error_message is not None


# ────────────────────────────────────────────────
# Execution contract (should FAIL right now)
# ────────────────────────────────────────────────

@pytest.mark.skipif(
    run_wallet_check_balance is None,
    reason="run_wallet_check_balance is not implemented yet"
)
async def test_wallet_check_balance_execution_contract():
    """
    Defines the full contract the skill must satisfy.
    Should fail until the stub is replaced with real logic.
    """
    input_data = WalletBalanceInput(
        agent_id="test-agent-wallet",
        address="0x1234567890abcdef1234567890abcdef12345678",
        primary_currency="USDC",
        include_pending=True
    )

    result = await run_wallet_check_balance(input_data)

    assert isinstance(result, WalletBalanceOutput)
    assert isinstance(result.success, bool)
    assert result.address == input_data.address
    assert isinstance(result.confirmed_balance, (int, float))
    assert result.confirmed_balance >= 0
    assert isinstance(result.total_balance, (int, float))
    assert result.total_balance >= result.confirmed_balance
    assert isinstance(result.currency, str)
    assert isinstance(result.last_checked, datetime)

    if result.success:
        assert result.error_message is None
    else:
        assert result.error_message is not None