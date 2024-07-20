import asyncio
import streamlit as st # type: ignore
from asyncio import sleep

import helpers.sidebar
import helpers.util
from aitools_autogen.blueprint_project8 import CoreClientProject8Example
from aitools_autogen.config import llm_config_openai as llm_config
from aitools_autogen.utils import clear_working_dir

st.set_page_config(
    page_title="Auto Code",
    page_icon="📄",
    layout="wide"
)

# Add comments to explain the purpose of the code sections

# Show sidebar
helpers.sidebar.show()



if st.session_state.get("blueprint", None) is None:
    st.session_state.blueprint = CoreClientProject8Example()


async def run_blueprint(ctr, seed: int = 42) -> str:
    await sleep(3)
    llm_config["seed"] = seed
    await st.session_state.blueprint.initiate_work(message=task)
    return st.session_state.blueprint.summary_result

blueprint_ctr, parameter_ctr = st.columns(2, gap="large")
with blueprint_ctr:
    st.markdown("# Modular Web Scraping Script Generator")
    url = st.text_input("Enter a URL to test the scraping:",
                        # value="https://raw.githubusercontent.com/OAI/OpenAPI-Specification/main/examples/v3.0/uspto.yaml")
                        value="https://realpython.com/")
    agents = st.button("Start the Scraping!", type="primary")

with parameter_ctr:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### Other Options")
    clear = st.button("Clear the autogen cache...&nbsp; ⚠️", type="secondary")
    seed = st.number_input("Enter a seed for the random number generator:", value=42)

dynamic_ctr = st.empty()
results_ctr = st.empty()

if clear:
    with results_ctr:
        st.status("Clearing the agent cache...")
    clear_working_dir("../.cache", "*")

if agents:
    with results_ctr:
        st.status("Running the Blueprint...")

    task = f"""
            I want to analyze web pages and generate Python scripts for scraping data from them. When given a URL,
examine the web page's structure and produce a Python script that can scrape key elements like titles, headers, and paragraphs.
            {url}
            """

    text = asyncio.run(run_blueprint(ctr=dynamic_ctr, seed=seed))
    st.balloons()

    with results_ctr:
        st.markdown(text)



