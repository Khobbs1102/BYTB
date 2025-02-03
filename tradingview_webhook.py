from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1335802330271973428/Jte3YJ76NL9p3v8lB-jVBtp2NiNFVBc7AqHsBxOsrUTCWIJgXdWoLtrh_Dlf5t23Nx29"

@app.route('/tradingview', methods=['POST'])
def tradingview_webhook():
    try:
        data = request.json  # Receive JSON from TradingView

        if not data:
            return jsonify({"error": "Invalid data"}), 400

        # Extract details from TradingView alert
        ticker = data.get('ticker', 'Unknown')
        price = data.get('close', 'Unknown')
        condition = data.get('strategy', {}).get('order', {}).get('comment', 'Unknown')

        # Determine color for Discord embed (Green for Buy, Red for Sell)
        color = 0x00FF00 if "buy" in condition.lower() or "long" in condition.lower() else 0xFF0000

        # Create a Discord embed message
        discord_message = {
            "embeds": [
                {
                    "title": "🚀 Trading Alert!",
                    "description": f"**Symbol:** {ticker}\n**Price:** ${price}\n**Condition:** {condition}",
                    "color": color
                }
            ]
        }

        # Send alert to Discord
        response = requests.post(DISCORD_WEBHOOK_URL, json=discord_message)

        if response.status_code == 204:
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "Failed to send message to Discord"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
