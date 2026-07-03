

import flet as ft

def main(page: ft.Page):
    page.title = "Custom AI Developer IDE"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 1200
    page.window.height = 800

    # --- UI STATE & HANDLERS ---
    def send_message(e):
        if not chat_input.value.strip():
            return
        # 1. Display user message in chat history
        chat_history.controls.append(
            ft.Text(f"You: {chat_input.value}", color=ft.Colors.BLUE_200)
        )
        # 2. Simulate AI Processing (Hook your CrewAI kickoff here later)
        chat_history.controls.append(
            ft.Text("Lead Architect: Working on specifications...", color=ft.Colors.GREEN_200)
        )
        
        # Simulated Code Output to Editor panel
        code_editor.value = (
            "// Generated TypeScript Example\n"
            "import express from 'express';\n\n"
            "const router = express.Router();\n"
            f"// Task: {chat_input.value}\n"
        )
        
        chat_input.value = ""
        page.update()

    # --- LEFT PANEL: AI CHAT AGENT ---
    chat_history = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )
    
    chat_input = ft.TextField(
        hint_text="Ask your Lead Architect to build something...",
        expand=True,
        on_submit=send_message,
    )

    chat_panel = ft.Container(
        content=ft.Column([
            ft.Text("AI Dev Crew Chat", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            chat_history,
            ft.Row([
                chat_input,
                ft.IconButton(icon=ft.Icons.SEND, on_click=send_message)
            ])
        ]),
        expand=1, # Takes 1/3 of horizontal screen space
        padding=15,
        border=ft.border.only(right=ft.BorderSide(1, ft.Colors.SURFACE_CONTAINER_HIGHEST))
    )

    # --- RIGHT PANEL: CODE EDITOR ---
    code_editor = ft.TextField(
        multiline=True,
        expand=True,
        text_style=ft.TextStyle(font_family="Courier New", size=14),
        value="// Code workspace\n// Your generated src/ files will load here...",
        border=ft.InputBorder.NONE,
        hint_text="Write or review code here...",
    )

    editor_panel = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("src/auth.ts", size=16, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.IconButton(icon=ft.Icons.SAVE, tooltip="Save File"),
                    ft.IconButton(icon=ft.Icons.PLAY_ARROW, tooltip="Run Code", icon_color=ft.Colors.GREEN),
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            code_editor
        ]),
        expand=2, # Takes 2/3 of horizontal screen space
        padding=15,
        bgcolor=ft.Colors.BLACK
    )

    # --- MAIN SPLIT-SCREEN LAYOUT ---
    page.add(
        ft.Row(
            [chat_panel, editor_panel],
            expand=True,
            spacing=0
        )
    )

ft.app(target=main)
