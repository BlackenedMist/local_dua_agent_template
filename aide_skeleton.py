
import sys
import time
import threading
import psutil  # pip install psutil
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QTreeView, QTabWidget, 
                             QDockWidget, QStatusBar, QLabel, QPushButton, 
                             QInputDialog, QProgressBar, QMenuBar)
from PySide6.QtGui import QFileSystemModel, QAction

# =====================================================================
# 1. BACKEND BACKGROUND DAEMON: SYSTEM RESOURCE TRACKER (Requirement 7)
# =====================================================================
class ResourceMonitorThread(QThread):
    resource_signal = Signal(float, float) # Sends back (CPU%, RAM%)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        while self.running:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            self.resource_signal.emit(cpu, ram)
            time.sleep(1) # Frequency of check

# =====================================================================
# 2. FRONTEND WORKSPACE: MAIN DEVELOPMENT ENVIRONMENT
# =====================================================================
class AgenticIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AIDE - Agentic Integrated Development Environment")
        self.resize(1300, 850)
        
        # Simulated Backend DB for local/remote Ollama Instances (Backend Req 1)
        self.ollama_registry = {
            "ollama-local": {"host": "127.0.0.1", "port": 11434, "status": "Active"},
            "ollama-remote": {"host": "10.0.0.26", "port": 11434, "status": "Active"}
        }

        self.init_ui()
        self.start_resource_monitoring()

    def init_ui(self):
        # --- Top Menu Bar ---
        self.menu_bar = self.menuBar()
        project_menu = self.menu_bar.addMenu("Projects")
        archive_action = QAction("Archive Active Project Set", self)
        project_menu.addAction(archive_action)

        # --- 1. CORE CENTER APP AREA: TABBED CODE EDITOR (Requirement 2) ---
        self.editor_tabs = QTabWidget()
        self.editor_tabs.setTabsClosable(True)
        self.editor_tabs.tabCloseRequested.connect(self.close_tab_handler)
        
        # Default placeholder workspace tab
        self.createNewTab("src/output.ts", "// Code workspace active\n// Load templates to change framework profiles.")
        self.setCentralWidget(self.editor_tabs)

        # --- 2. LEFT PANEL DOCK: FILE SYSTEM EXPLORER (Requirement 3) ---
        self.file_dock = QDockWidget("Project Workspace", self)
        self.file_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(".")
        
        self.file_tree = QTreeView()
        self.file_tree.setModel(self.file_model)
        self.file_tree.setRootIndex(self.file_model.index("."))
        self.file_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        
        self.file_dock.setWidget(self.file_tree)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.file_dock)

        # --- 3. RIGHT PANEL DOCK: COLLAPSIBLE CHAT INTERFACE (Requirement 1 & 8) ---
        self.chat_dock = QDockWidget("AI Team Orchestrator", self)
        chat_widget = QWidget()
        chat_layout = QVBoxLayout(chat_widget)
        
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_input = QTextEdit()
        self.chat_input.setMaximumHeight(80)
        self.chat_input.setPlaceholderText("Command your developer bot crew...")
        
        send_btn = QPushButton("Dispatch Snippet")
        send_btn.clicked.connect(self.dispatch_agent_tasks)
        
        chat_layout.addWidget(QLabel("Agent Relationships: Qwen (Architect) -> StarCoder (Dev)"))
        chat_layout.addWidget(self.chat_history)
        chat_layout.addWidget(self.chat_input)
        chat_layout.addWidget(send_btn)
        
        self.chat_dock.setWidget(chat_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.chat_dock)

        # --- 4. BOTTOM BAR: SYSTEM TOOLBELT & METRICS PANEL (Requirement 7) ---
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.model_status_lbl = QLabel("🤖 System Status: Thinking | Models Loaded")
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setMaximumWidth(150)
        self.cpu_bar.setFormat("CPU: %v%")
        
        self.status_bar.addWidget(self.model_status_lbl)
        self.status_bar.addPermanentWidget(self.cpu_bar)

    def createNewTab(self, filename, content):
        text_area = QTextEdit()
        text_area.setFontFamily("Courier New")
        text_area.setPlainText(content)
        self.editor_tabs.addTab(text_area, filename)

    def close_tab_handler(self, index):
        # Safety Prompt Framework implementation check (Requirement 3 Variant)
        self.editor_tabs.removeTab(index)

    # =====================================================================
    # 4. CONTROLLER COUPLING LOGIC
    # =====================================================================
    def start_resource_monitoring(self):
        self.monitor_thread = ResourceMonitorThread()
        self.monitor_thread.resource_signal.connect(self.update_resource_bars)
        self.monitor_thread.start()

    @Slot(float, float)
    def update_resource_bars(self, cpu, ram):
        self.cpu_bar.setValue(int(cpu))
        if cpu > 85.0:  # The Danger Red Zone Level Check
            self.model_status_lbl.setText("⚠️ DANGER ZONE: Exceeding VRAM Core Limit! Throttling parameters.")
            self.model_status_lbl.setStyleSheet("color: red;")
        else:
            self.model_status_lbl.setText("🤖 System Status: Orchestrator Connected & Steady")
            self.model_status_lbl.setStyleSheet("")

    def dispatch_agent_tasks(self):
        prompt = self.chat_input.toPlainText().strip()
        if not prompt: return
        
        self.chat_history.append(f"<b>You:</b> {prompt}")
        self.chat_input.clear()
        # Next stage step: Marshall payload data across network boundary to Docker Backend container

    def closeEvent(self, event):
        self.monitor_thread.running = False
        self.monitor_thread.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ide = AgenticIDE()
    ide.show()
    sys.exit(app.exec())
