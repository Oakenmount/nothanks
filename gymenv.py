import numpy as np
from pettingzoo import AECEnv
from pettingzoo.utils.agent_selector import agent_selector
from gymnasium import spaces

from gamestate import GameState


class CardGameEnv(AECEnv):
    def __init__(self, num_players=4):
        super(CardGameEnv, self).__init__()

        self.game_state = GameState(num_players)
        self.agents = [f"player_{i}" for i in range(num_players)]
        self.possible_agents = self.agents[:]

        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.reset()

        self.action_spaces = {i: spaces.Discrete(2) for i in self.agents}
        self.observation_spaces = {
            i: spaces.Dict(
                {
                    "observation": spaces.Box(
                        low=0, high=35, shape=(self.get_observation_space_size(),), dtype=np.uint8
                    ),
                    "action_mask": spaces.Box(low=0, high=1, shape=(2,), dtype=np.uint8),
                }
            )
            for i in range(num_players)
        }

    def get_observation_space_size(self):
        # Size of the observation space
        return self.game_state.as_vector().shape[0]

    def observe(self, agent):
        vec = self.game_state.as_vector()
        if agent == self.agent_selection:
            legal_actions = [1, self.game_state.get_player().can_skip() and 1 or 0]
        else:
            legal_actions = []
        return {"observation": vec, "action_mask": legal_actions}

    def observation_space(self, agent):
        return self.observation_spaces[agent]

    def action_space(self, agent):
        return self.action_spaces[agent]

    def step(self, action):
        if (
                self.truncations[self.agent_selection]
                or self.terminations[self.agent_selection]
        ):
            return self._was_dead_step(action)

        if action == 0:
            assert self.game_state.get_player().can_skip()
            self.game_state.skip_card()
        elif action == 1:
            self.game_state.take_card()
        else:
            raise ValueError("Invalid action")

        next_agent = self._agent_selector.next()

        over = self.game_state.is_over()

        # check if there is a winner
        if over:
            for i, agent in enumerate(self.agents):
                self.rewards[agent] = -self.game_state.players[i].score()
            winner = min(self.rewards.items(), key=lambda x: x[1])[0]
            self.rewards[winner] += 500
            self.terminations = {i: True for i in self.agents}

        self.agent_selection = next_agent

        self._accumulate_rewards()

    def reset(self, seed=None, options=None):
        # reset environment
        self.game_state = GameState(num_players=len(self.game_state.players))

        self.agents = self.possible_agents[:]
        self.rewards = {i: 0 for i in self.agents}
        self._cumulative_rewards = {name: 0 for name in self.agents}
        self.terminations = {i: False for i in self.agents}
        self.truncations = {i: False for i in self.agents}
        self.infos = {i: {} for i in self.agents}

        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.reset()


if __name__ == "__main__":
    env = CardGameEnv()
    env.reset(seed=42)

    for agent in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()

        if termination or truncation:
            action = None
        else:
            # this is where you would insert your policy
            action = env.action_space(agent).sample()
        print(reward)
        env.step(action)
    env.close()
