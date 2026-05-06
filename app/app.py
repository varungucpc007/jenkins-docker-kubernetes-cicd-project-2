try:
    from flask import Flask  # type: ignore[import]
except ImportError as e:
    raise ImportError("Flask is required to run this app. Install it with 'pip install flask'.") from e

app = Flask(__name__)

# Advanced CSS styles
CSS_STYLES = """
<style>
    /* Modern CSS Reset */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    /* Professional Color Scheme & Fonts */
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0;
        padding: 20px;
        position: relative;
        overflow-x: hidden;
    }

    /* Animated Background Pattern */
    body::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: moveBackground 20s linear infinite;
        pointer-events: none;
    }

    @keyframes moveBackground {
        0% {
            transform: translate(0, 0);
        }
        100% {
            transform: translate(50px, 50px);
        }
    }

    /* Main Card Container */
    .container {
        position: relative;
        z-index: 1;
        animation: fadeInUp 0.8s ease-out;
    }

    /* Professional Card Design */
    .success-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.2);
        padding: 50px 60px;
        text-align: center;
        max-width: 650px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .success-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 30px 80px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.3);
    }

    /* Success Icon Animation */
    .success-icon {
        margin-bottom: 30px;
        animation: scaleIn 0.5s ease-out 0.3s both;
    }

    .circle {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: pulse 2s infinite;
    }

    .checkmark {
        font-size: 48px;
        color: white;
        font-weight: bold;
    }

    /* Typography */
    h1 {
        font-size: 32px;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 15px;
        letter-spacing: -0.5px;
    }

    .badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 8px 20px;
        border-radius: 50px;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 25px;
        text-transform: uppercase;
        letter-spacing: 1px;
        animation: slideInLeft 0.5s ease-out;
    }

    /* Status Indicators */
    .status {
        margin: 25px 0;
        padding: 15px;
        background: #f7f9fc;
        border-radius: 12px;
        border-left: 4px solid #48bb78;
        text-align: left;
    }

    .status-item {
        display: flex;
        align-items: center;
        margin: 10px 0;
        font-size: 14px;
        color: #2d3748;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background: #48bb78;
        border-radius: 50%;
        margin-right: 10px;
        animation: blink 2s infinite;
    }

    /* Tech Stack Tags */
    .tech-stack {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
        margin: 25px 0;
    }

    .tech-tag {
        background: linear-gradient(135deg, #edf2f7 0%, #e2e8f0 100%);
        color: #4a5568;
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 500;
        font-family: 'Monaco', 'Courier New', monospace;
        transition: all 0.3s ease;
    }

    .tech-tag:hover {
        transform: translateY(-2px);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    /* Metrics Grid */
    .metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 15px;
        margin: 30px 0;
        padding: 20px 0;
        border-top: 1px solid #e2e8f0;
        border-bottom: 1px solid #e2e8f0;
    }

    .metric {
        text-align: center;
    }

    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #2d3748;
        font-family: 'Monaco', 'Courier New', monospace;
    }

    .metric-label {
        font-size: 12px;
        color: #718096;
        margin-top: 5px;
        text-transform: uppercase;
        font-weight: 600;
    }

    /* Footer */
    .footer {
        margin-top: 30px;
        padding-top: 20px;
        border-top: 1px solid #e2e8f0;
        font-size: 12px;
        color: #a0aec0;
        text-align: center;
    }

    .footer p {
        margin: 5px 0;
    }

    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes scaleIn {
        from {
            transform: scale(0);
        }
        to {
            transform: scale(1);
        }
    }

    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }

    @keyframes blink {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.3;
        }
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .success-card {
            padding: 30px 20px;
            margin: 20px;
        }
        
        h1 {
            font-size: 24px;
        }
        
        .metrics {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .circle {
            width: 60px;
            height: 60px;
        }
        
        .checkmark {
            font-size: 36px;
        }
    }
</style>
"""

# Advanced HTML template
HTML_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <meta name="description" content="Kubernetes CI/CD Pipeline Status Dashboard">
    <meta name="theme-color" content="#667eea">
    <title>K8s Pipeline | Production Ready</title>
    {CSS_STYLES}
</head>
<body>
    <div class="container">
        <div class="success-card">
            <div class="success-icon">
                <div class="circle">
                    <div class="checkmark">✓</div>
                </div>
            </div>
            
            <div class="badge">🚀 PRODUCTION READY</div>
            
            <h1>Kubernetes CI/CD Pipeline</h1>
            
            <div class="status">
                <div class="status-item">
                    <div class="status-dot"></div>
                    <span>Pipeline Status: <strong style="color:#48bb78">● Operational</strong></span>
                </div>
                <div class="status-item">
                    <div class="status-dot"></div>
                    <span>Deployment: <strong>Rolling Update Complete</strong></span>
                </div>
                <div class="status-item">
                    <div class="status-dot"></div>
                    <span>Service Mesh: <strong>Istio Enabled</strong></span>
                </div>
            </div>
            
            <div class="tech-stack">
                <span class="tech-tag">Docker</span>
                <span class="tech-tag">Kubernetes</span>
                <span class="tech-tag">Jenkins</span>
                <span class="tech-tag">GitOps</span>
                <span class="tech-tag">Prometheus</span>
                <span class="tech-tag">Grafana</span>
            </div>
            
            <div class="metrics">
                <div class="metric">
                    <div class="metric-value">99.99%</div>
                    <div class="metric-label">Uptime</div>
                </div>
                <div class="metric">
                    <div class="metric-value">3</div>
                    <div class="metric-label">Replicas</div>
                </div>
                <div class="metric">
                    <div class="metric-value">Zero</div>
                    <div class="metric-label">Downtime</div>
                </div>
                <div class="metric">
                    <div class="metric-value">Auto</div>
                    <div class="metric-label">Scaling</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return HTML_TEMPLATE

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)