from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import numpy as np
import random
import os

app = FastAPI(title="Monte Carlo PDE Solver", description="Solve PDEs using Monte Carlo methods")

# Add CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (frontend in backend url)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

class SimulationParams(BaseModel):
    n: int = 400  # number of random walks
    dim: int = 1  # 1D or 2D
    lattice_points: int = 15  # Number of points in lattice
    laplace: bool = True  # True for Laplace, False for Poisson

# Constants
h = 10e-2  # Distance between plates = 10cm
boundary_voltage_high = 5.0  # 5 Volts at Positive Plate
boundary_voltage_low = 0.0  # 0 Volts at Negative Plate
epsilon_naught = 8.854e-12  # Permittivity of Vacuum
charge_density = 1e-14  # Coulomb per meter cube

def f_1d(x, laplace=True):
    """The Function ∇²(phi) = f for 1D"""
    if laplace:
        return 0
    else:
        # For Poisson, assume constant charge density
        return (x / h - 0.5) * -charge_density / epsilon_naught

def g_1d(x):
    """1D Boundary Conditions"""
    if x <= 0:
        return boundary_voltage_low
    return boundary_voltage_high

def poisson_approximation_1d(A, N, lattice_points, laplace=True):
    """Monte Carlo solution for 1D PDE"""
    d = h / lattice_points
    result = 0
    F = 0
    
    for i in range(N):
        x = A
        steps = 0
        while True:
            if x <= 0 or x >= h:
                break
            if random.randint(0, 1):
                x += d
            else:
                x -= d
            if not laplace:
                F += f_1d(x, laplace) * d * d / 2
            steps += 1
            if steps > 1000:  # Prevent infinite loops
                break
        
        result += g_1d(x) + F
        F = 0
    
    return result / N

def g_2d(x):
    """2D Boundary Conditions: parallel plates at x=0,x=h"""
    if x[0] <= 0:
        return boundary_voltage_low
    if x[0] >= h:
        return boundary_voltage_high
    if x[1] <= 0 or x[1] >= h:
        return boundary_voltage_low

def poisson_approximation_2d(A, N, lattice_points):
    """Monte Carlo solution for 2D Laplace equation"""
    d = h / lattice_points
    result = 0
    
    for i in range(N):
        x = list(A)
        steps = 0
        while True:
            if x[0] <= 0 or x[0] >= h or x[1] <= 0 or x[1] >= h:
                break
            
            direction = random.randint(0, 3)
            if direction == 0:
                x[0] += d
            elif direction == 1:
                x[0] -= d
            elif direction == 2:
                x[1] += d
            else:
                x[1] -= d
            
            steps += 1
            if steps > 1000:  # Prevent infinite loops
                break
        
        result += g_2d(x)
    
    return result / N

@app.get("/")
async def serve_frontend():
    """Serve the frontend HTML file"""
    return FileResponse('frontend/index.html')

@app.post("/simulate/poisson")
def simulate_poisson(params: SimulationParams):
    """Simulate Poisson equation using Monte Carlo method"""
    try:
        if params.dim == 1:
            # 1D Poisson equation
            A = h / 2  # Test point at center
            result = poisson_approximation_1d(A, params.n, params.lattice_points, laplace=False)
            return {
                "method": "poisson", 
                "dimension": params.dim, 
                "n_walks": params.n,
                "lattice_points": params.lattice_points,
                "test_point": A,
                "result": float(result)
            }
        else:
            return {"error": "2D Poisson not implemented yet"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/simulate/laplace")
def simulate_laplace(params: SimulationParams):
    """Simulate Laplace equation using Monte Carlo method"""
    try:
        if params.dim == 1:
            # 1D Laplace equation
            A = h / 2  # Test point at center
            result = poisson_approximation_1d(A, params.n, params.lattice_points, laplace=True)
            return {
                "method": "laplace", 
                "dimension": params.dim, 
                "n_walks": params.n,
                "lattice_points": params.lattice_points,
                "test_point": A,
                "result": float(result)
            }
        elif params.dim == 2:
            # 2D Laplace equation
            A = [h/2, h/2]  # Test point at center
            result = poisson_approximation_2d(A, params.n, params.lattice_points)
            return {
                "method": "laplace", 
                "dimension": params.dim, 
                "n_walks": params.n,
                "lattice_points": params.lattice_points,
                "test_point": A,
                "result": float(result)
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/info")
def get_info():
    """Get information about the Monte Carlo PDE solver"""
    return {
        "title": "Monte Carlo PDE Solver",
        "description": "Solve Poisson and Laplace equations using Monte Carlo methods",
        "methods": ["laplace", "poisson"],
        "dimensions": [1, 2],
        "constants": {
            "plate_distance": f"{h*100} cm",
            "high_voltage": f"{boundary_voltage_high} V",
            "low_voltage": f"{boundary_voltage_low} V"
        }
    }
