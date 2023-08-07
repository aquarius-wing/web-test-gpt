from typing import List, Dict, Tuple


class BaseAgent:
    def __init__(self, execute_after_agents: List['BaseAgent'] = []):
        self.execute_after_agents = execute_after_agents

    def execute(self):
        for agent in self.execute_after_agents:
            agent.execute()
