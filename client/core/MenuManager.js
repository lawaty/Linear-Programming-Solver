const { Menu, BrowserWindow } = require("electron");

const MenuManager = {
  init() {
    const menuTemplate = [
      {
        label: "App",
        submenu: [
          {
            label: "Reload",
            accelerator: "CmdOrCtrl+R",
            click: () => {
              const win = BrowserWindow.getFocusedWindow();
              if (win) win.reload();
            },
          },
          {
            label: "Toggle DevTools",
            accelerator: "CmdOrCtrl+Shift+I",
            click: () => {
              const win = BrowserWindow.getFocusedWindow();
              if (win) win.webContents.toggleDevTools();
            },
          },
          { type: "separator" },
          {
            label: "Exit",
            accelerator: "CmdOrCtrl+Q",
            role: "quit",
          },
        ],
      },
    ];

    Menu.setApplicationMenu(Menu.buildFromTemplate(menuTemplate));
  },

  addMenu(label, submenuItems) {
    const currentMenu = Menu.getApplicationMenu()?.items.map(item => ({
      label: item.label,
      submenu: item.submenu ? item.submenu.items.map(sub => ({
        label: sub.label,
        type: sub.type || "normal",
        checked: sub.checked || false,
        accelerator: sub.accelerator || null,
        role: sub.role || null,
        click: sub.click || (() => { }),
      })) : [],
    })) || [];

    currentMenu.push({
      label,
      submenu: submenuItems,
    });

    Menu.setApplicationMenu(Menu.buildFromTemplate(currentMenu));
  },
};

module.exports = MenuManager;
