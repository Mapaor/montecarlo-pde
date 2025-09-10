// Get the current domain for API calls
const API_BASE = window.location.origin;

async function runSimulation() {
  const runBtn = document.getElementById('runBtn');
  const output = document.getElementById('output');
  // Get form values
  const equation = document.getElementById('equation').value;
  const dimension = parseInt(document.getElementById('dimension').value);
  const walks = parseInt(document.getElementById('walks').value);
  const lattice = parseInt(document.getElementById('lattice').value);
  // Validate inputs
  if (walks < 10 || walks > 10000) {
    showError('Number of walks must be between 10 and 10000');
    return;
  }
  if (lattice < 5 || lattice > 100) {
    showError('Lattice points must be between 5 and 100');
    return;
  }
  // Disable button and show loading
  runBtn.disabled = true;
  runBtn.textContent = 'Running...';
  output.innerHTML = '<div class="result-box loading">Running Monte Carlo simulation...</div>';
  try {
    const response = await fetch(`${API_BASE}/simulate/${equation}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        n: walks,
        dim: dimension,
        lattice_points: lattice
      })
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    if (data.error) {
      showError(data.error);
    } else {
      showSuccess(data);
    }
  } catch (error) {
    showError(`Simulation failed: ${error.message}`);
  } finally {
    runBtn.disabled = false;
    runBtn.textContent = 'Run Simulation';
  }
}

async function getInfo() {
  const output = document.getElementById('output');
  try {
    const response = await fetch(`${API_BASE}/api/info`);
    const data = await response.json();
    showInfo(data);
  } catch (error) {
    showError(`Failed to get system info: ${error.message}`);
  }
}

function showError(message) {
  const output = document.getElementById('output');
  output.innerHTML = `<div class="result-box error"><strong>Error:</strong> ${message}</div>`;
}

function showSuccess(data) {
  const output = document.getElementById('output');
  output.innerHTML = `
    <div class="result-box success">
      <h3>Simulation Results</h3>
      <p><strong>Method:</strong> ${data.method.charAt(0).toUpperCase() + data.method.slice(1)} Equation</p>
      <p><strong>Dimension:</strong> ${data.dimension}D</p>
      <p><strong>Random Walks:</strong> ${data.n_walks}</p>
      <p><strong>Lattice Points:</strong> ${data.lattice_points}</p>
      <p><strong>Test Point:</strong> ${Array.isArray(data.test_point) ? `[${data.test_point.join(', ')}]` : data.test_point}</p>
      <p><strong>Solution:</strong> <code>${data.result.toFixed(6)} V</code></p>
      <details>
        <summary>Raw Data</summary>
        <pre>${JSON.stringify(data, null, 2)}</pre>
      </details>
    </div>
  `;
}

function showInfo(data) {
  const output = document.getElementById('output');
  output.innerHTML = `
    <div class="result-box">
      <h3>System Information</h3>
      <p><strong>Title:</strong> ${data.title}</p>
      <p><strong>Description:</strong> ${data.description}</p>
      <p><strong>Available Methods:</strong> ${data.methods.join(', ')}</p>
      <p><strong>Supported Dimensions:</strong> ${data.dimensions.join('D, ')}D</p>
      <h4>Physical Constants:</h4>
      <ul>
        <li><strong>Plate Distance:</strong> ${data.constants.plate_distance}</li>
        <li><strong>High Voltage:</strong> ${data.constants.high_voltage}</li>
        <li><strong>Low Voltage:</strong> ${data.constants.low_voltage}</li>
      </ul>
      <details>
        <summary>Raw Data</summary>
        <pre>${JSON.stringify(data, null, 2)}</pre>
      </details>
    </div>
  `;
}

// Update dimension options when equation changes
document.getElementById('equation').addEventListener('change', function() {
  const dimension = document.getElementById('dimension');
  if (this.value === 'poisson') {
    // For now, only 1D Poisson is implemented
    dimension.innerHTML = '<option value="1">1D</option>';
    dimension.value = '1';
  } else {
    dimension.innerHTML = '<option value="1">1D</option><option value="2">2D</option>';
  }
});

// Load system info on page load
document.addEventListener('DOMContentLoaded', function() {
  getInfo();
});
