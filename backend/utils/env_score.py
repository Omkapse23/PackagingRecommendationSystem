def calculate_env_score(material):
    scores = {
        "Bubble Wrap": 60,
        "Corrugated Box": 80,
        "Paper Packaging": 90
    }
    return scores.get(material, 50)
