const { app, BrowserWindow } = require("electron");
const { spawn } = require("child_process");
const path = require("path");

const AppManager = {
  __main_window: null,
  __flask_process: null,

  init() {
    app.whenReady().then(() => {
      this.startFlaskServer();
      this.createMainWindow();
    });

    app.on("window-all-closed", () => {
      if (process.platform !== "darwin") {
        this.stopFlaskServer();
        app.quit();
      }
    });

    app.on("before-quit", () => {
      this.stopFlaskServer();
    });

    app.on("activate", () => {
      if (this.__main_window === null) {
        this.createMainWindow();
      }
    });
  },

  startFlaskServer() {
    const isPackaged = app.isPackaged;

    // Adjust the Python executable path for different platforms
    const pythonExecutable = isPackaged
      ? process.platform === "win32"
        ? path.join(process.resourcesPath, "python_env", "Scripts", "python.exe") // Windows
        : path.join(process.resourcesPath, "python_env", "bin", "python3") // Linux/Mac
      : process.platform === "win32"
        ? path.join(__dirname, "..", "server", "venv", "Scripts", "python.exe") // Dev Windows
        : path.join(__dirname, "..", "server", "venv", "bin", "python3"); // Dev Linux/Mac

    const serverScript = isPackaged
      ? path.join(process.resourcesPath, "server", "app.py") // Packaged mode
      : path.join(__dirname, "..", "server", "app.py"); // Development mode

    console.log(`Starting Flask server with: ${pythonExecutable} ${serverScript}`);

    this.__flask_process = spawn(pythonExecutable, [serverScript], {
      cwd: path.dirname(serverScript),
      detached: false,
      stdio: isPackaged ? "ignore" : "inherit", // Show logs in development mode
    });

    if (!isPackaged) {
      this.__flask_process.stdout?.on("data", (data) => console.log(`[Flask] ${data}`));
      this.__flask_process.stderr?.on("data", (data) => console.error(`[Flask Error] ${data}`));
    }

    this.__flask_process.unref();
  },

  stopFlaskServer() {
    if (this.__flask_process) {
      console.log("Stopping Flask server...");
      this.__flask_process.kill();
      this.__flask_process = null;
    }
  },

  createMainWindow() {
    this.__main_window = new BrowserWindow({
      width: 1024,
      height: 768,
      maximized: true,
      webPreferences: {
        preload: path.join(__dirname, "../preload.js"),
        contextIsolation: true,
        nodeIntegration: false,
      },
    });

    this.__main_window.maximize();

    const appPath = app.isPackaged
      ? path.join(process.resourcesPath, "www", "index.html") // Packaged mode
      : path.join(__dirname, "..", "www", "index.html"); // Development mode

    this.__main_window.loadFile(appPath).catch((err) => {
      console.error("Failed to load index.html:", err);
    });

    this.__main_window.on("closed", () => {
      this.__main_window = null;
    });
  },
};

module.exports = AppManager;
