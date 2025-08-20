# Player Behavior Analytics in *7 Days to Die*

This repository is a personal research portfolio project exploring player behavior in the survival game 7 Days to Die (7DTD). The analysis combines **statistical testing**, **machine learning**, **and clustering** to uncover insights about how different playstyles affect engagement, achievement progression, and retention.

---

## Motivation

This project is driven purely by **personal interest in game analytics and player behavior modeling**. The goal is to explore how **data science methods** (statistical inference, machine learning, clustering, regression) can provide insights into **player retention**, **engagement**, and **design feedback** for complex survival games.

---

## Repository Structure

This section provides a detailed overview of the project directory structure, helping you understand where key files and resources are located.

```text
.
├── 7DTD/                     
│   ├── 01-EDA.ipynb                        # Comprehensive exploratory data analysis (EDA) on cleaned player achievement & playtime data.
│   ├── 02-efficiency-regression.ipynb      # Achievement Unlock Efficiency Modeling using polynomial regression and ensemble methods.
│   ├── 03-Player-Segmentation.ipynb        # Player Archetype Discovery via clustering (PCA, hierarchical methods, K=6 segmentation).
│   ├── 04-PvP-PvE-Classification.ipynb     # PvE vs. PvP Classification using ratio features, A/B testing, and ML models (LogReg, Random Forest).
│   ├── 05-death-playtime-ABtest.ipynb      # Work-in-progress: testing whether early death counts (in first N unlocked achievements) affect total playtime.
│   ├── clean.csv                           # Processed dataset used across the notebooks.
│   └── readme.md                           # You are here
```

---

## Completed Studies

1. **Modeling Achievement Unlock Efficiency**

   - Built baseline polynomial regression on log-transformed playtime.

   - Found **degree-3 polynomial (R² ≈ 0.96)** best explains efficiency patterns.

   - Random Forest confirmed **log_playtime**, **crafting_count**, **combat_count** as strongest predictors.

   - Showed framework could be extended to detect **abnormal progression / cheaters**.

2. **Player Segmentation & Archetypes**

   - Applied **PCA (81% variance explained)** + hierarchical clustering, K=6 clusters.

   - Identified archetypes:

     - Generalists, Crafters, Explorers, Fighters, Death-heavy quitters, Steady progress.

   - Provided actionable insights for **retention strategies**, **balancing**, and **content design**.

3. **PvE vs. PvP Classification**

   - Defined groups using player kill data:

     - Single-player (PvE only) vs. Multi-player (co-op PvE with friendly fire or PvP).

   - **A/B testing** showed multi-player players invest significantly more time.

   - Built classifiers with ratio features → **Random Forest (ROC-AUC 0.95)**, Logistic Regression (ROC-AUC 0.90).

   - Demonstrated **multiplayer as a driver of engagement**.

---

## Work in Progress

**Death vs. Playtime A/B Testing**: Studying whether early death frequency (first N unlocks) predicts shorter total playtime (frustrated quitters).

---

## Future Directions

- **Sequential Modeling of Achievement Unlocks:**

    Use **RNNs** (e.g., LSTM/GRU) to model the order and timing of achievement unlocks → predict progression paths, churn, or player archetype transitions.

- **Advanced anomaly detection** for cheaters/bots based on efficiency score and progression patterns.

- **Cross-game generalization**: extend framework to other survival or MMO titles.

---