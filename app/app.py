from flask import Flask, jsonify, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time, random

app = Flask(__name__)

REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)
REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'HTTP request latency',
    ['endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5]
)
ERROR_COUNT = Counter(
    'app_errors_total',
    'Total errors',
    ['endpoint']
)

def track(endpoint, status):
    REQUEST_COUNT.labels(method='GET', endpoint=endpoint, status=status).inc()

@app.route('/')
def home():
    start = time.time()
    if random.random() < 0.05:
        ERROR_COUNT.labels(endpoint='/').inc()
        track('/', '500')
        REQUEST_LATENCY.labels(endpoint='/').observe(time.time() - start)
        return jsonify({"error": "Internal Server Error"}), 500
    time.sleep(random.uniform(0.01, 0.1))
    track('/', '200')
    REQUEST_LATENCY.labels(endpoint='/').observe(time.time() - start)
    return jsonify({"status": "healthy", "service": "SRE Observability Platform", "version": "1.0.0"})

@app.route('/api/data')
def data():
    start = time.time()
    time.sleep(random.uniform(0.05, 0.3))
    track('/api/data', '200')
    REQUEST_LATENCY.labels(endpoint='/api/data').observe(time.time() - start)
    return jsonify({"data": [1, 2, 3], "count": 3})

@app.route('/health')
def health():
    track('/health', '200')
    return jsonify({"status": "ok"})

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)