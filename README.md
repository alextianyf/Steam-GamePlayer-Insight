# Steam Game Player Insight

This repository is dedicated to analyzing **player behavior and achievement data from Steam games**.  
The goal is to apply **data science, machine learning, and statistical analysis** to understand how players engage with different games, discover playstyle archetypes, and study the relationship between playtime, achievements, and retention.  

The project is **purely personal-interest driven**: I started with *7 Days to Die (7DTD)* because I’ve recently enjoyed watching it streamed, even though I’ve never played it myself. More games will be added in the future as case studies.

---

## Motivation

This repository is a **personal research portfolio** combining gaming and data science.  
Even without playing the games myself, I enjoy exploring how **player data tells a story** about motivation, retention, and design.  
The ultimate goal is to develop **reusable frameworks** for analyzing game engagement across different genres.  

---

## Repository Structure

This section provides a detailed overview of the project directory structure, helping you understand where key files and resources are located.

```text
.Steam-GamePlayer-Insight/
├── data/                   # Data storage and processing
│ ├── raw/                  # Original raw data (as collected)
│ ├── intermediate/         # Cleaned / partially processed datasets
│ ├── players/              # Player-level data extracts
│ └── etl/                  # ETL scripts or transformed outputs
│
├── notebooks/              # Jupyter notebooks for analysis
│ ├── 7DTD/                 # Analyses specific to 7 Days to Die
│   ├── 01-EDA.ipynb
│   ├── 02-efficiency-regression.ipynb
│   ├── 03-Player-Segmentation.ipynb
│   ├── 04-PvP-PvE-Classification.ipynb
│   ├── 05-death-playtime-ABtest.ipynb (WIP)
│   └── readme.md
│
├── sql/                    # SQL queries for database extraction or transformation
│
├── LICENSE
├── .gitignore
└── README.md # This file
```

---

## Current Focus: *7 Days to Die (7DTD)*

Within `notebooks/7DTD/`, several studies have been completed:

1. **Exploratory Data Analysis (EDA)**  
   - Cleaned, validated, and explored the dataset.  
   - Studied achievement distributions, playtime skew, and data quality issues.

2. **Achievement Efficiency Regression**  
   - Modeled efficiency score (achievements per playtime).  
   - Polynomial regression (degree 3) achieved R² ≈ 0.96.  
   - Random Forest Regression confirmed **log_playtime, crafting_count, combat_count** as key predictors.  
   - Showed potential use for **anomaly/cheater detection**.

3. **Player Segmentation (Clustering)**  
   - PCA (81% variance explained) + hierarchical clustering → **6 archetypes**:  
     - Generalists, Crafters, Explorers, Fighters, Death-heavy quitters, Steady-progress.  
   - Identified high-churn groups (death-heavy) and content-focused niches (crafters/explorers).  
   - Provided insights for **retention strategies and design balance**.

4. **PvE vs PvP Classification**  
   - Defined groups via player kill data.  
   - A/B testing showed **multi-player mode players have significantly higher playtime**.  
   - Classification models: Logistic Regression (ROC-AUC 0.90), Random Forest (ROC-AUC 0.95).  
   - Highlights the **importance of multiplayer for retention**.

5. **Death vs Playtime A/B Testing (Work-in-progress)**  
   - Investigating whether early deaths (in the first N unlocked achievements) impact long-term playtime.  
   - Aim: detect **frustrated quitters** at an early stage.

---

## Future Directions

- **More Games:** Extend the framework to additional Steam titles (MMOs, PvP shooters, sandbox survival).  
- **Sequential Modeling:** Use RNNs (LSTM/GRU) to predict achievement unlock sequences, progression paths, and churn.  
- **Cheater/Bot Detection:** Leverage efficiency scores and outlier behavior to flag abnormal players.  
- **Cross-Game Archetypes:** Compare whether playstyle clusters generalize across different genres.  

---
