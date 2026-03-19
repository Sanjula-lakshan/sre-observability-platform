# SRE Observability Platform with DevSecOps Pipeline

A production-grade **Site Reliability Engineering (SRE)** observability platform featuring a full DevSecOps CI/CD pipeline, live SLO error budget tracking, and automated status page deployment.

## Architecture

- **CI/CD**: GitHub Actions → Docker build (multi-stage) → Trivy security scan → GHCR push
- **App**: Python Flask with custom Prometheus metrics (request rate, latency, error rate)
- **Observability**: Prometheus (scraping) + Grafana (dashboards) + Alertmanager (alerts)
- **SRE**: SLO error budget panel, p50/p95/p99 latency tracking
- **Status Page**: Auto-deployed to GitHub Pages on every main push

## What is an SLO Error Budget?

An **SLO (Service Level Objective)** defines a reliability target (e.g., 99.5% availability). The **error budget** is the allowed failure budget — if your SLO is 99.5%, you have 0.5% budget to "spend" on errors before breaching your SLO. This dashboard shows that budget in real-time.

## Quick Start

```bash
git clone <your-repo>
cd sre-observability-platform
docker compose up --build
```

| Service      | URL                                    |
| ------------ | -------------------------------------- |
| Flask App    | http://localhost:5000                  |
| Prometheus   | http://localhost:9090                  |
| Grafana      | http://localhost:3000 (admin/admin123) |
| Alertmanager | http://localhost:9093                  |

## Key Skills Demonstrated

- Multi-stage Docker builds for minimal image size
- Trivy vulnerability scanning integrated in CI
- Real Prometheus metrics with PromQL queries
- SLO error budget calculation (production SRE concept)
- GitOps-style automated status page deployment
