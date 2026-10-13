# Emergency Flood Routing for Ambulance

A real-time, flood-aware emergency routing system designed to help ambulances reach the nearest suitable hospital safely during heavy rainfall and urban flooding in Bengaluru.

The system combines live ambulance location, road-network data, traffic conditions, weather information, hospital reachability, and flood-risk inputs to calculate the safest and fastest available route. When a road becomes flooded or blocked, the system identifies the affected segment, evaluates alternative routes, and dynamically recommends a safer path.

----------

## Overview

During heavy rainfall, ambulance movement can be delayed by waterlogged roads, traffic congestion, and road closures. A route that is fastest under normal conditions may become unsafe or unusable during flooding.

**Emergency Flood Routing for Ambulance** addresses this problem by treating the Bengaluru road network as a dynamic graph. Roads are represented as edges, intersections as nodes, and each road segment is assigned a dynamic cost based on travel time, traffic, flood risk, weather conditions, and ambulance suitability.

The system does not simply find the shortest route. It recommends the most suitable route by balancing:

- Travel time
- Traffic delay
- Flood exposure
- Weather-related risk
- Road blockages
- Ambulance suitability
- Hospital reachability
- Route confidence

----------

## Key Features

- Secure user authentication and role-based access
- Interactive Bengaluru map
- Ambulance starting-point input through address, map click, coordinates, or GPS
- Verified 24/7 emergency hospital visualization
- Nearest suitable and reachable hospital selection
- Complete road-based route visualization
- Alternative-route generation and comparison
- Live weather integration
- Flood-risk and road-blockage handling
- Dynamic route recalculation
- Confidence-aware flood decision logic
- Route explanation and decision transparency
- Data freshness, source metadata, and system-health indicators
- Green-corridor integration architecture

----------

## How It Works

```text
Ambulance location
        ↓
Road matching and validation
        ↓
Nearby hospital discovery
        ↓
Hospital reachability analysis
        ↓
Weather and traffic retrieval
        ↓
Flood-risk assessment
        ↓
Route generation
        ↓
Multi-objective route ranking
        ↓
Recommended route displayed on map
        ↓
Dynamic recalculation when conditions change
```

When a road is confirmed to be blocked or severely flooded, it is excluded from the recommended route. If flood information is uncertain or moderate, the affected road is penalized instead of being automatically blocked.

----------

## Example Route Recommendation

```text
Nearest suitable hospital:
Trilife Hospital

Hospital location:
Kalyan Nagar, Bengaluru

Ambulance starting point:
Ramamurthy Nagar

Weather condition:
28°C, no rain

Fastest route:
Ramamurthy Nagar Circle → Outer Ring Road NH44/NH75
→ HRBR Layout → 1st Block, 7th Main Road → 80 Feet Road

Estimated travel time:
18 minutes

Distance:
7.4 km

Route status:
Available

Flood risk:
Low
```

The displayed hospital, weather, route, ETA, and distance are generated dynamically from the selected ambulance location and available data sources.

----------

## Technology Stack

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- MapLibre GL JS or Google Maps JavaScript API
- GeoJSON
- Turf.js
- Zustand
- TanStack Query
- Recharts
- Framer Motion

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn
- SQLAlchemy
- aiosqlite
- NetworkX
- GeoPandas
- Shapely
- PyProj
- Redis

### Database

- SQLite with aiosqlite for local development
- PostgreSQL with PostGIS for production-ready spatial data storage

### Routing and External Services

- GraphHopper, OSRM, or Google Routes API for road-network routing
- Open-Meteo or another approved weather provider
- Flood-detection module or flood-observation API
- Green-corridor or traffic-signal integration service

----------

## System Architecture

```text
Frontend Dashboard
        ↓
FastAPI Backend
        ↓
Authentication and Validation
        ↓
Hospital and Ambulance Services
        ↓
Weather and Traffic Services
        ↓
Flood-Risk Service
        ↓
Route Optimization Engine
        ↓
Route Visualization and Green Corridor
```

----------

## Route Optimization Logic

The system calculates a route score using multiple factors:

```text
Route Score =
0.45 × travel time
+ 0.20 × traffic delay
+ 0.20 × flood and blockage risk
+ 0.10 × weather risk
+ 0.05 × ambulance suitability
```

The route with the lowest valid score is recommended.

A route is considered invalid if it contains:

- A confirmed road closure
- A confirmed impassable flood segment
- An inaccessible hospital destination
- A road restricted for ambulance access

A route may be penalized if it contains:

- Moderate flood risk
- Low-confidence flood information
- Heavy rainfall
- High traffic delay
- Poor ambulance accessibility

----------

## API Overview

```text
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me

GET  /api/hospitals
GET  /api/hospitals/nearest-reachable
GET  /api/hospitals/{id}

POST /api/routes/plan
POST /api/routes/recalculate
GET  /api/routes/{id}
GET  /api/routes/{id}/segments

GET  /api/weather/current
GET  /api/weather/route

POST /api/roads/blockage
POST /api/roads/flood-report
GET  /api/roads/status

POST /api/green-corridor/request
GET  /api/green-corridor/{routeId}/status
```

The interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

----------

## Getting Started

### Prerequisites

- Python 3.11 or later
- Node.js
- npm
- Git
- Docker, optional for containerized deployment

### Clone the repository

```bash
git clone https://github.com/your-username/emergency_flood_routing_for_ambulance.git
cd emergency_flood_routing_for_ambulance
```

### Install backend dependencies

```bash
cd backend
python3.11 -m pip install -r requirements.txt
```

### Start the backend

```bash
python3.11 -m uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

### Install frontend dependencies

Open a new terminal:

```bash
cd frontend
npm install
```

### Start the frontend

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:3000
```

----------

## Environment Variables

Create a `.env` file in the frontend directory:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
NEXT_PUBLIC_MAP_STYLE_URL=your_map_style_url
```

Create a `.env` file in the backend directory:

```env
DATABASE_URL=sqlite+aiosqlite:///./app.db
SECRET_KEY=your_secure_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Do not expose private API keys in frontend environment variables.

----------

## Running with Docker

```bash
docker compose up --build
```

To stop the application:

```bash
docker compose down
```

----------

## Project Structure

```text
emergency_flood_routing_for_ambulance/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   ├── schemas/
│   │   └── core/
│   ├── requirements.txt
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── types/
│   │   └── services/
│   ├── package.json
│   └── .env.local
├── docs/
├── docker-compose.yml
└── README.md
```

----------

## Data Sources

- **Road network:** OpenStreetMap  
- **Hospital locations:** Verified hospital dataset or OpenStreetMap-derived data  
- **Weather:** Open-Meteo or another approved weather provider  
- **Traffic:** Routing provider or approved traffic-data service  
- **Flood information:** Flood-detection module, verified reports, sensors, or controlled development fixtures  

OpenStreetMap data is available under the Open Database License and requires attribution to OpenStreetMap contributors.  Open-Meteo data is offered under CC BY 4.0 and requires attribution when displayed publicly. [osmfoundation](https://osmfoundation.org/wiki/Attribution)

----------

## Important Notes

This project is designed as an **emergency decision-support system**. It does not guarantee that a road is safe, that an ambulance will arrive within the displayed time, or that a hospital has available capacity.

The system clearly distinguishes between:

- Live data
- Degraded data
- Stale data
- Unavailable data
- Development or test data

It should not be used as an autonomous emergency-control system without proper validation, authorization, institutional approval, and real-world field testing.

----------

## Future Enhancements

- Live CCTV-based flood detection
- IoT water-level sensor integration
- Real-time traffic-provider integration
- Hospital bed and emergency-capacity integration
- Ambulance mobile application
- Green-corridor traffic-signal integration
- Machine-learning-based ETA prediction
- Route-reliability forecasting
- Multi-ambulance dispatch optimization
- Historical flood-risk analysis
- Full cloud deployment and monitoring

----------

## License

This project is intended for educational and research purposes. External data providers and map services may have their own licensing requirements.

----------

## Acknowledgements

- [OpenStreetMap](https://www.openstreetmap.org/copyright)
- [Open-Meteo](https://open-meteo.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [NetworkX](https://networkx.org/)
- [MapLibre GL JS](https://maplibre.org/)
