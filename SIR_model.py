import numpy as np
import pandas as pd 
import streamlit as st
import matplotlib.pyplot as plt
import base64

#defining SIR_Model function
def sir_model(S, I, R, beta, gamma):
    new_infections = beta * S * I / N
    new_recoveries = gamma * I
    new_infections = min(new_infections, S)  # prevent negative values
    S_new = S - new_infections
    I_new = I + new_infections - new_recoveries
    R_new = R + new_recoveries
    return S_new, I_new, R_new

#App title
st.title('SIR Model Simulation')

#initial number of parameteres adding it dynamically
N = st.number_input('Total population', value=1000)
I0 = st.number_input('Initial number of infected individuals', value=1)
R0 = st.number_input('Initial number of recovered individuals', value=0)
S0 = N - I0 - R0
beta = st.number_input('Infection rate (beta)', value=0.3)
gamma = st.number_input('Recovery rate (gamma)', value=0.1)
days = st.number_input('Simulation duration (days)', value=100)

# Simulation of SIR_Curve
susceptible = [S0]
infected = [I0]
recovered = [R0]

for day in range(1, days+1):
    S, I, R = susceptible[-1], infected[-1], recovered[-1]
    S_new, I_new, R_new = sir_model(S, I, R, beta, gamma)
    susceptible.append(S_new)
    infected.append(I_new)
    recovered.append(R_new)

# Create DataFrame for numerical data gathering
data = pd.DataFrame({
    'Day': range(days+1),
    'Susceptible': susceptible,
    'Infected': infected,
    'Recovered': recovered
})

# Plotting stimulation chart
st.line_chart(data.set_index('Day'))

# Display DataFrame
st.write(data)

# Download DataFrame as CSV for further refference
if st.button('Download DataFrame as CSV'):
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="sir_simulation.csv">Download CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)