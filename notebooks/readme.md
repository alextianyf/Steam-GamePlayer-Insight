# Steam Game Play Analytics

This repository is dedicated to exploring **player behavior and achievement data from Steam games** using data science and machine learning. The goal is to understand how players engage with different titles, identify playstyles, and uncover insights that can inform retention, design, and progression systems.  

---

## Current Focus: *7 Days to Die (7DTD)*
We begin this journey with *7 Days to Die*, a zombie survival game. Although I’ve never personally played it, I recently became fascinated by watching live streams and wanted to use it as a case study for player analytics.  

Within `notebooks/7DTD`, you’ll find multiple analyses:  

- **Exploratory Data Analysis (EDA)** – Understanding the dataset, cleaning, and preparing features.  
- **Achievement Efficiency Regression** – Modeling how efficiently players unlock achievements relative to playtime.  
- **Player Segmentation (Clustering)** – Identifying archetypes such as generalists, crafters, explorers, combat players, and early quitters.  
- **PvE vs PvP Classification** – Testing differences in playtime and building classifiers to distinguish player types.  
- **Death vs Playtime A/B Testing (WIP)** – Investigating whether early deaths reduce overall playtime.  

---

## Future Plans
This repository will grow to include **multiple Steam games**, not just 7DTD. Each game offers unique mechanics and player behaviors, and by applying consistent analytical frameworks, we can compare how engagement differs across genres (survival, PvP, MMO, sandbox, etc.).  

Potential future directions:  
- Expanding to other survival/MMO games with rich achievement systems.  
- Building RNN/sequence models to predict achievement unlock order.  
- Detecting abnormal behavior patterns (e.g., cheaters, bots, or exploiters).  
- Comparing playstyle clusters across different games to see if archetypes are universal.  

---

## Motivation
This is a **purely personal-interest project**. I enjoy applying data science to gaming, and *7 Days to Die* was a natural starting point because I’ve recently enjoyed watching it streamed. Even without being a player myself, analyzing player data gives me a way to explore the game’s dynamics and connect statistical insights with gameplay.
