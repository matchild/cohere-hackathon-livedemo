import streamlit as st

WELCOME_TEXT_ = """

# Cohere Database Assistant (CoDA)

### Description

CoDA is an innovative NLP chat system developed during the **Cohere x NYSE Enterprise hackathon**. Our 
goal was to streamline the **process of gathering information about documents or datasets** within a company through 
**conversational interviews with data owners**. By leveraging AI-driven chat capabilities, CoDA facilitates **data 
democratization** within organizations, **saving significant time and costs** associated with identifying the right data 
sources, contacting the appropriate individuals, and locating specific datasets. 

### Key Features

1. **Data Submission:** Data owners can easily upload knowledge and **participate in structured interviews** conducted 
through the chat interface. This ensures seamless documentation and indexing of vital information. 

2. **Data Retrieval:** Employees, consultants, and other stakeholders **can ask questions about data** directly through 
the chat interface. CoDA intelligently retrieves relevant information or connects users with the appropriate data 
owners, fostering efficient knowledge access and sharing. 

### Benefits

- **Efficiency:** CoDA streamlines the process of collecting and accessing information, reducing the time and 
effort required to find relevant data within the organization. 

- **Cost Savings:** By eliminating the need for manual searches and facilitating direct communication with data 
owners, CoDA helps companies save on operational costs associated with data management. 

- **Enhanced Collaboration:** With easy access to comprehensive data insights, teams can collaborate more effectively 
and make informed decisions, driving overall productivity and innovation. 

### Use Cases

- **Data Documentation:** CoDA enables the systematic documentation of knowledge about documents and datasets, 
ensuring transparency and accessibility across the organization. 

- **Knowledge Sharing:** Employees can leverage CoDA to quickly locate relevant data sources or gain insights 
from subject matter experts, fostering a culture of knowledge sharing and collaboration. 

### Get Started

Experience the power of CoDA today and transform how your organization manages and accesses critical data. 
Test the functionalities of CoDa for **Data Submission** and **Data Retrieval** in the respective tabs of this tool.
"""


def welcome_ui() -> None:
    st.markdown(WELCOME_TEXT_)
