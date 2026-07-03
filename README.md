# local_dua_agent_template
ow this works when you run it:
You run python agent_duo.py.Qwen2.5-Coder wakes up first,
 processes your request, and writes a detailed architecture design document
 .The framework automatically captures Qwen's output and hands it to StarCoder2.S
 tarCoder2 reads Qwen's design rules and outputs the completed TypeScript/Python code file to your terminal.Would you like me to show you how to expand this script so that it automatically writes the finished code files directly to your hard drive, or would you prefer a UI-based agent tool like Open-WebUI Pipelines instead?


Step 1: Open Your Global OpenCode SettingsYou need to put your settings into the central OpenCode configuration file:Windows (WSL / Local): ~/.config/opencode/opencode.jsonMac / Linux: ~/.config/opencode/opencode.jsonIf the directory or file doesn’t exist yet, simply create them manually.Step 2: Paste the Agent Pipeline ConfigPaste the following JSON structure into your opencode.json file. This explicitly maps Qwen2.5-Coder as your primary macro-planning/review agent and StarCoder as your rapid execution/autocomplete engine.


Step 3: Triggering Them Together in OpenCodeNow, when you launch OpenCode (opencode in your editor terminal or split window), the two models will play distinct parts:The Lead Setup: Because default_agent is set to "lead-architect", Qwen2.5 handles the primary user interface chat window. It handles tool calls like checking project files and designing structural blueprints.The Assistant Setup: StarCoder2 handles small_model background tasks—meaning anytime OpenCode requires rapid micro-parsing, background syntax lookups, or file changes, it offloads those minor tasks to StarCoder.Targeted Agent Calls: Inside the OpenCode TUI/chat screen, you can also tag them explicitly at any point using the @ symbol. For example:@lead-architect Review this backend repository architecture.@starcoder-dev Turn that architecture spec into a router.ts file.





This is going to be a Intergrated IDE / Chat application.

The Main actors in this project are the two local models I have configured to work together ( will change in future ) - putting different models together

Current configuration is 
agent": {
    "lead-architect": {
      "description": "Breaks down requirements and plans code updates using your local Qwen model.",
	  "provider": "ollama-local",
      "model": "qwen2.5-coder-7b.gguf:latest"
	  }
}
"starcoder-dev": {
      "description": "Takes blueprints and writes code using your remote server engine.",
      "provider": "ollama-remote",
      "model": "starcoder15.gguf:latest"
	  }
}


It is designed to run in a docker environment ( This should be the final set of this project ) 





This application will contain 
1 ) a chat Interface  to talk to a developer bot and get feedback , support , error checking , advice or code and documentation
2 ) A code editor where user can edit the selected file ( with all syntax related the project type ) 
3 ) a folder / project Navigation explorer - similar to Eclipse IDE. where i can display activce sets of projects or a single project - drop downs , context menu right click create folder or project spec file ) 
    Users will be able to create, manage, delete , archive projects  ( look into project templates - creating java application or AI type  or webui type , bookwriting  ,or etc etc )  rate the models performance during the project
4) a history/ report on projects done, tasks 
5) A To do list and expected dates when to complete - Standard fields ( text area ) ie updated this portion today, found bug , solution , fix etc etc
6) STT so users can talk 
7) dedicate a low-level background daemon using Python’s psutil or NVML (Nvidia Management Library) bindings to query system state. 
 If VRAM thresholds pass 90% (the Danger Red Level), the backend orchestrator should dynamically slice the active Ollama model request payload context down 
 (e.g., forcing num_ctx: 2048 instead of 16384) or auto-trigger an Ollama unload endpoint request before the machine locks up
 Store these heavy interaction history datasets inside   
8) User wil be able to either send the entire editor page they are working on or a just a snipppet of code in the chat screen.
9)a hidden project directory configuration folder (e.g., current_project/.aide/)
 Hidden System Context Tracking (.aide_telemetry/ Pattern)
 Since your blueprint specifies calculating overall token analytics and generating project performance reports, 
 this hidden directory serves as your local time-series analytics engine.


 


Backend 

Is going to be a Model Management / status , orchestrator ( Ability to link into other projects ) 

1 ) keep and store the information about the local ollama instances  ( User should be able to add new/ delete or edit)
	-host names 
	-port numbers
	-list of models available
	-status of all ollama instances ( servers )
	-status of the active models being used.
	
2 ) Store basic information about 
	-the models that were used.
	-for how long they were used
	-project we worked on
	-keep a list of active projects - allow for archiing projects in zip on the local server ( git in the future )
 	
3 )  When sending information to the AI models and it exceeds context_parameters that is set by a limit all the information should be stored in a file 
	 in the project - This directory should not be displayed to the user unless he toggle to display it
	 end of a project the user should be able to see how many parameters he send ( Communication flow , models used , their agent status + role , etc etc ) 


Frontend - the Main Developement environment -


Stack
PyQt6’s QDockWidget

We can ceate a workspace where all projects will be stored - vissble = active project or project set ) hidden can be in another directory - same like the templates we will add in
( only have one for now, Will get more as project grows. -we wiill start with _writer_template.zip )

The ability to implement and change the theme of front end. 5 themes are good to start ( varies light and dark + high contrast ) (persisted on reboot)


For the UI Layout (The Window): Use Flet or PyQt6. 
For the Code Editor Component: Use a package like QCodeEditor (if using PyQt) or embed a web-based Monaco Editor 

 1) They make it easy to create a split-screen view ( project /file explorer far left ,Chat panel on the right, Editor panel on the center ). 
    the file explorer and and chat should be colapaibe
 2) The file explorer should give a create project - as we add templates it will increase the type of projects to create ) ( active sets and a simple filter ) typpe text if prpoject or file is in
    working set or active it will display at top. When text is cleared normal directory veiw. Projects will stored on local - disk  ( two directories active _ non active ) 
	user should have a drop down to select which projects will be disabled ( active or add other projects to the active set + remove them ) 
 3) chats should be archived in a chat list with meaningful titles and dates - ( ref at a later stage or send to AI )  ( archirved in the projec ( or project active set )
 
 
 Lets talk interface. 
 
1 ) There will be a landing page -basic information about current project  - Time spent - models used - tasks to do and tasks completed
2 ) the main work area will consist of the project/file expplorer the editor ( Tabbed and allow detach for side by side view ) and the chat interface on the right.
	The main code editor will adaopt the project types templates ( IE AI development - ai toools  or bookwriting then book writing tools 	
	user should have a check menu item, in a context menu to toggle page is read only. 
	editor should have a undo ad redo ( 5 steps is enough ) 	
	There should be a toolbelt at the bottom of the page. make this collapable going drown. Links to home or any other page should be found here. Tools for editor should also be here.
	can store snippets of code or prompts that has been used 
3)  A top bar were limited information about the active models will be displayed. ( working , thinking ,  discussing , builing ) time it took - total parameters sent   
	There should be a timer that if user hasn't saved in past 15 mins. - prompt the user its time to save. Unsaved files being closed - promt the user are you sure?
4)  there must be a well formed confirmation dialog when sending information from the editor to the backend. Just these pages -> iin this order -> total param count
5) A seperate page where the user can see the model and the Agent relationships that have been configured.
6) a key mapping tool. for developer / writers preferences. crtl Z or cntl -f ( Apply codes formatting and indentation ) 



The Mic Widget: A circular button floats completely independently of your main AIDE window.
 You can drag it with your mouse to sit over your left-hand explorer tree or right-hand chat block.
 The Flashing Feedback Loop: Clicking the button turns it green and flashes red-and-green to provide visual confirmation that the microphone array is reading raw audio processing frames.
 The Validation Gate: When clicked again to stop recording, a sleek dark intercept dialog box slides open right beside the mic button.
 The Target Routing Guard: The user interface prevents data injection into your codebase until you manually select the target destination dropdown 
 (e.g., separating an operational "marching order" for the bots from raw text injection into a specific template file).

Connecting Your Agents: Instead of hardcoding tasks like task_spec,
you will capture what you type into your custom chat window, pass it as a dynamic variable to
he Task description, a0nd reload the src/ file in your editor panel when the script finishes.



📁 aide-workspace-root/
│
├── 📁 backend-core/               # The Model Orchestrator & Database Layer
│   ├── 📄 Dockerfile
│   ├── 📄 orchestrator.py         # CrewAI / OpenCode pipeline connector
│   ├── 📄 models_db.json          # Keeps Ollama instances list, ports, and metrics
│   └── 📄 project_manager.py      # Zip archiving, active vs non-active directory pools
│
├── 📁 frontend-desktop/           # The Main Development Environment UI
│   ├── 📄 Dockerfile
│   ├── 📄 main_ide.py             # Main PyQt6 App Entry Window
│   ├── 📁 modules/
│   │   ├── 📄 code_editor.py      # Tabbed editor window with Monaco/QCodeEditor bindings
│   │   ├── 📄 file_explorer.py    # Tree widget with workspace filtering & context menus
│   │   ├── 📄 chat_sidebar.py     # Speech-to-Text (STT) + chat window interaction engine
│   │   └── 📄 toolbelt.py         # Collapsible footer snippet manager & system charts
│   └── 📁 themes/                 # 5 configuration theme definitions (JSON mappings)
│
└── 📁 workspace/                  # Local Hard-Drive Storage 
    ├── 📁 active_projects/        # Active Working Set view directories
    └── 📁 archived_projects/      # Non-active ZIP files
  



The blue print 

-> see aide_skeleton.py



