from typing import Optional
import asyncio
import aitools_autogen.utils as utils
from aitools_autogen.agents import WebPageScraperAgent
from aitools_autogen.blueprint import Blueprint
from aitools_autogen.config import llm_config_openai as llm_config, config_list_openai as config_list, WORKING_DIR
from autogen import ConversableAgent

class CoreClientProject8Example(Blueprint):

    def __init__(self, work_dir: Optional[str] = WORKING_DIR):
        super().__init__([], config_list=config_list, llm_config=llm_config)
        self._work_dir = work_dir or "code"
        self._summary_result: Optional[str] = None

    @property
    def summary_result(self) -> str | None:
        """The getter for the 'summary_result' attribute."""
        return self._summary_result

    @property
    def work_dir(self) -> str:
        """The getter for the 'work_dir' attribute."""
        return self._work_dir

    async def initiate_work(self, message: str):
        utils.clear_working_dir(self._work_dir)
        agent0 = ConversableAgent("a0",
                                  max_consecutive_auto_reply=0,
                                  llm_config=False,
                                  human_input_mode="NEVER")

        scraper_agent = WebPageScraperAgent()

        summary_agent = ConversableAgent("summary_agent",
                                         max_consecutive_auto_reply=6,
                                         llm_config=llm_config,
                                         human_input_mode="NEVER",
                                         code_execution_config=False,
                                         function_map=None,
                                         system_message="""You are a helpful AI assistant.
    Your task is to analyze web pages and generate Python scripts for scraping data from them. When given a URL, examine the web page's structure and produce a Python script that can scrape key elements like titles, headers, and paragraphs.
    Let's generate the script in a structured format:
    - The script should initialize necessary libraries and setup the scraping session.
    - Include comments within the script to explain each section of the code.
    - Extract basic elements like page title, headers (h1, h2), and all paragraphs.
    - Output should be neatly formatted and stored in variables or displayed directly.
    - Include error handling to manage cases when the webpage is not accessible or elements are missing.
    - Return `None` if the URL is not valid or the content cannot be scraped effectively.

            """)

        aiohttp_client_agent = ConversableAgent("aiohttp_client_agent",
                                                max_consecutive_auto_reply=6,
                                                llm_config=llm_config,
                                                human_input_mode="NEVER",
                                                code_execution_config=False,
                                                function_map=None,
                                                system_message="""
You are a software developer specializing in Python, focusing on data collection for web-based projects.
    Your task is to write Python scripts that scrape web content effectively using the BeautifulSoup and requests libraries.

    When you receive a URL, your script should expect that URL to point to a web page from which data needs to be extracted.

    Generate Python scripts that:
    - **fetch_content.py**: Initializes a scraping session using requests to fetch the page content. This module should handle network exceptions and return the HTML content.
    - **parse_content.py**: Parses the fetched content using BeautifulSoup. This module should extract key details such as the page title, headers (h1, h2, etc.), and paragraphs and return a structured dictionary of these elements.
    - **display_results.py**: Takes the parsed data and prints it in a readable format. This module should format the output nicely to make it easy to read.
    - **main.py**: Coordinates the use of the other modules, asks for user input for the URL, and manages the flow from fetching to displaying the data.

    Organize your code into functions or classes in each module to handle different aspects of scraping:
    - Use proper exception handling in each module to deal with potential errors, such as network issues or HTML parsing errors.
    - Ensure each script can be run as a standalone module for testing purposes but also works well when imported into `main.py`.

    The output scripts must be stored in the `coding` directory and include:
    - Clear comments in the code to explain the functionality of each part, making it educational for beginners.
    Always put `# filename: /<filename>` as the first line of each code block.

    Your generated scripts should not require any additional configuration or modification by the end-user to be executed.
    Do not suggest incomplete code which requires users to modify.

    Generate multiple Python script files in one response to demonstrate how the scraping tasks are separated into different modules, enhancing maintainability and readability.


        """)

        agent0.initiate_chat(scraper_agent, True, True, message=message)

        message = agent0.last_message(scraper_agent)

        agent0.initiate_chat(summary_agent, True, True, message=message)

        api_description_message = agent0.last_message(summary_agent)

        # api_description = api_description_message["content"]
        # print(api_description)

        agent0.initiate_chat(aiohttp_client_agent, True, True, message=api_description_message)

        llm_message = agent0.last_message(aiohttp_client_agent)["content"]
        utils.save_code_files(llm_message, self.work_dir)

        self._summary_result = utils.summarize_files(self.work_dir)

if __name__ == "__main__":
    # Create an instance of CoreClientProject8Example
    project = CoreClientProject8Example()

    # Define the message as a URL from which to scrape data
    message = "https://realpython.com/"

    # Run the initiate_work method to perform the web scraping
    asyncio.run(project.initiate_work(message))

    # Print the result which should include details about the scraping results or the path to the generated script
    print(project.summary_result)

