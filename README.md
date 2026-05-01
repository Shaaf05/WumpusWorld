# Wumpus World AI Explorer

A web-based **Wumpus World AI simulation** built with **Python Flask**, HTML, CSS, and JavaScript.  
This project demonstrates how an intelligent agent explores an unknown grid environment, detects danger using percepts, marks safe and risky cells, and attempts to find the gold while avoiding pits and the Wumpus.

---

## Project Overview

Wumpus World is a classic Artificial Intelligence problem where an agent must move through a grid-based environment. The world contains:

- A hidden Wumpus
- Random pits
- A gold location
- Breeze percepts near pits
- Stench percepts near the Wumpus
- Safe and dangerous cell inference

The agent starts from the top-left corner of the grid and uses basic knowledge-based reasoning to decide which cells are safe to explore.

---

## Features

- Interactive Wumpus World simulation
- Flask backend for game logic
- Random world generation
- Adjustable grid size
- AI agent movement
- Safe and danger cell marking
- Breeze and stench percept detection
- Real-time game state updates
- Start and stop controls
- Clean web-based user interface

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web server and API routes |
| HTML | Page structure |
| CSS | User interface styling |
| JavaScript | Frontend logic and visualization |
| Threading | Background agent execution |
| JSON | Communication between frontend and backend |

---

## Project Structure

```text
Wumpus-World-AI-Explorer/
│
├── app.py
├── index.html
├── README.md
└── screenshots/
    └── interface.png
