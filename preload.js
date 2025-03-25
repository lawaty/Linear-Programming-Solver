const { contextBridge, ipcRenderer } = require("electron");

let preload_finished = false;

const waitTillPreloadFinishes = async () => {
  if (preload_finished) return;

  await new Promise((resolve) => {
    const checkPreload = () => {
      if (preload_finished) {
        resolve();
      } else {
        setTimeout(checkPreload, 50); // Check every 50ms
      }
    };
    checkPreload();
  });
};

const electronAPI = {
  sendToMain: (channel, data) => ipcRenderer.send(channel, data),
  invokeMain: (channel, data) => ipcRenderer.invoke(channel, data),
  on: (channel, callback) => ipcRenderer.on(channel, (_, data) => callback(data)),
  waitTillPreloadFinishes,
};

// Expose Electron API immediately
contextBridge.exposeInMainWorld("electron", electronAPI);

(async () => {
  preload_finished = true;
})();
