from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class WalletBalanceInput(BaseModel):
    """Parameters for checking an agent's wallet balance"""
    agent_id: str = Field(..., min_length=3, description="Unique agent identifier")
    address: str = Field(..., description="The agent's wallet address (checksummed)")
    primary_currency: str = Field("USDC", description="Currency to report in (usually USDC)")
    include_pending: bool = Field(True, description="Include pending/unconfirmed amounts")


class WalletBalanceOutput(BaseModel):
    """Current wallet balance information"""
    success: bool
    address: str
    confirmed_balance: float = Field(..., ge=0, description="Confirmed / settled balance")
    pending_balance: Optional[float] = Field(None, description="Pending / unconfirmed amount")
    total_balance: float = Field(..., ge=0, description="confirmed + pending")
    currency: str = Field("USDC", description="Reported currency")
    last_checked: datetime = Field(default_factory=datetime.utcnow)
    low_balance_warning: bool = Field(False, description="True if below safe threshold")
    error_message: Optional[str] = None
    metadata: dict = Field(default_factory=dict)  # chain, token_contract, etc.