document.getElementById("productForm").addEventListener("submit", function (e) {
    e.preventDefault();

    // Read input values
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

        // Show result section
        document.getElementById("resultSection").style.display = "block";

        // Recommended Material
        document.getElementById("recommendedMaterial").innerText =
            "Material: " + data.best_material_name + " (" + data.best_material + ")";

        // Eco Score
        document.getElementById("ecoScore").innerText =
            "Eco Score: " + data.best_eco_score;

        // Cost
        document.getElementById("estimatedCost").innerText =
            "Price (₹): " + data.best_price_inr +
            " | Cost Index: " + data.best_cost_index;

        // Ranking Table
        let rows = "";

        data.ranking.forEach((item, index) => {

            rows += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${item.material_name} (${item.material})</td>
                    <td>₹${item.price_inr}</td>
                    <td>${item.co2}</td>
                    <td>${item.eco_score}</td>
                </tr>
            `;
        });

        document.getElementById("rankingTable").innerHTML = rows;
    })
    .catch(error => {
        console.error(error);
        alert("Error connecting frontend with backend.");
    });
});