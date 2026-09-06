"""
Portfolio Manager Module
Inspired by TradingAgents Portfolio Manager
Handles trade execution, position tracking, and portfolio optimization
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"
    CLOSED = "closed"


@dataclass
class Order:
    """Trade order"""
    order_id: str
    asset: str
    direction: str  # "buy" or "sell"
    size: float
    entry_price: float
    stop_loss: float
    take_profit: float
    risk_percent: float
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    executed_at: Optional[datetime] = None
    exit_price: Optional[float] = None
    profit_loss: Optional[float] = None


@dataclass
class Position:
    """Open position"""
    asset: str
    direction: str
    size: float
    entry_price: float
    current_price: float
    stop_loss: float
    take_profit: float
    unrealized_pnl: float
    risk_amount: float
    opened_at: datetime
    age_hours: float = 0.0


@dataclass
class PortfolioState:
    """Complete portfolio state"""
    cash_balance: float
    total_equity: float
    open_positions: List[Position]
    day_pnl: float
    total_pnl: float
    exposure_percent: float
    margin_used: float
    free_margin: float
    risk_exposure: float


class PortfolioManager:
    """
    Portfolio Manager inspired by TradingAgents

    Responsibilities:
    - Order approval/rejection
    - Position sizing optimization
    - Risk exposure monitoring
    - Trade execution simulation
    - Portfolio rebalancing
    """

    def __init__(
        self,
        initial_capital: float = 10000.0,
        max_risk_per_trade: float = 2.0,
        max_portfolio_exposure: float = 50.0,
        max_correlated_exposure: float = 30.0,
        min_cash_buffer: float = 20.0
    ):
        self.initial_capital = initial_capital
        self.cash_balance = initial_capital
        self.equity = initial_capital

        # Risk parameters
        self.max_risk_per_trade = max_risk_per_trade
        self.max_portfolio_exposure = max_portfolio_exposure
        self.max_correlated_exposure = max_correlated_exposure
        self.min_cash_buffer = min_cash_buffer

        # State
        self.open_positions: Dict[str, Position] = {}
        self.order_history: List[Order] = []
        self.daily_pnl = 0.0
        self.total_pnl = 0.0

        # Asset correlations for risk management
        self.asset_classes = {
            "XAU": "precious_metal",
            "XAG": "precious_metal",
            "BTC": "crypto",
            "ETH": "crypto",
            "XPD": "precious_metal",
            "XPT": "precious_metal",
            "HG": "industrial_metal"
        }

    def calculate_position_size(
        self,
        asset: str,
        entry_price: float,
        stop_loss: float,
        risk_percent: Optional[float] = None
    ) -> Dict:
        """
        Calculate optimal position size with portfolio constraints

        Returns:
            {
                "approved": bool,
                "size": float,
                "risk_amount": float,
                "reason": str
            }
        """
        risk_pct = risk_percent or self.max_risk_per_trade

        # Check if risk percent exceeds limit
        if risk_pct > self.max_risk_per_trade:
            return {
                "approved": False,
                "size": 0,
                "risk_amount": 0,
                "reason": f"Risk {risk_pct}% exceeds max {self.max_risk_per_trade}%"
            }

        # Calculate risk amount
        risk_amount = self.equity * (risk_pct / 100)
        stop_distance = abs(entry_price - stop_loss)

        if stop_distance == 0:
            return {
                "approved": False,
                "size": 0,
                "risk_amount": 0,
                "reason": "Invalid stop loss (zero distance)"
            }

        # Calculate position size
        position_size = risk_amount / stop_distance
        notional_value = position_size * entry_price

        # Check exposure limits
        current_exposure = sum(
            pos.size * pos.current_price
            for pos in self.open_positions.values()
        )
        new_exposure = current_exposure + notional_value
        exposure_pct = (new_exposure / self.equity) * 100

        if exposure_pct > self.max_portfolio_exposure:
            return {
                "approved": False,
                "size": 0,
                "risk_amount": 0,
                "reason": f"Would exceed max exposure {self.max_portfolio_exposure}%"
            }

        # Check cash buffer
        required_margin = notional_value * 0.05  # Assume 5% margin
        if (self.cash_balance - required_margin) < (self.equity * self.min_cash_buffer / 100):
            return {
                "approved": False,
                "size": 0,
                "risk_amount": 0,
                "reason": "Insufficient cash buffer"
            }

        # Check correlated exposure
        asset_class = self.asset_classes.get(asset, "unknown")
        correlated_exposure = sum(
            pos.size * pos.current_price
            for pos in self.open_positions.values()
            if self.asset_classes.get(pos.asset) == asset_class
        )
        correlated_pct = ((correlated_exposure + notional_value) / self.equity) * 100

        if correlated_pct > self.max_correlated_exposure:
            return {
                "approved": False,
                "size": 0,
                "risk_amount": 0,
                "reason": f"Would exceed correlated exposure for {asset_class}"
            }

        return {
            "approved": True,
            "size": round(position_size, 2),
            "risk_amount": round(risk_amount, 2),
            "notional": round(notional_value, 2),
            "margin_required": round(required_margin, 2),
            "reason": "Position approved"
        }

    def approve_order(self, order: Order) -> Dict:
        """
        Review and approve/reject order (TradingAgents Portfolio Manager role)

        Evaluates:
        - Risk limits
        - Portfolio constraints
        - Market conditions
        """
        # Calculate position size
        sizing = self.calculate_position_size(
            order.asset,
            order.entry_price,
            order.stop_loss,
            order.risk_percent
        )

        if not sizing["approved"]:
            order.status = OrderStatus.REJECTED
            return {
                "approved": False,
                "order_id": order.order_id,
                "reason": sizing["reason"]
            }

        # Update order size to approved size
        order.size = sizing["size"]
        order.status = OrderStatus.APPROVED

        return {
            "approved": True,
            "order_id": order.order_id,
            "size": sizing["size"],
            "risk_amount": sizing["risk_amount"],
            "margin_required": sizing["margin_required"],
            "reason": "Order approved by Portfolio Manager"
        }

    def execute_order(self, order: Order, current_price: float) -> Dict:
        """Execute approved order"""
        if order.status != OrderStatus.APPROVED:
            return {
                "success": False,
                "reason": f"Order not approved (status: {order.status.value})"
            }

        # Create position
        position = Position(
            asset=order.asset,
            direction=order.direction,
            size=order.size,
            entry_price=current_price,
            current_price=current_price,
            stop_loss=order.stop_loss,
            take_profit=order.take_profit,
            unrealized_pnl=0.0,
            risk_amount=order.size * abs(order.entry_price - order.stop_loss),
            opened_at=datetime.now()
        )

        # Update state
        self.open_positions[order.asset] = position
        margin_required = order.size * current_price * 0.05
        self.cash_balance -= margin_required

        order.status = OrderStatus.EXECUTED
        order.executed_at = datetime.now()
        self.order_history.append(order)

        return {
            "success": True,
            "position": position,
            "cash_remaining": self.cash_balance,
            "message": f"Executed {order.direction} {order.size} {order.asset} at ${current_price}"
        }

    def update_positions(self, current_prices: Dict[str, float]) -> PortfolioState:
        """Update all positions with current prices"""
        total_unrealized = 0.0
        total_margin = 0.0

        for asset, position in self.open_positions.items():
            if asset in current_prices:
                position.current_price = current_prices[asset]

                # Calculate unrealized P&L
                if position.direction == "buy":
                    position.unrealized_pnl = (
                        position.current_price - position.entry_price
                    ) * position.size
                else:
                    position.unrealized_pnl = (
                        position.entry_price - position.current_price
                    ) * position.size

                # Update age
                position.age_hours = (
                    datetime.now() - position.opened_at
                ).total_seconds() / 3600

                total_unrealized += position.unrealized_pnl
                total_margin += position.size * position.current_price * 0.05

        # Update equity
        self.equity = self.initial_capital + self.total_pnl + total_unrealized

        # Calculate exposure
        exposure = sum(
            pos.size * pos.current_price
            for pos in self.open_positions.values()
        )
        exposure_pct = (exposure / self.equity) * 100 if self.equity > 0 else 0

        # Risk exposure
        total_risk = sum(
            pos.risk_amount for pos in self.open_positions.values()
        )
        risk_pct = (total_risk / self.equity) * 100 if self.equity > 0 else 0

        return PortfolioState(
            cash_balance=self.cash_balance,
            total_equity=self.equity,
            open_positions=list(self.open_positions.values()),
            day_pnl=self.daily_pnl,
            total_pnl=self.total_pnl + total_unrealized,
            exposure_percent=exposure_pct,
            margin_used=total_margin,
            free_margin=self.cash_balance,
            risk_exposure=risk_pct
        )

    def close_position(
        self,
        asset: str,
        exit_price: float,
        reason: str = "manual"
    ) -> Dict:
        """Close open position"""
        if asset not in self.open_positions:
            return {"success": False, "reason": "No open position for asset"}

        position = self.open_positions[asset]

        # Calculate realized P&L
        if position.direction == "buy":
            realized_pnl = (exit_price - position.entry_price) * position.size
        else:
            realized_pnl = (position.entry_price - exit_price) * position.size

        # Update state
        margin_released = position.size * exit_price * 0.05
        self.cash_balance += margin_released + realized_pnl
        self.total_pnl += realized_pnl
        self.daily_pnl += realized_pnl

        del self.open_positions[asset]

        return {
            "success": True,
            "realized_pnl": realized_pnl,
            "asset": asset,
            "reason": reason,
            "cash_balance": self.cash_balance
        }

    def should_rebalance(self) -> bool:
        """Check if portfolio rebalancing is needed"""
        if not self.open_positions:
            return False

        # Check if any position is too large
        for pos in self.open_positions.values():
            position_value = pos.size * pos.current_price
            if position_value > self.equity * 0.25:  # Max 25% in single position
                return True

        return False

    def get_portfolio_summary(self) -> str:
        """Formatted portfolio summary"""
        state = self.update_positions({})  # Update with current prices

        output = f"""
## 📊 Portfolio Summary

### Account
- **Initial Capital**: ${self.initial_capital:,.2f}
- **Current Equity**: ${state.total_equity:,.2f}
- **Cash Balance**: ${state.cash_balance:,.2f}
- **Total P&L**: ${state.total_pnl:,.2f} ({(state.total_pnl/self.initial_capital)*100:+.2f}%)

### Risk Metrics
- **Exposure**: {state.exposure_percent:.1f}% (max {self.max_portfolio_exposure}%)
- **Risk Exposure**: {state.risk_exposure:.2f}%
- **Free Margin**: ${state.free_margin:,.2f}

### Positions ({len(state.open_positions)} open)
"""
        for pos in state.open_positions:
            pnl_emoji = "🟢" if pos.unrealized_pnl >= 0 else "🔴"
            output += f"- {pos.asset}: {pos.size} lots @ ${pos.entry_price:,.2f} "
            output += f"(Current: ${pos.current_price:,.2f}) {pnl_emoji} ${pos.unrealized_pnl:,.2f}\n"

        return output


# Quick portfolio management functions
def create_portfolio(
    initial_capital: float = 10000.0,
    max_risk: float = 2.0
) -> PortfolioManager:
    """Create new portfolio"""
    return PortfolioManager(
        initial_capital=initial_capital,
        max_risk_per_trade=max_risk
    )


def check_order_eligibility(
    portfolio: PortfolioManager,
    asset: str,
    entry: float,
    stop: float,
    risk: float = 1.0
) -> Dict:
    """Quick order eligibility check"""
    return portfolio.calculate_position_size(asset, entry, stop, risk)


if __name__ == "__main__":
    # Test
    pm = PortfolioManager(initial_capital=10000)

    # Create order
    order = Order(
        order_id="001",
        asset="XAU",
        direction="buy",
        size=0.01,
        entry_price=4640,
        stop_loss=4620,
        take_profit=4680,
        risk_percent=1.0
    )

    # Approve and execute
    approval = pm.approve_order(order)
    print(f"Approval: {approval}")

    if approval["approved"]:
        result = pm.execute_order(order, current_price=4640)
        print(f"Execution: {result}")

    print(pm.get_portfolio_summary())
