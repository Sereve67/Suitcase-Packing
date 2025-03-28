from flask import Flask, render_template, request, jsonify

def knapsack_dp(items, capacity):
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if items[i - 1]['size'] <= w:
                dp[i][w] = max(items[i - 1]['value'] + dp[i - 1][w - items[i - 1]['size']], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]
    
    packed_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            packed_items.append(items[i - 1]['name'])
            w -= items[i - 1]['size']
    
    return packed_items, dp[n][capacity]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pack', methods=['POST'])
def pack_suitcase():
    data = request.get_json()
    items = data['items']
    capacity = data['capacity']
    packed_items, max_value = knapsack_dp(items, capacity)
    return jsonify({"packed_items": packed_items, "max_value": max_value})

if __name__ == '__main__':
    app.run(debug=True)
