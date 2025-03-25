const { app, BrowserWindow } = require("electron");
const path = require("path");

const AppManager = {
  __main_window: null,

  init() {
    app.whenReady().then(() => {
      this.createMainWindow();
    });

    app.on("window-all-closed", () => {
      if (process.platform !== "darwin") app.quit();
    });

    app.on("activate", () => {
      if (this.__main_window === null) {
        this.createMainWindow();
      }
    });
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
      ? path.join(process.resourcesPath, '..', "www", "index.html")  // Packaged mode
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
