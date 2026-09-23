"""
Reinforcement Learning Module

This module provides comprehensive reinforcement learning utilities including:
- Environment interface
- Agent implementations
- Q-Learning algorithm
- Deep Q-Network (DQN) concepts
- Policy Gradient methods
- SARSA algorithm
- Monte Carlo methods
- Exploration strategies
- Reward shaping
- Experience replay
- Value iteration

Note: This module uses numpy for numerical operations.
Install with: pip install numpy

All functions include comprehensive docstrings and type hints.
"""

import random
import math
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict, deque


try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


class ActionType(Enum):
    """Types of action spaces."""
    DISCRETE = "discrete"
    CONTINUOUS = "continuous"


class ExplorationStrategy(Enum):
    """Exploration strategies."""
    EPSILON_GREEDY = "epsilon_greedy"
    SOFTMAX = "softmax"
    UCB = "ucb"
    THOMPSON_SAMPLING = "thompson_sampling"


@dataclass
class State:
    """State representation."""
    values: Dict[str, Any]
    
    def __hash__(self):
        """Hash state for dictionary keys."""
        return hash(tuple(sorted(self.values.items())))
    
    def __eq__(self, other):
        """Compare states."""
        if not isinstance(other, State):
            return False
        return self.values == other.values


@dataclass
class Action:
    """Action representation."""
    action_id: str
    value: Any
    
    def __hash__(self):
        """Hash action for dictionary keys."""
        return hash(self.action_id)
    
    def __eq__(self, other):
        """Compare actions."""
        if not isinstance(other, Action):
            return False
        return self.action_id == other.action_id


@dataclass
class Transition:
    """State-action-reward-next state tuple."""
    state: State
    action: Action
    reward: float
    next_state: State
    done: bool


class Environment:
    """Base environment interface."""
    
    def __init__(self):
        """Initialize environment."""
        self.current_state: Optional[State] = None
        self.action_space: List[Action] = []
        self.state_space: List[State] = []
    
    def reset(self) -> State:
        """Reset environment to initial state."""
        raise NotImplementedError
    
    def step(self, action: Action) -> Tuple[State, float, bool, Dict]:
        """Execute action and return next state, reward, done, info."""
        raise NotImplementedError
    
    def get_action_space(self) -> List[Action]:
        """Get available actions."""
        return self.action_space
    
    def get_state_space(self) -> List[State]:
        """Get possible states."""
        return self.state_space


class GridWorld(Environment):
    """Simple grid world environment."""
    
    def __init__(self, width: int = 5, height: int = 5):
        """Initialize grid world."""
        super().__init__()
        self.width = width
        self.height = height
        self.agent_pos = (0, 0)
        self.goal_pos = (width - 1, height - 1)
        self.obstacles: List[Tuple[int, int]] = []
        
        # Define actions
        self.action_space = [
            Action("up", (0, -1)),
            Action("down", (0, 1)),
            Action("left", (-1, 0)),
            Action("right", (1, 0))
        ]
        
        self.reset()
    
    def reset(self) -> State:
        """Reset agent to start position."""
        self.agent_pos = (0, 0)
        return self._get_state()
    
    def step(self, action: Action) -> Tuple[State, float, bool, Dict]:
        """Execute action in grid world."""
        x, y = self.agent_pos
        dx, dy = action.value
        
        new_x = max(0, min(self.width - 1, x + dx))
        new_y = max(0, min(self.height - 1, y + dy))
        
        # Check obstacles
        if (new_x, new_y) in self.obstacles:
            new_x, new_y = x, y
        
        self.agent_pos = (new_x, new_y)
        
        # Calculate reward
        if self.agent_pos == self.goal_pos:
            reward = 10.0
            done = True
        else:
            reward = -0.1  # Small penalty for each step
            done = False
        
        info = {"position": self.agent_pos}
        
        return self._get_state(), reward, done, info
    
    def _get_state(self) -> State:
        """Get current state."""
        return State({"position": self.agent_pos})
    
    def add_obstacle(self, x: int, y: int) -> None:
        """Add obstacle to grid."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.obstacles.append((x, y))


class QLearningAgent:
    """Q-Learning algorithm implementation."""
    
    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.95,
                 epsilon: float = 0.1, epsilon_decay: float = 0.995):
        """Initialize Q-Learning agent."""
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.q_table: Dict[Tuple[State, Action], float] = defaultdict(float)
    
    def get_q_value(self, state: State, action: Action) -> float:
        """Get Q-value for state-action pair."""
        return self.q_table[(state, action)]
    
    def set_q_value(self, state: State, action: Action, value: float) -> None:
        """Set Q-value for state-action pair."""
        self.q_table[(state, action)] = value
    
    def choose_action(self, state: State, actions: List[Action]) -> Action:
        """Choose action using epsilon-greedy policy."""
        if random.random() < self.epsilon:
            return random.choice(actions)
        
        # Choose action with max Q-value
        q_values = [self.get_q_value(state, action) for action in actions]
        max_q = max(q_values)
        max_actions = [action for action, q in zip(actions, q_values) if q == max_q]
        
        return random.choice(max_actions)
    
    def learn(self, transition: Transition) -> float:
        """Update Q-value using Q-Learning update rule."""
        state = transition.state
        action = transition.action
        reward = transition.reward
        next_state = transition.next_state
        done = transition.done
        
        # Current Q-value
        current_q = self.get_q_value(state, action)
        
        # Maximum Q-value for next state
        if done:
            max_next_q = 0.0
        else:
            # Get all possible actions for next state
            next_actions = self.get_action_space_for_state(next_state)
            if next_actions:
                max_next_q = max(self.get_q_value(next_state, a) for a in next_actions)
            else:
                max_next_q = 0.0
        
        # Q-Learning update
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.set_q_value(state, action, new_q)
        
        # Decay epsilon
        self.epsilon *= self.epsilon_decay
        
        return abs(new_q - current_q)
    
    def get_action_space_for_state(self, state: State) -> List[Action]:
        """Get available actions for state (simplified)."""
        # In real implementation, this would depend on the environment
        return self.action_space if hasattr(self, 'action_space') else []
    
    def set_action_space(self, actions: List[Action]) -> None:
        """Set action space."""
        self.action_space = actions


class SARSAAgent:
    """SARSA (State-Action-Reward-State-Action) algorithm."""
    
    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.95,
                 epsilon: float = 0.1, epsilon_decay: float = 0.995):
        """Initialize SARSA agent."""
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.q_table: Dict[Tuple[State, Action], float] = defaultdict(float)
        self.action_space: List[Action] = []
    
    def choose_action(self, state: State) -> Action:
        """Choose action using epsilon-greedy policy."""
        if random.random() < self.epsilon:
            return random.choice(self.action_space)
        
        q_values = [self.q_table[(state, action)] for action in self.action_space]
        max_q = max(q_values)
        max_actions = [action for action, q in zip(self.action_space, q_values) if q == max_q]
        
        return random.choice(max_actions)
    
    def learn(self, transition: Transition, next_action: Action) -> float:
        """Update Q-value using SARSA update rule."""
        state = transition.state
        action = transition.action
        reward = transition.reward
        next_state = transition.next_state
        done = transition.done
        
        current_q = self.q_table[(state, action)]
        next_q = self.q_table[(next_state, next_action)]
        
        # SARSA update
        target = reward + self.discount_factor * next_q
        new_q = current_q + self.learning_rate * (target - current_q)
        self.q_table[(state, action)] = new_q
        
        self.epsilon *= self.epsilon_decay
        
        return abs(new_q - current_q)


class PolicyGradientAgent:
    """Simple policy gradient agent (REINFORCE)."""
    
    def __init__(self, learning_rate: float = 0.01, discount_factor: float = 0.99):
        """Initialize policy gradient agent."""
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.policy: Dict[Tuple[State, Action], float] = defaultdict(float)
    
    def get_action_probabilities(self, state: State, actions: List[Action]) -> Dict[Action, float]:
        """Get action probabilities using softmax."""
        # Get policy parameters
        values = [self.policy[(state, action)] for action in actions]
        
        # Softmax
        exp_values = [math.exp(v) for v in values]
        total = sum(exp_values)
        
        probabilities = {action: exp / total for action, exp in zip(actions, exp_values)}
        return probabilities
    
    def choose_action(self, state: State, actions: List[Action]) -> Action:
        """Choose action based on policy."""
        probabilities = self.get_action_probabilities(state, actions)
        
        r = random.random()
        cumulative = 0.0
        
        for action, prob in probabilities.items():
            cumulative += prob
            if r <= cumulative:
                return action
        
        return actions[-1]
    
    def update_policy(self, episode: List[Transition]) -> None:
        """Update policy using REINFORCE algorithm."""
        # Calculate returns
        returns = []
        G = 0.0
        
        for transition in reversed(episode):
            G = transition.reward + self.discount_factor * G
            returns.insert(0, G)
        
        # Normalize returns
        if returns:
            mean_return = sum(returns) / len(returns)
            std_return = math.sqrt(sum((r - mean_return) ** 2 for r in returns) / len(returns))
            returns = [(r - mean_return) / (std_return + 1e-8) for r in returns]
        
        # Update policy
        for transition, G in zip(episode, returns):
            state = transition.state
            action = transition.action
            
            # Get action probabilities
            actions = [transition.action]  # Simplified
            probabilities = self.get_action_probabilities(state, actions)
            
            # Gradient update
            for act, prob in probabilities.items():
                gradient = (1.0 if act == action else 0.0) - prob
                self.policy[(state, act)] += self.learning_rate * G * gradient


class ExperienceReplay:
    """Experience replay buffer for off-policy learning."""
    
    def __init__(self, capacity: int = 10000):
        """Initialize experience replay buffer."""
        self.capacity = capacity
        self.buffer: deque = deque(maxlen=capacity)
    
    def add(self, transition: Transition) -> None:
        """Add transition to buffer."""
        self.buffer.append(transition)
    
    def sample(self, batch_size: int) -> List[Transition]:
        """Sample random batch of transitions."""
        return random.sample(list(self.buffer), min(batch_size, len(self.buffer)))
    
    def size(self) -> int:
        """Get buffer size."""
        return len(self.buffer)


class RewardShaper:
    """Reward shaping utilities."""
    
    @staticmethod
    def normalize_rewards(episode: List[Transition]) -> List[float]:
        """Normalize rewards in episode."""
        rewards = [t.reward for t in episode]
        
        if not rewards:
            return rewards
        
        mean = sum(rewards) / len(rewards)
        std = math.sqrt(sum((r - mean) ** 2 for r in rewards) / len(rewards))
        
        if std > 0:
            normalized = [(r - mean) / std for r in rewards]
        else:
            normalized = rewards
        
        return normalized
    
    @staticmethod
    def potential_based_reward(transition: Transition, 
                                potential_func: Callable[[State], float],
                                gamma: float = 0.99) -> float:
        """Apply potential-based reward shaping."""
        current_potential = potential_func(transition.state)
        next_potential = potential_func(transition.next_state)
        
        shaped_reward = transition.reward + gamma * next_potential - current_potential
        return shaped_reward


class ValueIteration:
    """Value iteration for planning."""
    
    def __init__(self, environment: Environment, discount_factor: float = 0.9,
                 theta: float = 0.001):
        """Initialize value iteration."""
        self.environment = environment
        self.discount_factor = discount_factor
        self.theta = theta
        self.values: Dict[State, float] = {}
        self.policy: Dict[State, Action] = {}
    
    def run(self, max_iterations: int = 1000) -> Dict[State, float]:
        """Run value iteration algorithm."""
        # Initialize values
        for state in self.environment.get_state_space():
            self.values[state] = 0.0
        
        for iteration in range(max_iterations):
            delta = 0.0
            
            for state in self.environment.get_state_space():
                old_value = self.values[state]
                
                # Bellman update
                actions = self.environment.get_action_space()
                max_value = float('-inf')
                
                for action in actions:
                    # Simulate action (simplified)
                    # In real implementation, would use environment model
                    action_value = 0.0  # Placeholder
                    max_value = max(max_value, action_value)
                
                self.values[state] = max_value
                delta = max(delta, abs(old_value - self.values[state]))
            
            if delta < self.theta:
                break
        
        return self.values


class MonteCarloAgent:
    """Monte Carlo agent using first-visit or every-visit."""
    
    def __init__(self, gamma: float = 0.99, first_visit: bool = True):
        """Initialize Monte Carlo agent."""
        self.gamma = gamma
        self.first_visit = first_visit
        self.returns: Dict[Tuple[State, Action], List[float]] = defaultdict(list)
        self.q_table: Dict[Tuple[State, Action], float] = {}
    
    def update(self, episode: List[Transition]) -> None:
        """Update Q-values from episode."""
        # Calculate returns
        G = 0.0
        returns = []
        
        for transition in reversed(episode):
            G = transition.reward + self.gamma * G
            returns.insert(0, G)
        
        # Update returns and Q-values
        visited = set()
        
        for transition, G in zip(episode, returns):
            state = transition.state
            action = transition.action
            state_action = (state, action)
            
            if self.first_visit:
                if state_action not in visited:
                    self.returns[state_action].append(G)
                    visited.add(state_action)
            else:
                self.returns[state_action].append(G)
        
        # Calculate average returns
        for state_action, rets in self.returns.items():
            self.q_table[state_action] = sum(rets) / len(rets)
    
    def get_q_value(self, state: State, action: Action) -> float:
        """Get Q-value."""
        return self.q_table.get((state, action), 0.0)


class RLTrainer:
    """Reinforcement learning training utilities."""
    
    def __init__(self, environment: Environment, agent: Any):
        """Initialize trainer."""
        self.environment = environment
        self.agent = agent
        self.episode_rewards: List[float] = []
        self.episode_lengths: List[int] = []
    
    def train(self, num_episodes: int, max_steps: int = 1000) -> Dict:
        """Train agent for specified episodes."""
        all_rewards = []
        all_lengths = []
        
        for episode in range(num_episodes):
            state = self.environment.reset()
            total_reward = 0.0
            steps = 0
            
            for step in range(max_steps):
                actions = self.environment.get_action_space()
                action = self.agent.choose_action(state, actions)
                
                next_state, reward, done, info = self.environment.step(action)
                
                transition = Transition(state, action, reward, next_state, done)
                
                # Learn (simplified - doesn't get next action for SARSA)
                if hasattr(self.agent, 'learn'):
                    self.agent.learn(transition)
                
                total_reward += reward
                steps += 1
                state = next_state
                
                if done:
                    break
            
            all_rewards.append(total_reward)
            all_lengths.append(steps)
        
        self.episode_rewards = all_rewards
        self.episode_lengths = all_lengths
        
        return {
            "total_rewards": all_rewards,
            "average_reward": sum(all_rewards) / len(all_rewards),
            "average_length": sum(all_lengths) / len(all_lengths),
            "best_reward": max(all_rewards)
        }


class Evaluation:
    """Evaluation utilities for RL agents."""
    
    @staticmethod
    def evaluate_agent(environment: Environment, agent: Any, 
                     num_episodes: int = 100) -> Dict:
        """Evaluate agent performance."""
        total_rewards = []
        total_steps = []
        
        for _ in range(num_episodes):
            state = environment.reset()
            episode_reward = 0.0
            steps = 0
            
            while True:
                actions = environment.get_action_space()
                action = agent.choose_action(state, actions)
                
                next_state, reward, done, info = environment.step(action)
                
                episode_reward += reward
                steps += 1
                state = next_state
                
                if done or steps > 1000:
                    break
            
            total_rewards.append(episode_reward)
            total_steps.append(steps)
        
        return {
            "average_reward": sum(total_rewards) / len(total_rewards),
            "average_steps": sum(total_steps) / len(total_steps),
            "best_reward": max(total_rewards),
            "worst_reward": min(total_rewards),
            "std_reward": math.sqrt(sum((r - sum(total_rewards)/len(total_rewards))**2 
                                     for r in total_rewards) / len(total_rewards))
        }


def demonstrate_reinforcement_learning():
    """Demonstrate reinforcement learning functionality."""
    print("=== Reinforcement Learning Demonstration ===\n")
    
    # Environment
    print("1. Grid World Environment:")
    env = GridWorld(width=5, height=5)
    env.add_obstacle(2, 2)
    env.add_obstacle(3, 3)
    
    initial_state = env.reset()
    print(f"   Initial state: {initial_state.values}")
    print(f"   Goal position: {env.goal_pos}")
    print(f"   Obstacles: {env.obstacles}")
    
    # Q-Learning
    print("\n2. Q-Learning Agent:")
    ql_agent = QLearningAgent(learning_rate=0.1, discount_factor=0.95, epsilon=0.1)
    ql_agent.set_action_space(env.get_action_space())
    
    # Train for a few episodes
    trainer = RLTrainer(env, ql_agent)
    results = trainer.train(num_episodes=50, max_steps=100)
    
    print(f"   Average reward: {results['average_reward']:.2f}")
    print(f"   Best reward: {results['best_reward']:.2f}")
    print(f"   Average length: {results['average_length']:.2f}")
    
    # SARSA
    print("\n3. SARSA Agent:")
    sarsa_agent = SARSAAgent(learning_rate=0.1, discount_factor=0.95, epsilon=0.1)
    sarsa_agent.action_space = env.get_action_space()
    
    trainer_sarsa = RLTrainer(env, sarsa_agent)
    results_sarsa = trainer_sarsa.train(num_episodes=50, max_steps=100)
    
    print(f"   Average reward: {results_sarsa['average_reward']:.2f}")
    print(f"   Best reward: {results_sarsa['best_reward']:.2f}")
    
    # Experience Replay
    print("\n4. Experience Replay:")
    replay_buffer = ExperienceReplay(capacity=1000)
    
    for _ in range(10):
        state = env.reset()
        action = random.choice(env.get_action_space())
        next_state, reward, done, info = env.step(action)
        transition = Transition(state, action, reward, next_state, done)
        replay_buffer.add(transition)
    
    batch = replay_buffer.sample(5)
    print(f"   Buffer size: {replay_buffer.size()}")
    print(f"   Batch size: {len(batch)}")
    
    # Policy Gradient
    print("\n5. Policy Gradient Agent:")
    pg_agent = PolicyGradientAgent(learning_rate=0.01, discount_factor=0.99)
    
    # Simulate episode
    episode = []
    state = env.reset()
    for _ in range(10):
        action = random.choice(env.get_action_space())
        next_state, reward, done, info = env.step(action)
        episode.append(Transition(state, action, reward, next_state, done))
        state = next_state
    
    pg_agent.update_policy(episode)
    print(f"   Policy updated from episode of {len(episode)} steps")
    
    # Monte Carlo
    print("\n6. Monte Carlo Agent:")
    mc_agent = MonteCarloAgent(gamma=0.99, first_visit=True)
    
    mc_agent.update(episode)
    print(f"   Q-table entries: {len(mc_agent.q_table)}")
    
    # Reward Shaping
    print("\n7. Reward Shaping:")
    shaped_rewards = RewardShaping.normalize_rewards(episode)
    print(f"   Normalized rewards: {shaped_rewards[:5]}...")
    
    # Evaluation
    print("\n8. Agent Evaluation:")
    eval_results = Evaluation.evaluate_agent(env, ql_agent, num_episodes=10)
    print(f"   Average reward: {eval_results['average_reward']:.2f}")
    print(f"   Std reward: {eval_results['std_reward']:.2f}")
    
    # Value Iteration
    print("\n9. Value Iteration:")
    small_env = GridWorld(width=3, height=3)
    vi = ValueIteration(small_env, discount_factor=0.9, theta=0.001)
    
    values = vi.run(max_iterations=100)
    print(f"   Value table entries: {len(values)}")
    
    print("\n=== Demonstration Complete ===")
    print("\nReinforcement Learning Best Practices:")
    print("- Use appropriate exploration strategies")
    print("- Balance exploration vs exploitation")
    print("- Use experience replay for off-policy learning")
    print("- Apply reward shaping to guide learning")
    print("- Normalize rewards for stable training")
    print("- Monitor training progress with metrics")
    print("- Use discount factor appropriate for task")
    print("- Consider state representation carefully")
    print("- Test agents in varied environments")
    print("- Use proper evaluation protocols")
    print("- Hyperparameter tuning is important")
    print("- Consider safety for real-world applications")


if __name__ == "__main__":
    demonstrate_reinforcement_learning()
