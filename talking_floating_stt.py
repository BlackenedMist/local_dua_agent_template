

-> talking_floating_stt.py

import sys
import numpy as np
import sounddevice as sd  # pip install sounddevice
from PySide6.QtCore import Qt, QTimer, Slot, QPoint
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTextEdit, QLabel, QComboBox, QGraphicsDropShadowEffect)
from PySide6.QtGui import QColor, QFont

# =====================================================================
# 1.  /FLOATING MICROPHONE ORB OVERLAY -> if ( closed or not used store in toobelt )
# =====================================================================
class FloatingMicButton(QWidget):
    def __init__(self, callback_on_stop):
        super().__init__()
        self.callback_on_stop = callback_on_stop
        self.is_recording = False
        self.pulse_state = 0
        
        # Borderless, translucent widget floating on top of all windows
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SubWindow)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(70, 70)
        
        # UI Setup
        layout = QVBoxLayout(self)
        self.button = QPushButton("🎙️", self)
        self.button.setFixedSize(55, 55)
        self.button.setFont(QFont("Segoe UI Emoji", 20))
        self.set_mic_style(QColor("#2d3748"), "white")
        
        # Add smooth glow shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 4)
        self.button.setGraphicsEffect(shadow)
        
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.button.clicked.connect(self.toggle_recording)
        
        # Timer for flashing recording animation
        self.pulse_timer = QTimer(self)
        self.pulse_timer.timeout.connect(self.animate_pulse)

        # Drag variables to allow user to move the mic anywhere on screen
        self.drag_position = QPoint()

    def set_mic_style(self, bg_color, text_color, border_color="transparent"):
        self.button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color.name()};
                color: {text_color};
                border: 2px solid {border_color};
                border-radius: 27px;
            }}
        """)

    def toggle_recording(self):
        if not self.is_recording:
            # Start Recording Mode
            self.is_recording = True
            self.pulse_timer.start(150) # Flash speed
            self.set_mic_style(QColor("#2f855a"), "white", "#48bb78") # Solid Green base
        else:
            # Stop Recording Mode
            self.is_recording = False
            self.pulse_timer.stop()
            self.set_mic_style(QColor("#2d3748"), "white")
            # Fire intercept panel callback with simulated voice parsing text
            simulated_voice_text = "Refactor the authentication logic inside router.ts to validate incoming session tokens securely."
            self.callback_on_stop(simulated_voice_text)

    def animate_pulse(self):
        # Alternate colors to mimic flashing recording loop
        if self.pulse_state == 0:
            self.set_mic_style(QColor("#e53e3e"), "white", "#feb2b2") # Red Flash Warning
            self.pulse_state = 1
        else:
            self.set_mic_style(QColor("#2f855a"), "white", "#48bb78") # Green Flash Active
            self.pulse_state = 0

    # Drag-and-Drop Floating Movement mechanics
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

# =====================================================================
# 2. INTERCEPT VALIDATION DIALOG BOX
# =====================================================================
class VoiceInterceptField(QWidget):
    def __init__(self, target_dispatch_callback):
        super().__init__()
        self.dispatch_callback = target_dispatch_callback
        
        # Borderless desktop alert block
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setStyleSheet("""
            QWidget {
                background-color: #1a202c;
                border: 1px solid #4a5568;
                border-radius: 8px;
                color: #e2e8f0;
            }
        """)
        self.resize(420, 220)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        
        layout.addWidget(QLabel("📝 Voice Intercept (Review & Target Input):"))
        
        # Editable workspace area so you can fix errors before sending
        self.text_editor = QTextEdit()
        self.text_editor.setStyleSheet("background-color: #2d3748; border-radius: 4px; padding: 4px;")
        layout.addWidget(self.text_editor)
        
        # Dropdown routing context selector
        routing_layout = QHBoxLayout()
        routing_layout.addWidget(QLabel("🎯 Route Target:"))
        self.target_selector = QComboBox()
        self.target_selector.addItems([
            "Send to Chat Panel (Advice/Error Checks)",
            "Send to Lead Architect (Marching Orders)",
            "Inject Directly into Active Editor File",
            "Send to Book Writing Template Module"
        ])
        self.target_selector.setStyleSheet("background-color: #2d3748; padding: 4px;")
        routing_layout.addWidget(self.target_selector)
        layout.addLayout(routing_layout)
        
        # Action Buttons
        btn_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("background-color: #4a5568; color: white; padding: 6px; border-radius: 4px;")
        cancel_btn.clicked.connect(self.hide)
        
        approve_btn = QPushButton("Approve & Disptach")
        approve_btn.setStyleSheet("background-color: #3182ce; color: white; padding: 6px; border-radius: 4px; font-weight: bold;")
        approve_btn.clicked.connect(self.approve_and_send)
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(approve_btn)
        layout.addLayout(btn_layout)

    def show_intercept(self, raw_text, spawn_position):
        self.text_editor.setPlainText(raw_text)
        # Position panel comfortably right next to the mic widget pointer location
        self.move(spawn_position.x() + 70, spawn_position.y() - 70)
        self.show()

    def approve_and_send(self):
        final_text = self.text_editor.toPlainText().strip()
        selected_route = self.target_selector.currentText()
        if final_text:
            self.dispatch_callback(final_text, selected_route)
        self.hide()

# =====================================================================
# 3. CORE SIMULATION WORKSPACE MAIN ENGINE CONTAINER
# =====================================================================
class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        
        # Instantiate widgets
        self.floating_mic = FloatingMicButton(self.handle_voice_capture_event)
        self.intercept_panel = VoiceInterceptField(self.handle_final_dispatch)
        
        # Place floating mic initial position at bottom-right viewport area
        self.floating_mic.move(1100, 700)
        self.floating_mic.show()
        
    def handle_voice_capture_event(self, transcript):
        # Open intercept panel next to floating widget location
        mic_pos = self.floating_mic.pos()
        self.intercept_panel.show_intercept(transcript, mic_pos)

    def handle_final_dispatch(self, text, route):
        # Main output boundary channel log printout
        print(f"\n🚀 DISPATCH SUCCESSFUL TO DESTINATION: [{route}]")
        print(f"Content: \"{text}\"")

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    controller = AppController()
    controller.run()
