# Expirers
### Group Members: Cianna, Zara, Darien, Sophie 

A secure PDF‑sharing and automatic‑expiry platform built with **Flask** and **Firebase**.

---

## Getting Started

### 1  Clone the repository
```bash
git clone https://github.com/sophietsanang/Expirers.git
cd Expirers
```

### 2  Install prerequisites
* **Python 3.8** or later
* **pip** (bundled with Python)

> **Tip — use a virtual environment**
> ```bash
> python3 -m venv venv
> source venv/bin/activate   # macOS / Linux
> # .\venv\Scripts\activate   # Windows PowerShell
> ```

### 3  Install dependencies
```bash
pip install -r requirements.txt
```
The `requirements.txt` file lists all third‑party packages, including `Flask`, `firebase‑admin`, `sendgrid`, `python‑dotenv`, `python‑dateutil`, and `requests`.

### 4  Run the application
```bash
python server.py
```
The server will start at `http://127.0.0.1:5000/` by default.

---

## Additional Configuration
Two credential files are **not** committed to the repository:

1. `.env`
2. `bus-expirer-firebase-adminsdk-fbsvc-34c2895d64.json`

We have already sent you these files separately. **Please add them to the project root before running the application.**

---

Feel free to open an issue or pull request if you encounter any problems. 
