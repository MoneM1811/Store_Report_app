# inventory_search_app.py

import streamlit as st
import pandas as pd

# --- Page Configuration ---
st.set_page_config(page_title="Sharqawi Inventory Search", layout="wide")

st.markdown("## 📦 Sharqawi Inventory Search Report")
st.markdown("Use the filters below to explore the inventory status by material or vendor.")

# --- Load Data ---
@st.cache_data
def load_data():
    path = r"L:\Monthly Reports\Search_Report.xlsx"  # Updated path
    df = pd.read_excel(path)

    df['Last_issue'] = pd.to_datetime(df['Last_issue'], errors='coerce').dt.strftime('%Y-%m-%d')
    df['Last_Received'] = pd.to_datetime(df['Last_Received'], errors='coerce').dt.strftime('%Y-%m-%d')

    # Format numbers
    df['Vendor_Balance'] = df['Vendor_Balance'].map('{:,.1f}'.format)
    df['Store_Qunt'] = df['Store_Qunt'].map('{:,.2f}'.format)
    df['last_RCV_Cost'] = df['last_RCV_Cost'].map('{:,.3f}'.format)
    
    return df

search_df = load_data()

# --- Sidebar Filters ---
material = st.sidebar.text_input("🔍 Search by Material")
description = st.sidebar.text_input("📝 Material Description")
vendor_no = st.sidebar.text_input("🏷️ Vendor No.")
vendor_name = st.sidebar.text_input("👤 Vendor Name")

filtered_df = search_df.copy()

if material:
    filtered_df = filtered_df[filtered_df['Material'].astype(str).str.contains(material, case=False)]

if description:
    filtered_df = filtered_df[filtered_df['Material Description'].astype(str).str.contains(description, case=False)]

if vendor_no:
    filtered_df = filtered_df[filtered_df['Vendor No.'].astype(str).str.contains(vendor_no, case=False)]

if vendor_name:
    filtered_df = filtered_df[filtered_df['Vendor Name'].astype(str).str.contains(vendor_name, case=False)]

# --- Highlighting Logic ---
def highlight_background(val, col):
    try:
        numeric_val = float(val.replace(',', ''))
    except:
        return ''

    if col == "Store_Qunt":
        if numeric_val == 0:
            return 'background-color: #ffeaea'  # very light red
        elif numeric_val < 0:
            return 'background-color: #ffcccc'  # light red
        else:
            return 'background-color: #e6ffea'  # light green
    elif col == "Vendor_Balance":
        if numeric_val < 0:
            return 'background-color: #ffe6e6'
    return ''

# Apply styles
styled_df = filtered_df.style \
    .applymap(lambda val: highlight_background(val, 'Store_Qunt'), subset=['Store_Qunt']) \
    .applymap(lambda val: highlight_background(val, 'Vendor_Balance'), subset=['Vendor_Balance'])

# --- Display Table ---
st.markdown("### 📊 Filtered Inventory Data")
st.dataframe(styled_df, use_container_width=True)

# --- Export Section ---
st.markdown("### 📁 Export Data")
col1, col2 = st.columns(2)

with col1:
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", data=csv, file_name="Sharqawi_Inventory.csv", mime="text/csv")

with col2:
    excel_export_path = r"D:\My_Work\M.Salah Task\Sharqawi_Inventory_Export.xlsx"
    filtered_df.to_excel(excel_export_path, index=False)
    st.success(f"Excel exported to: {excel_export_path}")
