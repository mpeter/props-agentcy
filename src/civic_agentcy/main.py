from civic_agentcy.crew import CivicAgentcyCrew

def run(topic):
    inputs = {'topic': topic}
    CivicAgentcyCrew().crew().kickoff(inputs=inputs)