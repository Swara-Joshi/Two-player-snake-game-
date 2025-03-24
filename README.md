# Yellow Snake Game AI

This project implements an AI for the Yellow Snake in a two-player game involving both a Yellow Snake and a Red Snake. The Yellow Snake uses **A* search algorithm**, **manhattan distance**, and several strategies for movement, eating apples, avoiding oscillation, and predicting the opponent's next move.

The project involves networking using **socket programming** and simulates real-time decision-making for the Yellow Snake.

## Features

- **A* Pathfinding** for optimal movement.
- **Opponent Prediction** for Red Snake's next moves.
- **Oscillation Detection** to avoid repetitive behavior.
- **Post-Apple Strategy** to stay in a fixed direction after eating the apple.
- **Server-Client Communication** using **Socket Programming**.

## Requirements

- Python 3.x
- `socket` module (comes with Python)
- `ast` module (comes with Python)
- `heapq` module (comes with Python)
- `random` module (comes with Python)

## Installation

To use the project, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/yellow-snake-ai.git
    ```

2. **Navigate to the project directory**:
    ```bash
    cd yellow-snake-ai
    ```

3. **Install dependencies** (if any additional libraries are needed, they will be listed in requirements.txt, but for this project no extra dependencies are required).

    ```bash
    pip install -r requirements.txt
    ```

## How to Run

1. **Start the Server**:
    Run the server that listens for the client connection and handles movement decisions for the Yellow Snake:
    ```bash
    python server.py
    ```

2. **Connect the Client**:
    You'll need a game client that can connect to the server. Use a basic socket-based client or modify it according to your needs.

## Game Logic

- The **Yellow Snake** uses **A* algorithm** to navigate and determine the best path towards the apple, while avoiding the Red Snake.
- **Oscillation detection** is implemented to avoid unnecessary back-and-forth movement.
- **Opponent prediction** is utilized to anticipate the Red Snake's next move and avoid dangerous areas.
- The Yellow Snake adjusts its movement based on proximity to the apple and other conditions (such as eating apples).

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

