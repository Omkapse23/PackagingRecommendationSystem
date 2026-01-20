document.getElementById("productForm").addEventListener("submit", function (e) {
    e.preventDefault();

    // Read input values
    const weight = document.getElementById("weight").value;
    const volume = document.getElementById("volume").value;
    const fragility = document.getElementById("fragility").value;

    // Basic validation
    if (weight === "" || volume === "" || fragility === "") {
        alert("Please enter all input values.");
        return;
    }

    fetch("https://packagingrecommendationsystem-1.onrender.com/predict", {
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

            // Show recommended material (Name + ID)
            document.getElementById("recommendedMaterial").innerText =
                "Material: " + data.best_material_name + " (" + data.best_material + ")";

            // Show eco score
            document.getElementById("ecoScore").innerText =
                "Eco Score: " + data.best_eco_score;

            // Show cost index
            document.getElementById("estimatedCost").innerText =
                "Price (₹): " + data.best_price_inr + " | Cost Index: " + data.best_cost_index;

            // Fill ranking table
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
            alert("Error connecting frontend with backend");
        });
});
