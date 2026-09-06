import streamlit as st
import os
import json
from datetime import datetime

st.set_page_config(page_title="AI IT Help Desk", page_icon="🖥️", layout="centered")

KB_FOLDER = "knowledge_base"
TICKETS_FILE = "tickets/tickets.json"
ASSETS_FILE = "assets/assets.json"


# ---------- Shared data helpers ----------

def load_knowledge_base():
    kb = {}
    if os.path.exists(KB_FOLDER):
        for filename in os.listdir(KB_FOLDER):
            if filename.endswith(".txt"):
                with open(os.path.join(KB_FOLDER, filename), "r") as f:
                    kb[filename] = f.read()
    return kb


def search_knowledge_base(query, kb):
    query = query.lower()
    for filename, content in kb.items():
        topic = filename.replace(".txt", "").replace("_", " ")
        if any(word in query for word in topic.split()):
            return topic, content
    return None, None


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


def create_ticket(issue, category="General", priority="Medium"):
    os.makedirs("tickets", exist_ok=True)
    tickets = []
    if os.path.exists(TICKETS_FILE):
        with open(TICKETS_FILE, "r") as f:
            tickets = json.load(f)
    ticket_id = len(tickets) + 1001
    ticket = {
        "id": ticket_id,
        "issue": issue,
        "category": category,
        "priority": priority,
        "status": "Open",
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    tickets.append(ticket)
    with open(TICKETS_FILE, "w") as f:
        json.dump(tickets, f, indent=2)
    return ticket


# ---------- Page ----------

st.title("🖥️ AI IT Help Desk")

tab1, tab2 = st.tabs(["🛠️ Help Desk", "💻 Asset Tracker"])

# ================= TAB 1: HELP DESK (unchanged behavior from original app.py) =================
with tab1:
    st.write("👋 Hi! I'm your IT Support Assistant. Describe your issue below.")

    kb = load_knowledge_base()
    user_input = st.text_input("What issue are you having?")

    if user_input:
        topic, content = search_knowledge_base(user_input, kb)
        if content:
            st.subheader(f"📋 Troubleshooting: {topic.title()}")
            st.text(content)

            resolved = st.radio("Did this solve your problem?", ["Select an option", "Yes", "No"])
            if resolved == "No":
                ticket = create_ticket(user_input, category=topic.title())
                st.error(f"🎫 Ticket #{ticket['id']} created and assigned to IT Support.")
                st.json(ticket)
            elif resolved == "Yes":
                st.success("Glad that helped! 🎉")
        else:
            st.warning("I couldn't find a matching article. Creating a ticket for you.")
            ticket = create_ticket(user_input, category="Unclassified")
            st.error(f"🎫 Ticket #{ticket['id']} created and assigned to IT Support.")
            st.json(ticket)

# ================= TAB 2: ASSET TRACKER (unchanged behavior from original asset_tracker.py) =================
with tab2:
    st.write("Track company hardware — laptops, monitors, and more.")

    assets = load_assets()

    subtab1, subtab2 = st.tabs(["📋 View Assets", "➕ Add Asset"])

    with subtab1:
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

    with subtab2:
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

