document.getElementById("productForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const weight = Number(document.getElementById("weight").value);
    const volume = Number(document.getElementById("volume").value);
    const fragility = Number(document.getElementById("fragility").value);

    // Validation
    if (!weight || !volume || !fragility) {
        alert("Please fill in all product details.");
        return;
    }

    if (weight < 1 || weight > 500) {
        alert("Product weight must be between 1 and 500 kg.");
        return;
    }

    if (volume < 1 || volume > 5000) {
        alert("Product volume must be between 1 and 5000 cm³.");
        return;
    }

    if (fragility < 1 || fragility > 5) {
        alert("Fragility level must be between 1 and 5.");
        return;
    }

    // Show loading spinner
    document.getElementById("loadingSection").style.display = "block";
    document.getElementById("resultSection").style.display = "none";

    const btn = document.getElementById("recommendBtn");
    btn.disabled = true;
    btn.innerHTML = "Generating Recommendation...";

    fetch("https://packagingrecommendationsystem.onrender.com/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            weight: weight,
            volume: volume,
            fragility: fragility
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Backend error");
        }
        return response.json();
    })
    .then(data => {

        // Hide loading
        document.getElementById("loadingSection").style.display = "none";

        // Enable button
        btn.disabled = false;
        btn.innerHTML = "Get AI Recommendation";

        // Show result
        document.getElementById("resultSection").style.display = "block";

        // Recommendation Card
        document.getElementById("recommendedMaterial").innerHTML = `
            <div class="fs-4 fw-bold text-success">
                ${data.best_material_name}
            </div>

            <div class="text-muted mt-1">
                Material ID: ${data.best_material}
            </div>
        `;

        document.getElementById("ecoScore").innerHTML = `
            <span class="fs-3 fw-bold text-success">
                ${data.best_eco_score}
            </span>
        `;

        document.getElementById("estimatedCost").innerHTML = `
            <div><strong>Price:</strong> ₹${data.best_price_inr}</div>
            <div><strong>Cost Index:</strong> ${data.best_cost_index}</div>
        `;

        // Ranking Table
        let rows = "";

        data.ranking.forEach((item, index) => {

            rows += `
                <tr>
                    <td class="fw-bold">${index + 1}</td>

                    <td>
                        <strong>${item.material_name}</strong><br>
                        <small class="text-muted">${item.material}</small>
                    </td>

                    <td>₹${Number(item.price_inr).toFixed(2)}</td>

                    <td>${Number(item.co2).toFixed(3)}</td>

                    <td>
                        <span class="badge bg-success">
                            ${Number(item.eco_score).toFixed(2)}
                        </span>
                    </td>
                </tr>
            `;
        });

        document.getElementById("rankingTable").innerHTML = rows;
    })
    .catch(error => {

        document.getElementById("loadingSection").style.display = "none";

        btn.disabled = false;
        btn.innerHTML = "Get AI Recommendation";

        console.error(error);

        alert("Unable to connect to the backend server. Please try again later.");
    });
});