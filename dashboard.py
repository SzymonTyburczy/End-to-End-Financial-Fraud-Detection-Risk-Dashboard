import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="🛡️",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/predict"

st.title("🛡️ Enterprise Fraud Detection System")
st.markdown("### Analyst panel for transaction fraud detection using XGBoost model")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Transaction Details")
    step = st.number_input("Time Step", min_value=1, value=100, help="Simulation hour")
    type_txn = st.selectbox("Transaction Type", ["TRANSFER", "CASH_OUT", "PAYMENT", "CASH_IN", "DEBIT"])
    amount = st.number_input("Amount", min_value=0.0, value=1000.0, step=10.0)

with col2:
    st.subheader("2. Origin Details")
    nameOrig = st.text_input("Client ID (Origin)", "C12345678")
    oldbalanceOrg = st.number_input("Old Balance (Origin)", min_value=0.0, value=1000.0)

    simulate_fraud = st.checkbox("Simulate Fund Theft (Fraud Pattern)")

    if simulate_fraud:
        newbalanceOrig = 0.0
        st.warning(f"Simulation: New balance set to {newbalanceOrig} (Theft!)")
    else:
        default_new = max(0.0, oldbalanceOrg - amount)
        newbalanceOrig = st.number_input("New Balance (Origin)", min_value=0.0, value=default_new)

st.markdown("---")
st.subheader("3. Destination Details")
c3, c4 = st.columns(2)
with c3:
    nameDest = st.text_input("Client ID (Dest)", "M98765432")
    oldbalanceDest = st.number_input("Old Balance (Dest)", min_value=0.0, value=0.0)
with c4:
    # Common fraud pattern: Money sent but not received (or account is a "black hole")
    newbalanceDest = st.number_input("New Balance (Dest)", min_value=0.0, value=0.0)

st.markdown("---")
submit = st.button("Analyze Transaction", use_container_width=True)

if submit:
    payload = {
        "step": step,
        "type": type_txn,
        "amount": amount,
        "nameOrig": nameOrig,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "nameDest": nameDest,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest,
        "isFlaggedFraud": 0
    }

    with st.spinner("XGBoost model is processing data..."):
        try:
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                result = response.json()
                prediction = result["prediction"]
                probability = result["fraud_probability"]

                st.markdown("## Analysis Result:")

                col_res1, col_res2 = st.columns([1, 2])

                with col_res1:
                    if prediction == "FRAUD":
                        st.error("🚨 FRAUD DETECTED")
                    else:
                        st.success("✅ LEGITIMATE TRANSACTION")

                with col_res2:
                    st.metric("Fraud Probability", f"{probability:.2%}")
                    st.progress(probability)

                # Business explanation
                with st.expander("🔍 Why this result? (Interpretation)"):
                    st.write(f"The model assessed the risk at **{probability:.4f}**.")
                    st.write("Main factors analyzed by the model:")
                    st.write("- **Balance Discrepancy (ErrorBalance):** Did money disappear without a trace?")
                    st.write("- **Transaction Type:** TRANSFER and CASH_OUT are the riskiest.")
                    st.write(f"- **Amount:** {amount}")
            else:
                st.error(f"API Error: {response.status_code}")
                st.text(response.text)

        except requests.exceptions.ConnectionError:
            st.error(" Cannot connect to API. Did you start `uvicorn api.main:app`?")