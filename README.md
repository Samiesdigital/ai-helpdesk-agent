# AI IT Help Desk Agent

An AI-assisted IT support tool built with Python and Streamlit. It combines a troubleshooting assistant, automated ticket creation, and a hardware asset tracker into a single connected app — so support requests can be matched to an employee's actual assigned device.

🔗 **Live app:** [samie-itsupport-agent.streamlit.app](https://samie-itsupport-agent.streamlit.app)

## What it does

**Help Desk tab**
- Employee describes an IT issue in plain language
- The app searches a knowledge base of common issues (VPN, wifi, printer, password reset, login, email, slow computer) and returns troubleshooting steps
- If the employee enters their name, the app looks up their assigned device from the Asset Tracker and displays it alongside the fix
- If the issue isn't resolved (or no matching article is found), the app automatically creates a support ticket — including the employee's linked device info, if found

**Asset Tracker tab**
- View all company hardware (laptops, monitors, phones, etc.) with filtering by status and search by employee name or asset ID
- Add new assets with ID, type, brand/model, serial number, and assigned employee
- Update an asset's status (In Use / In Storage / Retired) directly from the list

## Why I built it this way

This started as two separate projects — a troubleshooting bot and an asset tracker — built independently to practice different skills (knowledge-base search/ticketing vs. CRUD data management). I later merged them into one app and added a lookup layer connecting the two, so a support ticket isn't just "an issue" — it's an issue tied to a specific, known piece of hardware. This mirrors how real IT help desks work, where support agents need device context to resolve tickets efficiently.

## Tech stack

- **Language:** Python
- **Framework:** [Streamlit](https://streamlit.io/)
- **Data storage:** JSON files (`tickets/tickets.json`, `assets/assets.json`)
- **Deployment:** GitHub + Streamlit Community Cloud

## Project structure

```
ai-helpdesk-agent/
├── app.py                  # Main app: Help Desk + Asset Tracker tabs
├── knowledge_base/         # Troubleshooting articles (.txt files)
├── tickets/                # Stored support tickets (JSON)
├── assets/                 # Stored hardware asset records (JSON)
└── requirements.txt
```

## Running locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Roadmap

- Personalize troubleshooting steps based on the employee's specific device model
- Expand ticket dashboard/filtering
- Add authentication so employees only see their own device/tickets
