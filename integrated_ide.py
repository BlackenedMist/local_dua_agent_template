import threading
import flet as ft
from crewai import Agent, Task, Crew, LLM

def main(page: ft.Page):
    page.title = "Local AI Agent IDE Dashboard"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 1200
    page.window.height = 800

    # ==========================================
    # 1. DEFINE YOUR AGENT DUO INFRASTRUCTURE
    # ==========================================
    # Local Qwen Architect
    qwen_lead = LLM(
        model="ollama/qwen2.5-coder-7b.gguf:latest",
        base_url="http://localhost:11434"
    )
    # Remote StarCoder Worker
    starcoder_dev = LLM(
        model="ollama/starcoder15.gguf:latest",
        base_url="http://10.0.0.26:11434"
    )

    tech_lead = Agent(
        role='Senior Software Architect',
        goal='Break down user requests into architectural specifications.',
        backstory='You design clean, modular project frameworks.',
        llm=qwen_lead
    )

    developer = Agent(
        role='Software Engineer',
        goal='Write clean, bug-free, highly typed production code.',
        backstory='You translate architecture blueprints into final files.',
        llm=starcoder_dev
    )

    # ==========================================
    # 2. UI CONTROLS & COMPONENT DEFINITIONS
    # ==========================================
    chat_history = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    
    # Progress spinner shown during agent thinking cycles
    loading_spinner = ft.ProgressRing(visible=False, width=20, height=20)
    
    chat_input = ft.TextField(
        hint_text="Tell the agents what file to build...",
        expand=True,
    )

    code_editor = ft.TextField(
        multiline=True,
        expand=True,
        text_style=ft.TextStyle(font_family="Courier New", size=14),
        value="// Code workspace\n// Enter a prompt on the left to generate structural code...",
        border=ft.InputBorder.NONE,
    )

    file_label = ft.Text("src/output.ts", size=16, weight=ft.FontWeight.BOLD)

    # ==========================================
    # 3. BACKGROUND AGENT EXECUTION LOOPS
    # ==========================================
    def run_agent_workflow(prompt_text):
        try:
            # Dynamically attach the user's prompt directly to the Crew tasks
            task_spec = Task(
                description=f"Create a software architectural design document for: {prompt_text}",
                expected_output="A clean markdown architectural overview file.",
                agent=tech_lead,
                output_file="src/design_spec.md"
            )

            task_code = Task(
                description=f"Read the design specification and write the complete source code implementation to satisfy: {prompt_text}",
                expected_output="The final raw production source code text file without markdown wrappers.",
                agent=developer,
                output_file="src/output.ts"
            )

            # Assemble the team and run orchestration
            dev_team = Crew(agents=[tech_lead, developer], tasks=[task_spec, task_code])
            dev_team.kickoff()

            # Read the newly written code back off your hard drive
            with open("src/output.ts", "r") as f:
                generated_code = f.read()

            # Safely push the code straight to your editor workspace UI
            code_editor.value = generated_code
            chat_history.controls.append(ft.Text("Lead Architect: Generation complete! Code updated.", color=ft.Colors.GREEN_400))
        
        except Exception as ex:
            chat_history.controls.append(ft.Text(f"System Error: {str(ex)}", color=ft.Colors.RED_400))
        
        finally:
            # Turn off the loading animations when processing completes
            loading_spinner.visible = False
            chat_input.disabled = False
            page.update()

    def handle_submit(e):
        user_prompt = chat_input.value.strip()
        if not user_prompt:
            return

        # Render user message and turn on processing layout states
        chat_history.controls.append(ft.Text(f"You: {user_prompt}", color=ft.Colors.BLUE_200))
        chat_history.controls.append(ft.Text("System: Orchestrating local and remote server engines...", color=ft.Colors.GREY_400))
        
        chat_input.value = ""
        chat_input.disabled = True
        loading_spinner.visible = True
        page.update()

        # Spin off the CrewAI kickoff into a separate thread so your IDE layout doesn't lock or freeze
        agent_thread = threading.Thread(target=run_agent_workflow, args=(user_prompt,))
        agent_thread.start()

    # Bind the execution handler to actions
    chat_input.on_submit = handle_submit

    # ==========================================
    # 4. VIEW LAYOUT DESIGN
    # ==========================================
    chat_panel = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("CrewAI Agent Studio", size=18, weight=ft.FontWeight.BOLD),
                loading_spinner
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            chat_history,
            ft.Row([
                chat_input,
                ft.IconButton(icon=ft.Icons.SEND, on_click=handle_submit)
            ])
        ]),
        expand=1,
        padding=15,
        border=ft.border.only(right=ft.BorderSide(1, ft.Colors.SURFACE_CONTAINER_HIGHEST))
    )

    editor_panel = ft.Container(
        content=ft.Column([
            ft.Row([
                file_label,
                ft.Row([
                    ft.IconButton(icon=ft.Icons.SAVE, tooltip="Save File"),
                    ft.IconButton(icon=ft.Icons.PLAY_ARROW, tooltip="Execute Module", icon_color=ft.Colors.GREEN),
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            code_editor
        ]),
        expand=2,
        padding=15,
        bgcolor=ft.Colors.BLACK
    )

    page.add(ft.Row([chat_panel, editor_panel], expand=True, spacing=0))

if __name__ == "__main__":
    ft.app(target=main)
