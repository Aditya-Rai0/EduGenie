from app.agents.base import BaseAgent, AgentInput, AgentOutput


class OrchestratorAgent(BaseAgent):

    def __init__(self):
        super().__init__(name="orchestrator", model="gpt-4o")
        self._agents: dict[str, BaseAgent] = {}

    def register_agent(self, name: str, agent: BaseAgent):
        self._agents[name] = agent

    async def run(self, input_data: AgentInput) -> AgentOutput:
        results: dict[str, AgentOutput] = {}
        for name, agent in self._agents.items():
            output = await agent.run(input_data)
            results[name] = output
        return AgentOutput(
            job_id=input_data.job_id,
            status="completed",
            result={k: v.model_dump() for k, v in results.items()},
        )
