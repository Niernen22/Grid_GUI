import queue
import math
import random

# The "Grid" class is responsible for learning and decision-making of agents.
class Grid:
    def __init__(self, start, goal, grid_map, alpha=0.1, gamma=0.9, epsilon=0.2):
        self._start = start  # Starting position
        self._goal = goal  # Goal position
        self._width = len(grid_map[0])  # Width of the grid
        self._height = len(grid_map)  # Height of the grid
        self._grid_map = grid_map  # The grid state (obstacles, goals)

        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate

        # Initialize Q-table for each grid state
        self.q_table = {}
        for y in range(self._height):
            for x in range(self._width):
                self.q_table[(y, x)] = [0, 0, 0, 0]  # Q-values for actions (right, down, left, up)

    # Reward function that evaluates the step based on current state and action
    def reward_function(self, state):
        if state == self._goal:  # If the goal is reached
            return 1  # Positive reward
        if self._grid_map[state[0]][state[1]] == 1:  # If it hits an obstacle
            return -1  # Negative reward (penalty)
        return -0.1  # Small penalty to encourage finding the shortest path

    # Determine the neighboring states (possible moves) from the current state
    def neighbors(self, position):
        (x, y) = position
        result = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]  # Right, down, left, up
        # Filter valid neighboring states
        result = filter(self.within_bounds, result)
        result = filter(self.not_obstacle, result)
        return list(result)

    # Check if the given position is within the valid grid area
    def within_bounds(self, position):
        (x, y) = position
        return 0 <= x < self._height and 0 <= y < self._width

    # Check if the given position is not an obstacle
    def not_obstacle(self, position):
        (x, y) = position
        return not self._grid_map[x][y]  # Return True if it's not an obstacle (0)

    # Update Q-value based on the current state, action, reward, and next state
    def update_q_value(self, current_state, action, reward, next_state):
        best_future_q = max(self.q_table[next_state])  # Best future Q-value
        current_q = self.q_table[current_state][action]  # Current Q-value
        # Update Q-value using the Q-learning formula
        self.q_table[current_state][action] += self.alpha * (reward + self.gamma * best_future_q - current_q)

    # Choose an action based on epsilon-greedy strategy (exploration vs exploitation)
    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:  # Exploration (random action)
            return random.choice([0, 1, 2, 3])  # Random action choice
        else:  # Exploitation (choose the best action)
            return max(range(4), key=lambda a: self.q_table[state][a])  # Best action based on Q-table

    # Perform learning using the Q-learning algorithm
    def train(self, num_episodes):
        for _ in range(num_episodes):  # Multiple training episodes
            state = self._start  # Starting state
            while state != self._goal:  # Until the goal is reached
                action = self.choose_action(state)  # Choose action
                neighbors = self.neighbors(state)  # Get possible neighboring states
                next_state = neighbors[action] if action < len(neighbors) else state  # Determine next state

                reward = self.reward_function(next_state)  # Calculate reward
                self.update_q_value(state, action, reward, next_state)  # Update Q-values

                state = next_state  # Update state

    # Find the best path after learning
    def find_best_path(self):
        state = self._start  # Starting state
        path = [state]  # Store the path
        while state != self._goal:  # Until the goal is reached
            action = max(range(4), key=lambda a: self.q_table[state][a])  # Choose the best action
            neighbors = self.neighbors(state)  # Get possible neighboring states
            next_state = neighbors[action] if action < len(neighbors) else state  # Determine next state
            path.append(next_state)  # Update the path
            state = next_state  # Update state
        return path  # Return the best path

# Find the best path based on learned Q-values
def find_optimal_path(start, goal, grid_map):
    grid = Grid(start, goal, grid_map)  # Create the grid environment
    grid.train(1000)  # Train for 1000 episodes
    return grid.find_best_path()  # Return the best path
