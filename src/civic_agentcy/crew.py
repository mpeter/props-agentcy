import os
import re
import sys
from langchain_anthropic import ChatAnthropic
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from civic_agentcy.tools.search_tools import PerplexitySearch, SerpApiSearch
from civic_agentcy.tools.exa_search_tools import ExaSearchTool
from civic_agentcy.tools.you_search_tools import YouSearch, YouSummarize, YouFetchRaw, YouSearchAISnippets, YouLLMSearch, YouNewsSearch

# Define the StreamToExpander class within crew.py for reuse
class StreamToExpander:
    def __init__(self, expander):
        self.expander = expander
        self.buffer = []

    def write(self, data):
        # Filter out ANSI escape codes using a regular expression
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)
        self.buffer.append(cleaned_data)
        if "\n" in data:
            self.expander.markdown(''.join(self.buffer))
            self.buffer = []

    def flush(self):
        # This flush method is needed for compatibility with sys.stdout
        pass

# Your existing code for search tools and model
search_tool = PerplexitySearch()
serp_api_search_tool = SerpApiSearch()
you_search_tool = YouSearch()
you_summarize_tool = YouSummarize()
you_fetch_raw_tool = YouFetchRaw()
you_search_ai_snippets_tool = YouSearchAISnippets()
you_llm_search_tool = YouLLMSearch()
you_news_search_tool = YouNewsSearch()
exa_search_tool = ExaSearchTool()

# model = ChatAnthropic(model='claude-3-haiku-20240307')
model = ChatAnthropic(model='claude-3-opus-20240229')

@CrewBase
class CivicAgentcyCrew():
    """CivicAgentcy crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[serp_api_search_tool],
            verbose=True,
            llm=model
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=True,
            llm=model
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.researcher(),
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
            agent=self.reporting_analyst(),
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CivicAgentcy crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=2,
        )

    def kickoff(self, inputs, output_stream=None):
        if output_stream:
            original_stdout = sys.stdout
            sys.stdout = output_stream
        
        try:
            return self.crew().kickoff(inputs=inputs)
        finally:
            if output_stream:
                sys.stdout = original_stdout
