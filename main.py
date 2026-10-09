from Market_Data.live_data import MarketDataService, MarketDataError
from Market_Data.candles import CandleManager

from Technical_Analysis.indicators import TechnicalAnalyzer
from Technical_Analysis.trend import TrendAnalyzer
from Technical_Analysis.support_resistance import SupportResistanceAnalyzer
from Technical_Analysis.candle_analysis import CandleAnalyzer

from Signal_System.signal_generator import SignalGenerator
from AI_Engine.decision import AIDecisionEngine


def run_analysis():

    print("=" * 60)
    print("AI QUOTEX TRADING ASSISTANT")
    print("=" * 60)

    # ==========================================
    # SETTINGS
    # ==========================================

    symbol = "EUR/USD"
    interval = "1min"
    candle_count = 100

    # ==========================================
    # MARKET DATA
    # ==========================================

    try:

        market_service = MarketDataService()

        market_result = market_service.get_candles(
            symbol=symbol,
            interval=interval,
            outputsize=candle_count,
        )

    except MarketDataError as error:

        print("Market Data Error:")
        print(error)
        return

    candles = market_result.get(
        "candles",
        []
    )

    if not candles:

        print("No candle data available.")
        return

    # ==========================================
    # CANDLE MANAGER
    # ==========================================

    candle_manager = CandleManager(
        max_candles=500
    )

    candle_manager.load_candles(
        candles
    )

    df = candle_manager.get_dataframe()

    if len(df) < 30:

        print(
            "Not enough candle data "
            "for analysis."
        )
        return

    # ==========================================
    # TECHNICAL ANALYSIS
    # ==========================================

    technical_result = (
        TechnicalAnalyzer.analyze(df)
    )

    trend_result = (
        TrendAnalyzer.analyze(df)
    )

    support_resistance_result = (
        SupportResistanceAnalyzer.analyze(df)
    )

    candle_result = (
        CandleAnalyzer.analyze(df)
    )

    # ==========================================
    # SIGNAL GENERATION
    # ==========================================

    signal_generator = SignalGenerator()

    signal_result = signal_generator.generate(
        trend_result=trend_result,
        technical_result=technical_result,
        support_resistance_result=(
            support_resistance_result
        ),
        candle_result=candle_result,
    )

    # ==========================================
    # FINAL AI DECISION
    # ==========================================

    decision_engine = AIDecisionEngine()

    final_decision = decision_engine.decide(
        signal_result
    )

    # ==========================================
    # OUTPUT
    # ==========================================

    print(
        "Data Mode:",
        market_result["mode"]
    )

    print(
        "Asset:",
        symbol
    )

    print(
        "Timeframe:",
        interval
    )

    print(
        "Candles:",
        len(df)
    )

    print("-" * 60)

    print(
        "Trend:",
        trend_result["symbol"],
        trend_result["trend"]
    )

    print(
        "Current Price:",
        technical_result[
            "current_price"
        ]
    )

    print(
        "Moving Average:",
        technical_result[
            "moving_average"
        ]["signal"]
    )

    print(
        "RSI:",
        technical_result["rsi"]["value"],
        technical_result["rsi"]["signal"]
    )

    print(
        "MACD:",
        technical_result["macd"]["signal"]
    )

    print(
        "Bollinger:",
        technical_result[
            "bollinger_bands"
        ]["signal"]
    )

    print(
        "Support:",
        support_resistance_result[
            "support"
        ]
    )

    print(
        "Resistance:",
        support_resistance_result[
            "resistance"
        ]
    )

    print(
        "Candlestick:",
        candle_result["bias"]
    )

    print("=" * 60)

    print(
        "FINAL SIGNAL:",
        final_decision[
            "display_signal"
        ]
    )

    print(
        "Confidence:",
        f'{final_decision["confidence"]}%'
    )

    print(
        "Risk:",
        final_decision["risk"]
    )

    print(
        "Message:",
        final_decision["message"]
    )

    print(
        "Auto Trade:",
        final_decision["auto_trade"]
    )

    print("=" * 60)

    if market_result["mode"] == "DEMO":

        print(
            "⚠ DEMO DATA - "
            "NOT LIVE MARKET DATA"
        )

    else:

        print(
            "✅ LIVE MARKET DATA"
        )

    print("=" * 60)


if __name__ == "__main__":
    run_analysis()