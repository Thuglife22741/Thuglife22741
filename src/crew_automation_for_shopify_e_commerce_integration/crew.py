from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool
from crewai_tools import SeleniumScrapingTool
from crewai_tools import WebsiteSearchTool

@CrewBase
class CrewAutomationForShopifyECommerceIntegrationCrew():
    """CrewAutomationForShopifyECommerceIntegration crew"""

    @agent
    def seo_content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['seo_content_creator'],
            tools=[ScrapeWebsiteTool(), SeleniumScrapingTool()],
        )

    @agent
    def seo_reviewer_publisher(self) -> Agent:
        return Agent(
            config=self.agents_config['seo_reviewer_publisher'],
            tools=[],
        )

    @agent
    def social_media_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['social_media_creator'],
            tools=[WebsiteSearchTool()],
        )

    @agent
    def instagram_direct_responder(self) -> Agent:
        return Agent(
            config=self.agents_config['instagram_direct_responder'],
            tools=[],
        )

    @agent
    def email_marketing_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['email_marketing_manager'],
            tools=[],
        )

    @agent
    def streamlit_dashboard_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['streamlit_dashboard_developer'],
            tools=[],
        )


    @task
    def scrape_competitor_data(self) -> Task:
        return Task(
            config=self.tasks_config['scrape_competitor_data'],
            tools=[ScrapeWebsiteTool(), SeleniumScrapingTool()],
        )

    @task
    def review_and_publish_seo_content(self) -> Task:
        return Task(
            config=self.tasks_config['review_and_publish_seo_content'],
            tools=[],
        )

    @task
    def generate_social_media_post(self) -> Task:
        return Task(
            config=self.tasks_config['generate_social_media_post'],
            tools=[WebsiteSearchTool()],
        )

    @task
    def automate_instagram_responses(self) -> Task:
        return Task(
            config=self.tasks_config['automate_instagram_responses'],
            tools=[],
        )

    @task
    def configure_email_marketing(self) -> Task:
        return Task(
            config=self.tasks_config['configure_email_marketing'],
            tools=[],
        )

    @task
    def develop_streamlit_dashboard(self) -> Task:
        return Task(
            config=self.tasks_config['develop_streamlit_dashboard'],
            tools=[],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the CrewAutomationForShopifyECommerceIntegration crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
