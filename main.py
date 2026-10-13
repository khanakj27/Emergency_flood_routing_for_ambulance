"""FastAPI application — Bengaluru Emergency Route Intelligence System (ERIS)."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import create_tables
from app.services.road_graph_service import road_graph_service
from app.services.hospital_service import hospital_service

# API routers
from app.api import health, floods, simulations, green_corridor, websocket
from app.api.auth import router as auth_router
from app.api.weather import router as weather_router
from app.api.routes import router as routes_router
from app.api.hospitals import router as hospitals_router
from app.api.geocoding import router as geocoding_router
from app.api.ambulances import router as ambulances_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────────────────────────
    print("=" * 60)
    print(f"  {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"  System Mode: {settings.SYSTEM_MODE}")
    print("=" * 60)

    # Create DB tables
    print("Initialising database...")
    await create_tables()
    print("Database tables ready.")

    # Pre-load road graph
    print("Loading Bengaluru road network...")
    road_graph_service.load_graph()
    G = road_graph_service.get_graph()
    print(f"Road graph ready: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    # Pre-load hospitals
    print("Loading hospital data...")
    hospital_service.load_hospitals()
    print(f"Hospitals loaded: {len(hospital_service.get_all())}")

    print("ERIS ready to serve requests.")
    yield

    # ── Shutdown ──────────────────────────────────────────────────────
    print("ERIS shutting down.")


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Bengaluru Emergency Route Intelligence System — "
        "Flood-aware ambulance routing with real weather, road-network routing, "
        "and hospital reachability. System mode: "
        + settings.SYSTEM_MODE
    ),
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(auth_router)
app.include_router(weather_router)
app.include_router(routes_router)
app.include_router(hospitals_router)
app.include_router(geocoding_router)
app.include_router(ambulances_router)
app.include_router(health.router)
app.include_router(floods.router)
app.include_router(simulations.router)
app.include_router(green_corridor.router)
app.include_router(websocket.router)


@app.get("/")
async def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "system_mode": settings.SYSTEM_MODE,
        "docs": "/docs",
    }
