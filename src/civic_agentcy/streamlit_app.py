import streamlit as st
from civic_agentcy.crew import CivicAgentcyCrew, StreamToExpander

def run_crewai_app():
    st.title("CivicAgentcy")

    topic = st.text_input('Enter a topic for analysis:', 'advertising outlook media spend 2024')

    if st.button('Analyze'):
        # Create an expander for showing progress or intermediate output
        expander = st.expander("Processing...")
        with expander:
            # Create an instance of the StreamToExpander for directing output to the expander
            stream_to_expander = StreamToExpander(expander)
            # Initialize your CivicAgentcyCrew with the output stream
            crew = CivicAgentcyCrew()

            with st.spinner('Analyzing...'):
                try:
                    # Assuming kickoff method returns a string or an object that can be converted to string
                    crew_result = crew.kickoff({'topic': topic}, output_stream=stream_to_expander)
                except Exception as e:
                    st.error(f"An error occurred during analysis: {e}")
                    return

        # Create a separate container for the final result
        final_result_container = st.container()
        with final_result_container:
            st.success('Analysis complete!')
            st.markdown("### Analysis Result", unsafe_allow_html=True)
            # Assuming crew_result is a string. If it's not, you might need to convert or format it accordingly.
            st.markdown(f"<div style='white-space: pre-wrap;'>{crew_result}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    run_crewai_app()