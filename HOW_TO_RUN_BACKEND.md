# How to Run the Backend Server

## ⚠️ IMPORTANT: Run from the CORRECT directory!

The backend server **MUST** be run from the **project root directory** (`C:\tripsxing_chatbot`), NOT from inside the `backend` folder.

## ✅ Correct Way to Run:

### Option 1: Using the batch file (Easiest)
Double-click `run_backend.bat` from the project root.

### Option 2: Using PowerShell/Command Prompt
1. Open PowerShell or Command Prompt
2. Navigate to the project root:
   ```powershell
   cd C:\tripsxing_chatbot
   ```
3. Run the server:
   ```powershell
   python -m uvicorn backend.main:app --reload --port 8000
   ```

## ❌ WRONG Way (This will cause errors):
```powershell
cd C:\tripsxing_chatbot\backend  # ❌ DON'T do this
python -m uvicorn backend.main:app --reload --port 8000  # ❌ This will fail!
```

## Prerequisites:
1. ✅ PostgreSQL database `tripsxing_chatbot` must exist
2. ✅ PostgreSQL password is set to `2006` (or update in `backend/database.py`)
3. ✅ All dependencies installed: `python -m pip install -r backend/requirements.txt`

## Troubleshooting:

### Error: "No module named 'backend'"
- **Solution**: Make sure you're running from `C:\tripsxing_chatbot`, NOT from `C:\tripsxing_chatbot\backend`

### Error: "Database does not exist"
- **Solution**: Create the database:
  ```sql
  CREATE DATABASE tripsxing_chatbot;
  ```

### Error: "Invalid password"
- **Solution**: Check your PostgreSQL password in `backend/database.py` or create a `.env` file

