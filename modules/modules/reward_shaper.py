import numpy as np

def shape(base_reward, context):
    volatility = context.get("volatility", 0)
    net_growth = context.get("net_worth_growth", 0)
    drawdown = context.get("drawdown", 0)
    sentiment = context.get("sentiment", "neutral")
    position = context.get("position_type", 0)

    growth_bonus = 1.5 * net_growth if net_growth > 0 else 0
    drawdown_penalty = -2.0 * drawdown if drawdown > 0.2 else 0

    if volatility < 0.01:
        stability_bonus = +0.1
    elif volatility > 0.05:
        stability_bonus = -0.1
    else:
        stability_bonus = 0

    sentiment_bonus = 0
    if sentiment in ["strong_bullish", "bullish"] and position == 1:
        sentiment_bonus = 0.5
    elif sentiment in ["strong_bearish", "bearish"] and position == -1:
        sentiment_bonus = 0.5
    elif sentiment in ["strong_bullish", "bullish"] and position == -1:
        sentiment_bonus = -0.5
    elif sentiment in ["strong_bearish", "bearish"] and position == 1:
        sentiment_bonus = -0.5

    final_reward = base_reward + growth_bonus + drawdown_penalty + stability_bonus + sentiment_bonus
    return float(np.clip(final_reward, -10.0, 10.0))
