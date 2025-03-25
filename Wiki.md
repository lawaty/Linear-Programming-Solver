🟦 **Linear Programming Solver**  
🖥️ *Electron-based Client + Python Flask Backend*  

---

## 🏗️ **Project Structure**  
📂 **lp-solver-client/**  
📁 `core/` - Core logic for the Electron app  
📁 `server/` - Python Flask backend  
&nbsp;&nbsp;&nbsp;&nbsp;📂 `api/` - API route definitions  
&nbsp;&nbsp;&nbsp;&nbsp;📂 `core/` - LP-solving logic  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📄 `interfaces.py` - Interfaces implemented by solvers  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📄 `Simplex.py` - Simplex method solver  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📄 `BigM.py` - Big-M method solver  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📄 `TwoPhase.py` - Two-Phase method solver  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📄 `GoalProgramming.py` - Goal Programming solver  
&nbsp;&nbsp;&nbsp;&nbsp;📂 `venv/` - Python virtual environment  
&nbsp;&nbsp;&nbsp;&nbsp;📄 `app.py` - Flask application entry point  
&nbsp;&nbsp;&nbsp;&nbsp;📄 `install_dep.sh` - Python dependencies setup  
📁 `www/` - Frontend (HTML, jQuery, Bootstrap)  
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

```sh
chmod +x install.sh  # Only needed once
./install.sh
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

## 🤝 **Contributing**  
🔹 **Fork** the repository  
🔹 Create a **new branch** (`feature-branch`)  
🔹 **Commit** your changes  
🔹 **Push** & create a **Pull Request**  

---

📌 **Notes:**  
✔ The **packaged app includes Flask**, so no extra setup is needed after building.  
✔ If you encounter permission issues, try `sudo ./install.sh`.  

---

This **canvas format** makes it **clearer and more visually appealing**. 🚀 Let me know if you need any refinements!