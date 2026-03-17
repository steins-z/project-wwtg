# 周末搭子 🎉

AI-powered weekend activity planner for WeChat Mini Program.

## Project Structure

```
├── backend/          # FastAPI Python backend
├── miniprogram/      # WeChat Mini Program frontend
├── docs/             # PRD and technical design
├── tools/            # Development tools
└── docker-compose.yml
```

## Quick Start

### Backend

```bash
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload
# API at http://localhost:8000
# Health check: http://localhost:8000/health
```

### Docker (all services)

```bash
docker-compose up --build
```

### Mini Program

1. Open WeChat DevTools
2. Import `miniprogram/` directory
3. Replace appid in `project.config.json`
4. Mock mode enabled by default (no backend needed)

## W1 Status

- ✅ FastAPI scaffold with all API endpoints
- ✅ SSE streaming chat endpoint
- ✅ Mock services (LLM, weather, plans, data pipeline)
- ✅ Conversation state machine
- ✅ SQLAlchemy DB models
- ✅ Mini program chat UI, plan cards, detail page
- ⬜ Real LLM integration (W2)
- ⬜ Real weather/map APIs (W2)
- ⬜ Playwright data pipeline (W2)
- ⬜ Database migrations (W2)
