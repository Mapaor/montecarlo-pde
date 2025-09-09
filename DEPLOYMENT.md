# Monte Carlo PDE Solver - Deployment Guide

## Quick Setup for Render Deployment

Your repository is now ready for deployment on Render! Here's everything that has been configured:

### ✅ Files Ready for Deployment

1. **`app.py`** - FastAPI backend with Monte Carlo PDE solvers
2. **`requirements.txt`** - Python dependencies (updated for compatibility)
3. **`render.yaml`** - Render deployment configuration
4. **`frontend/index.html`** - Interactive web interface
5. **`.gitignore`** - Git ignore rules for Python projects
6. **`README.md`** - Updated with deployment instructions

### 🚀 Deploy to Render

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Setup Monte Carlo PDE solver for Render deployment"
   git push origin main
   ```

2. **Deploy on Render**:
   - Go to [render.com](https://render.com) and sign up/login
   - Click "New +" → "Web Service"
   - Connect your GitHub account and select this repository
   - Render will automatically detect the `render.yaml` file
   - Click "Deploy" (deployment will take 2-5 minutes)

3. **Access Your App**:
   - Your app will be available at: `https://your-service-name.onrender.com`
   - The web interface will load automatically at the root URL

### 🧪 What's Included

#### Backend API Endpoints:
- `GET /` - Web interface
- `POST /simulate/laplace` - Solve Laplace equation (∇²φ = 0)
- `POST /simulate/poisson` - Solve Poisson equation (∇²φ = -ρ/ε₀)
- `GET /api/info` - System information

#### Frontend Features:
- Interactive parameter controls
- Support for 1D and 2D simulations
- Real-time results display
- Responsive design for mobile/desktop
- Error handling and validation

#### Simulation Parameters:
- **Random Walks**: 10-10,000 (default: 400)
- **Lattice Points**: 5-100 (default: 15)
- **Dimensions**: 1D and 2D
- **Equations**: Laplace and Poisson

### 🔧 Technical Details

#### Physical Setup:
- **Parallel plate capacitor** (10 cm separation)
- **Boundary conditions**: 0V and 5V plates
- **Charge density**: Configurable for Poisson equation
- **Test point**: Center of domain

#### Monte Carlo Method:
- Random walk algorithm
- Configurable step size based on lattice
- Boundary value integration
- Statistical convergence with multiple walks

### 🛠️ Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn app:app --reload

# Open browser to http://localhost:8000
```

### 📝 Example API Usage

```bash
# Test the API
curl -X POST "https://your-app.onrender.com/simulate/laplace" \
     -H "Content-Type: application/json" \
     -d '{"n": 400, "dim": 1, "lattice_points": 15}'
```

### 🎯 Next Steps

1. **Commit and push** your changes to GitHub
2. **Deploy to Render** using the instructions above
3. **Test the deployed application** with different parameters
4. **Share your Monte Carlo PDE solver** with others!

### 💡 Additional Features You Can Add

- **Visualization**: Add plotting capabilities with matplotlib
- **More PDE types**: Heat equation, wave equation
- **Advanced algorithms**: Semi-floating, full-floating random walks
- **Parameter optimization**: Automatic convergence detection
- **Database storage**: Save simulation results

Your Monte Carlo PDE solver is now production-ready! 🎉
