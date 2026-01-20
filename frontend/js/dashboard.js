// frontend/js/dashboard.js

let trendChartInstance = null;
let ecoChartInstance = null;

//  API Base
const API_BASE = "http://127.0.0.1:5000/dashboard";

function formatNumber(val, digits = 2) {
  if (val === null || val === undefined || isNaN(val)) return "0";
  return Number(val).toFixed(digits);
}

function safeText(val, fallback = "-") {
  if (val === null || val === undefined || val === "") return fallback;
  return String(val);
}

async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return await res.json();
}

// KPI Summary
async function loadSummary(fragilityValue) {
  const url = `${API_BASE}/summary?fragility=${fragilityValue}`;
  const data = await fetchJSON(url);

  document.getElementById("totalRec").innerText = safeText(data.total, "0");
  document.getElementById("avgEco").innerText = formatNumber(data.avg_eco, 2);
  document.getElementById("avgCost").innerText = formatNumber(data.avg_cost, 3);
  document.getElementById("topMat").innerText = safeText(data.top_material, "-");

  //  Eco vs CO2 donut chart
  // We don't have avg_co2 in API. So here we show Eco% vs Remaining%
  const eco = Number(data.avg_eco) || 0;
  const remaining = Math.max(0, 100 - eco);

  const ctx = document.getElementById("ecoChart").getContext("2d");
  if (ecoChartInstance) ecoChartInstance.destroy();

  ecoChartInstance = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Avg Eco Score", "Remaining"],
      datasets: [
        {
          label: "Eco",
          data: [eco, remaining],
          backgroundColor: ["#2563eb", "#dc2626"],
          borderWidth: 0,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: "top" },
      },
      cutout: "55%",
    },
  });
}

// Top Materials Chart
async function loadTopMaterials(fragilityValue) {
  const url = `${API_BASE}/top-materials?fragility=${fragilityValue}`;
  const data = await fetchJSON(url);

  const labels = data.map((x) => x.material);
  const counts = data.map((x) => x.count);

  const ctx = document.getElementById("trendChart").getContext("2d");
  if (trendChartInstance) trendChartInstance.destroy();

  trendChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Recommendations Count",
          data: counts,
          backgroundColor: ["#2563eb", "#16a34a", "#dc2626", "#f59e0b", "#9333ea", "#0ea5e9", "#64748b"],
          borderRadius: 10,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: true },
      },
      scales: {
        y: { beginAtZero: true },
      },
    },
  });
}

// Recent Recommendations Table
async function loadRecentTable(fragilityValue) {
  // Get full history
  const url = `${API_BASE}/history`;
  let data = await fetchJSON(url);

  // If user selected fragility filter, apply filter on frontend
  if (fragilityValue !== "all") {
    data = data.filter((row) => String(row.fragility) === String(fragilityValue));
  }

  // sort newest first if timestamp exists
  data = data.sort((a, b) => {
    const ta = new Date(a.timestamp || a.time || a.datetime || 0).getTime();
    const tb = new Date(b.timestamp || b.time || b.datetime || 0).getTime();
    return tb - ta;
  });

  // take last 10
  const recent10 = data.slice(0, 10);

  const tbody = document.getElementById("recentTable");
  tbody.innerHTML = "";

  if (recent10.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="7" class="text-center text-muted">No records found</td>
      </tr>
    `;
    return;
  }

  // IMPORTANT: handle all possible column names from your CSV
  recent10.forEach((row) => {
    const timestamp =
      row.timestamp || row.time || row.datetime || row.created_at || "-";

    const weight = row.weight ?? "-";
    const volume = row.volume ?? "-";
    const fragility = row.fragility ?? "-";

    const bestMaterial =
      row.best_material || row.material || row.recommended_material || "-";

    const ecoScore =
      row.best_eco_score ?? row.eco_score ?? row.eco ?? "-";

    const costScore =
      row.best_cost_index ?? row.cost_index ?? row.cost ?? "-";

    tbody.innerHTML += `
      <tr>
        <td>${safeText(timestamp)}</td>
        <td>${safeText(weight)}</td>
        <td>${safeText(volume)}</td>
        <td>${safeText(fragility)}</td>
        <td><b>${safeText(bestMaterial)}</b></td>
        <td>${safeText(ecoScore)}</td>
        <td>${safeText(costScore)}</td>
      </tr>
    `;
  });
}

//  Load everything
async function loadDashboard() {
  const fragilityValue = document.getElementById("fragilityFilter").value;

  try {
    await loadSummary(fragilityValue);
    await loadTopMaterials(fragilityValue);
    await loadRecentTable(fragilityValue);
  } catch (err) {
    console.error(err);
    alert("Dashboard error: backend data not loading");
  }
}

// Events
document.getElementById("fragilityFilter").addEventListener("change", loadDashboard);
document.getElementById("refreshBtn").addEventListener("click", loadDashboard);

// Initial load
loadDashboard();
