### 🟦 **Linear Programming Solver**  
🖥️ *Electron-based Client + Python Flask Backend*  

---

## 🏗️ **Project Structure**  
📂 **LP-Solver-App-Root/**  
📁 `core/` - Core logic for the Electron app  
📁 `server/` - Python Flask backend  
&nbsp;&nbsp;&nbsp;&nbsp;📂 `api/` - API route definitions  
&nbsp;&nbsp;&nbsp;&nbsp;📂 `core/` - LP-solving logic  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📄 `Solver.py` - Base Class implementes the common lienar algebra methods  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📄 `Simplex.py` - Simplex method solver  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📄 `BigM.py` - Big-M method solver  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📄 `TwoPhase.py` - Two-Phase method solver  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📄 `GoalProgramming.py` - Goal Programming solver  
&nbsp;&nbsp;&nbsp;&nbsp;📂 `venv/` - Python virtual environment  
&nbsp;&nbsp;&nbsp;&nbsp;📄 `app.py` - Flask application entry point  
&nbsp;&nbsp;&nbsp;&nbsp;📄 `install.sh` - Unified installation script  
📁 `www/` - Frontend (HTML, jQuery, Tailwind CSS)  
📄 `entry.js` - Electron main process entry point  
📄 `preload.js` - Electron preload script  
📄 `package.json` - Electron dependencies & scripts  
📄 `README.md` - Project documentation  

---

## ⚙️ **Installation & Setup**  

### 📌 **1. Requirements**  
✔ **Node.js** (v16+ recommended)  
✔ **Python** (3.8+ recommended)  

---

### 📦 **2. Install Dependencies**  
Run the **setup script** to install both **Electron and Python dependencies** in one step:  

#### 🖥️ **Linux/macOS (Bash)**
```sh
chmod +x install.sh  # Only needed once
./install.sh
```

#### 🪟 **Windows (PowerShell)**
```powershell
bash install.sh
```

✅ **This script will:**  
🔹 Install **Node.js dependencies** (`npm install`)  
🔹 Set up a **Python virtual environment** (`venv/`)  
🔹 Install **Flask and required Python packages**  

Alternatively, install dependencies manually.

---

### 🚀 **3. Running the Application**  
Launch both **Electron UI** and **Flask server** with:  

```sh
npm start
```

---

### 📦 **4. Building the Application**  
To package the **Electron app + Flask server**:  

```sh
npm run build
```

For specific platforms:  

🔹 **Linux:** `npm run build-linux`  
🔹 **Windows:** `npm run build-windows`  
🔹 **Mac:** `npm run build-mac`  

---

## 🔌 **API Endpoints**  

| ⚡ Method | 🛠️ Endpoint | 📌 Description |
|----------|------------|----------------------------|
| **POST** | `/api/solve/simplex` | Solves LP using Simplex Method |
| **POST** | `/api/solve/big-m` | Solves LP using Big-M Method |
| **POST** | `/api/solve/two-phase` | Solves LP using Two-Phase Method |
| **POST** | `/api/solve/goal-programming` | Solves LP using Goal Programming |

---

📌 **Notes:**  
✔ The **packaged app includes Flask**, so no extra setup is needed after building.  
✔ If you encounter permission issues on Linux/macOS, try `sudo ./install.sh`.  
✔ On **Windows**, run `bash install.sh` in **Git Bash, WSL, or Cygwin**.