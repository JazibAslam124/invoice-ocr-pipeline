import streamlit as st
import requests
import pandas as pd
import json
from PIL import Image

st.set_page_config(page_title="Invoice OCR", layout="wide")
st.title("Invoice OCR Pipeline")
st.caption("Upload an invoice image → get structured data instantly")

API_URL = "http://localhost:8000/extract"

uploaded = st.file_uploader("Upload invoice (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Input image")
        st.image(Image.open(uploaded), use_column_width=True)

    with col2:
        st.subheader("Extracted data")
        with st.spinner("Running OCR..."):
            uploaded.seek(0)
            response = requests.post(
                API_URL,
                files={"file": (uploaded.name, uploaded, uploaded.type)}
            )

        if response.status_code == 200:
            data = response.json()["data"]
            st.success(f"Done — {response.json()['ocr_lines_count']} text regions found")

            fields = {
                "Vendor": data.get("vendor"),
                "Invoice #": data.get("invoice_number"),
                "Date": data.get("date"),
                "Due date": data.get("due_date"),
                "Subtotal": data.get("subtotal"),
                "Tax": data.get("tax"),
                "Total": data.get("total"),
                "Currency": data.get("currency"),
            }
            df = pd.DataFrame(fields.items(), columns=["Field", "Value"])
            st.dataframe(df, use_container_width=True, hide_index=True)

            col_a, col_b = st.columns(2)
            with col_a:
                st.download_button("Download JSON", json.dumps(data, indent=2),
                                   file_name="invoice.json", mime="application/json")
            with col_b:
                st.download_button("Download CSV", df.to_csv(index=False),
                                   file_name="invoice.csv", mime="text/csv")

            with st.expander("Raw OCR text"):
                st.text(data.get("raw_text", ""))
        else:
            st.error(f"API error: {response.text}")