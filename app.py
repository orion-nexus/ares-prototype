import streamlit as st
import pandas as pd

# Load decision steps from CSV files
def load_decision_steps(file_path):
    df = pd.read_csv(file_path)
    # Fill empty milestones with the last non-empty milestone
    df['Milestone'] = df['Milestone'].ffill()
    return df

# Streamlit App UI
def main():
    # Set the page title and icon
    st.set_page_config(page_title="ARES - Automated Resource and Efficiency System", page_icon="🚀")

    # Sidebar with title, subheader, and process selection
    with st.sidebar:
        st.title("ARES 🚀")
        st.subheader("Automated Resource and Efficiency System")

        # Adding Material Icons
        st.header(":material/settings: Process Selection")

        process_options = [
            "Project Management",
            "HR Management",
            "Team Management",
            "Conflict Management",
            "Confidential Informational Management",
            "Product Development Management"
        ]
        process_selection = st.selectbox("Select a process:", process_options)
        
        st.warning("Note: changing the selected process will reset the decision steps.")

    # Show the title of the selected process in the main area
    st.header(f"Selected Process: {process_selection}")

    # Load decision steps from the corresponding CSV file
    file_mapping = {
        "Project Management": "project_management.csv",
        "HR Management": "hr_management.csv",
        "Team Management": "team_management.csv",
        "Conflict Management": "conflict_management.csv",
        "Confidential Informational Management": "confidential_information.csv",
        "Product Development Management": "product_development.csv"
    }

    # Clear history if the process selection changes
    if 'previous_selection' not in st.session_state or st.session_state['previous_selection'] != process_selection:
        st.session_state['current_step'] = 0
        st.session_state['responses'] = []
        st.session_state['previous_selection'] = process_selection

    if process_selection in file_mapping:
        decision_steps_df = load_decision_steps(file_mapping[process_selection])

        if 'current_step' not in st.session_state:
            st.session_state['current_step'] = 0
        if 'responses' not in st.session_state:
            st.session_state['responses'] = []

        current_step = st.session_state['current_step']
        s = current_step + 1

        for i in range(current_step):
            row = decision_steps_df.iloc[i]
            previous_milestone = decision_steps_df.iloc[i - 1]['Milestone']
            if i == 0 or row['Milestone'] != previous_milestone:
                st.subheader(f"Milestone: {row['Milestone']}")
            st.write(f"##### Step: {row['Step']}")
            st.write(f"Your Response: {st.session_state['responses'][i]}")
            if st.session_state['responses'][i] == 'Yes':
                st.write(f"Recommendation: {row['Yes']}")
            else:
                st.write(f"Recommendation: {row['No']}")

        if current_step < len(decision_steps_df):
            row = decision_steps_df.iloc[current_step]
            previous_milestone = decision_steps_df.iloc[current_step - 1]['Milestone'] if current_step > 0 else None
            if current_step == 0 or row['Milestone'] != previous_milestone:
                st.subheader(f"Milestone: {row['Milestone']}")
            st.write(f"Step: {row['Step']}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f'Yes (Step {s})', key=f'yes_{s}'):
                    st.session_state['responses'].append('Yes')
                    st.write(f"Recommendation: {row['Yes']}")
                    st.session_state['current_step'] += 1
                    st.rerun()
            with col2:
                if st.button(f'No (Step {s})', key=f'no_{s}'):
                    st.session_state['responses'].append('No')
                    st.write(f"Recommendation: {row['No']}")
                    st.session_state['current_step'] += 1
                    st.rerun()
        else:
            st.write("You have reached the end of the process.")

if __name__ == "__main__":
    main()
