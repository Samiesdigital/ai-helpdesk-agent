import streamlit as st
import os
import json
from datetime import datetime

st.set_page_config(page_title="AI IT Help Desk", page_icon="🖥️")
st.title("🖥️ AI IT Help Desk")
st.write("👋 Hi! I'm your IT Support Assistant. Describe your issue below.")

KB_FOLDER = "knowledge_base"
TICKETS_FILE = "tickets/tickets.json"


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
