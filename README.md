# Steam-GamePlayer-Insight

## 🎯 Project Objectives

This project focuses on three main objectives:

1. **🧑‍💻 Player Insight**  
   Understand what kinds of players exist (e.g. achievers, explorers, casuals) by analyzing game ownership, playtime, and achievement profiles.

2. **🏆 Achievement Prediction**  
   Given a user’s gameplay history, can we predict which achievements they’re likely to unlock next?

3. **📈 Retention Modeling**  
   Estimate which factors contribute to whether a player continues playing a game or churns early.

---

## Why Analyze Player Behavior?

Steam games offer a rich ecosystem for behavioral analytics. From playtime and session patterns to achievement progression, each signal helps us understand:

- Which types of players unlock certain achievements  
- How player behaviors cluster into gameplay archetypes  
- What early in-game milestones predict long-term retention  
- How game design choices influence engagement and difficulty

This ETL system is designed to provide the clean, reliable datasets that downstream analysis depends on.

---

## Game Selection Rationale

To support a diverse range of player behaviors and game mechanics, the full project will eventually include several games across different genres, chosen based on:

- A large, active player base  
- A rich, structured achievement system  
- Distinct gameplay and progression mechanics  
- Compatibility with Steam's public API format  

However, this repository currently focuses on one title:

### 7 Days to Die

- **Genre**: Open-World Sandbox Survival (Crafting, Exploration, Combat)

- **Why Start Here?**  
  *7 Days to Die* features open-ended survival gameplay and a broad achievement system that reflects various player behaviors — from zombie combat to base-building. It provides strong analytical signals for clustering, prediction, and early-game survival studies.

- **Personal Connection**  
  I’ve followed this game’s development and community for years, and its strategic depth and variety make it a compelling case for player insight research.

- **Analytical Features**  
  The Steam achievement system tracks key behaviors like:
  - Crafting volume (e.g., tools, structures)
  - Combat milestones (e.g., zombie/player kills)
  - Exploration and survival (e.g., distance traveled, longest life lived)

  These data points enable us to:
  - Segment players by in-game behavior  
  - Predict future achievements  
  - Study early factors that influence retention  

---