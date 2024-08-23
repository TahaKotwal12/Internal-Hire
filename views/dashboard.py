import streamlit as st
from Database.Db import load_data
import plotly.express as px
import pandas as pd

# Session state
if 'df' not in st.session_state:
    st.session_state.df = None

#st.set_page_config(page_title="HR Dashboard", layout="wide")
st.title("Dashboard")
st.text("Streamline internal hiring with our efficient app")

# Load data
if st.session_state.df is None:
    
    with st.spinner("Loading Data please wait !!"):
        try:
            load_data()
        except Exception as e:
            st.error("Unable to load data")
            st.exception(e)

if st.session_state.df is not None:
    df = st.session_state.df

    # Count
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Employees", df.shape[0])
    with col2:
        st.metric("Departments", df['DEPARTMENT'].nunique())
    with col3:
        st.metric("Available Employees", df['AVAILABILITY'].sum())

    # Department distribution
    st.subheader("Employee Distribution by Department")
    fig_dept = px.pie(df, names='DEPARTMENT', title='')
    st.plotly_chart(fig_dept, use_container_width=True)

    # Availability distribution
    st.subheader("Employee Availability")
    availability_data = df['AVAILABILITY'].value_counts().reset_index()
    availability_data.columns = ['Status', 'Count']
    availability_data['Status'] = availability_data['Status'].map({1: 'Available', 0: 'Not Available'})
    fig_avail = px.pie(availability_data, names='Status', values='Count', title='',
                       color='Status', color_discrete_map={'Available': 'green', 'Not Available': 'red'})
    st.plotly_chart(fig_avail, use_container_width=True)

    # Top 5 Departments by Headcount
    st.subheader("Top 5 Departments by Headcount")
    top_departments = df['DEPARTMENT'].value_counts().nlargest(5).reset_index()
    top_departments.columns = ['Department', 'Count']
    fig_top5 = px.bar(top_departments, x='Department', y='Count', title='')
    st.plotly_chart(fig_top5, use_container_width=True)

    # Availability by Department
    st.subheader("Availability by Department")
    dept_availability = df.groupby('DEPARTMENT')['AVAILABILITY'].mean().sort_values(ascending=False)
    fig_dept_avail = px.bar(dept_availability, x=dept_availability.index, y=dept_availability.values,
                            labels={'y': 'Availability Rate', 'x': 'Department'},
                            color=dept_availability.values, color_continuous_scale='RdYlGn')
    st.plotly_chart(fig_dept_avail, use_container_width=True)

else:
    st.warning("No data available. Please check your database connection.")