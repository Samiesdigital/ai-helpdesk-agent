import streamlit as st
import os
import json
from datetime import datetime

ASSETS_FILE = "assets/assets.json"

st.set_page_config(page_title="IT Asset Tracker", page_icon="💻")
st.title("💻 IT Asset Tracker")
st.write("Track company hardware — laptops, monitors, and more.")


def load_assets():
    os.makedirs("assets", exist_ok=True)
    if os.path.exists(ASSETS_FILE):
        with open(ASSETS_FILE, "r") as f:
            return json.load(f)
    return []


def save_assets(assets):
    os.makedirs("assets", exist_ok=True)
    with open(ASSETS_FILE, "w") as f:
        json.dump(assets, f, indent=2)


assets = load_assets()

tab1, tab2 = st.tabs(["📋 View Assets", "➕ Add Asset"])

with tab1:
    st.subheader("All Assets")

    if not assets:
        st.info("No assets logged yet. Add one in the 'Add Asset' tab.")
    else:
        status_filter = st.selectbox(
            "Filter by status", ["All", "In Use", "In Storage", "Retired"]
        )
        search_term = st.text_input("Search by employee name or asset ID")

        filtered = assets
        if status_filter != "All":
            filtered = [a for a in filtered if a["status"] == status_filter]
        if search_term:
            term = search_term.lower()
            filtered = [
                a for a in filtered
                if term in a["assigned_to"].lower() or term in a["asset_id"].lower()
            ]

        if not filtered:
            st.warning("No assets match your filters.")
        else:
            for asset in filtered:
                with st.expander(f"{asset['asset_id']} — {asset['type']} ({asset['status']})"):
                    st.write(f"**Brand/Model:** {asset['brand_model']}")
                    st.write(f"**Serial Number:** {asset['serial_number']}")
                    st.write(f"**Assigned To:** {asset['assigned_to']}")
                    st.write(f"**Status:** {asset['status']}")
                    st.write(f"**Added:** {asset['added']}")

                    new_status = st.selectbox(
                        "Update status",
                        ["In Use", "In Storage", "Retired"],
                        index=["In Use", "In Storage", "Retired"].index(asset["status"]),
                        key=f"status_{asset['asset_id']}",
                    )
                    if new_status != asset["status"]:
                        if st.button(f"Save status for {asset['asset_id']}", key=f"save_{asset['asset_id']}"):
                            asset["status"] = new_status
                            save_assets(assets)
                            st.success(f"Updated {asset['asset_id']} to {new_status}")
                            st.rerun()

with tab2:
    st.subheader("Add a New Asset")

    with st.form("add_asset_form"):
        asset_id = st.text_input("Asset ID (e.g. LAP-001)")
        asset_type = st.selectbox("Type", ["Laptop", "Desktop", "Monitor", "Phone", "Tablet", "Printer", "Other"])
        brand_model = st.text_input("Brand / Model")
        serial_number = st.text_input("Serial Number")
        assigned_to = st.text_input("Assigned To (employee name, or 'Unassigned')")
        status = st.selectbox("Status", ["In Use", "In Storage", "Retired"])

        submitted = st.form_submit_button("Add Asset")

        if submitted:
            if not asset_id or not brand_model or not serial_number:
                st.error("Please fill in Asset ID, Brand/Model, and Serial Number.")
            elif any(a["asset_id"] == asset_id for a in assets):
                st.error(f"Asset ID '{asset_id}' already exists. Use a unique ID.")
            else:
                new_asset = {
                    "asset_id": asset_id,
                    "type": asset_type,
                    "brand_model": brand_model,
                    "serial_number": serial_number,
                    "assigned_to": assigned_to if assigned_to else "Unassigned",
                    "status": status,
                    "added": datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
                assets.append(new_asset)
                save_assets(assets)
                st.success(f"Added asset {asset_id}!")
                st.rerun()