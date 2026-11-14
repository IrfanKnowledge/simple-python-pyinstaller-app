#!/usr/bin/env python3
"""
Web interface for the Dicoding CI/CD Python Calculator Application.
Uses the `calc.add2` library function and serves an interactive web UI + JSON API.
Binds to 0.0.0.0:$PORT (defaults to 5050 locally or 10000 on Render).
"""

import json
import os
import socket
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

# Ensure local directory is in sys.path so `import calc` works from any working directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calc  # noqa: E402


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Python Calc CI/CD App — irfx_programmer | Dicoding</title>
    <style>
        :root {
            --bg: #0f172a;
            --card: #1e293b;
            --accent: #38bdf8;
            --success: #22c55e;
            --text: #f8fafc;
            --muted: #94a3b8;
            --border: #334155;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
        }
        .container {
            max-width: 720px;
            width: 100%;
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 32px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45);
        }
        .badge-row {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 16px;
        }
        .badge {
            font-size: 12px;
            font-weight: 600;
            padding: 5px 12px;
            border-radius: 999px;
            background: rgba(56, 189, 248, 0.15);
            color: var(--accent);
            border: 1px solid rgba(56, 189, 248, 0.3);
        }
        .badge.live {
            background: rgba(34, 197, 94, 0.15);
            color: var(--success);
            border-color: rgba(34, 197, 94, 0.35);
        }
        h1 {
            font-size: 26px;
            margin-bottom: 8px;
            color: #ffffff;
        }
        p.subtitle {
            color: var(--muted);
            font-size: 14px;
            margin-bottom: 24px;
            line-height: 1.5;
        }
        .calc-box {
            background: rgba(15, 23, 42, 0.65);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .form-row {
            display: grid;
            grid-template-columns: 1fr auto 1fr auto;
            gap: 12px;
            align-items: center;
        }
        input[type="text"] {
            width: 100%;
            padding: 12px 14px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: #0f172a;
            color: #fff;
            font-size: 15px;
        }
        button {
            padding: 12px 20px;
            border-radius: 8px;
            border: none;
            background: var(--accent);
            color: #0f172a;
            font-weight: 700;
            font-size: 15px;
            cursor: pointer;
        }
        .result-banner {
            margin-top: 16px;
            padding: 14px 16px;
            border-radius: 8px;
            background: rgba(34, 197, 94, 0.12);
            border: 1px solid rgba(34, 197, 94, 0.35);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .result-value {
            font-size: 20px;
            font-weight: 700;
            color: var(--success);
            font-family: monospace;
        }
        .meta-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            font-size: 13px;
        }
        .meta-item {
            background: rgba(15, 23, 42, 0.45);
            border: 1px solid var(--border);
            padding: 10px 14px;
            border-radius: 8px;
        }
        .meta-label { color: var(--muted); font-size: 11px; text-transform: uppercase; }
        .meta-val { color: var(--text); font-weight: 600; margin-top: 2px; font-family: monospace; }
    </style>
</head>
<body>
    <div class="container">
        <div class="badge-row">
            <span class="badge live">● STATUS: LIVE DEPLOYMENT</span>
            <span class="badge">Jenkins CI/CD Pipeline</span>
            <span class="badge">Render.com Cloud PaaS</span>
        </div>
        <h1>Simple Python PyInstaller & Web App (calc.add2)</h1>
        <p class="subtitle">
            Proyek Akhir <strong>Belajar Implementasi CI/CD — Dicoding Indonesia</strong>.<br/>
            Pipeline: <code>submission-cicd-pipeline-irfx_programmer</code> (Build → Test → Manual Approval → Deploy)
        </p>

        <div class="calc-box">
            <form method="GET" action="/">
                <div class="form-row">
                    <input type="text" name="a" value="{val_a}" placeholder="Nilai pertama (mis. 25)" />
                    <span style="font-weight:700; color: var(--accent);">+</span>
                    <input type="text" name="b" value="{val_b}" placeholder="Nilai kedua (mis. 75)" />
                    <button type="submit">Hitung add2()</button>
                </div>
            </form>
            <div class="result-banner">
                <span>Hasil <code>calc.add2("{val_a}", "{val_b}")</code>:</span>
                <span class="result-value">{result} ({result_type})</span>
            </div>
        </div>

        <div class="meta-grid">
            <div class="meta-item">
                <div class="meta-label">Peserta / Dicoding ID</div>
                <div class="meta-val">Irfan Muhammad Faisal (irfx_programmer)</div>
            </div>
            <div class="meta-item">
                <div class="meta-label">Pipeline Stages</div>
                <div class="meta-val">Build • Test • Manual Approval • Deploy</div>
            </div>
            <div class="meta-item">
                <div class="meta-label">Host / Container</div>
                <div class="meta-val">{hostname}</div>
            </div>
            <div class="meta-item">
                <div class="meta-label">Timestamp (UTC)</div>
                <div class="meta-val">{timestamp}</div>
            </div>
        </div>
    </div>
</body>
</html>
"""


class CalcRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        val_a = params.get("a", ["25"])[0]
        val_b = params.get("b", ["75"])[0]
        computed = calc.add2(val_a, val_b)

        if parsed.path == "/health" or parsed.path == "/api/add":
            payload = {
                "status": "ok",
                "pipeline": "submission-cicd-pipeline-irfx_programmer",
                "user": "irfx_programmer",
                "input_a": val_a,
                "input_b": val_b,
                "result": computed,
                "result_type": type(computed).__name__,
                "hostname": socket.gethostname(),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            body = json.dumps(payload, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        html = (
            HTML_TEMPLATE.replace("{val_a}", str(val_a))
            .replace("{val_b}", str(val_b))
            .replace("{result}", str(computed))
            .replace("{result_type}", type(computed).__name__)
            .replace("{hostname}", socket.gethostname())
            .replace("{timestamp}", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"))
        )
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        sys.stdout.write("%s - - [%s] %s\n" % (
            self.address_string(),
            self.log_date_time_string(),
            fmt % args
        ))
        sys.stdout.flush()


def main():
    port = int(os.environ.get("PORT", "5050"))
    server = HTTPServer(("0.0.0.0", port), CalcRequestHandler)
    print(f"Starting Python Calc Web Server on http://0.0.0.0:{port} ...")
    sys.stdout.flush()
    server.serve_forever()


if __name__ == "__main__":
    main()
