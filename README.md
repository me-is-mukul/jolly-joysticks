# jolly-joysticks
## Codejam Project : FusionAI
https://github.com/user-attachments/assets/39cd91cb-74d6-47c1-9758-8d323cff36d5

# WORKFLOW DIAGRAM
![flowchart](https://github.com/user-attachments/assets/5b353b56-224b-470b-b346-d57cae0463df)
# FusionAI

**FusionAI** is a versatile desktop client designed to integrate and harness the power of multiple AI models seamlessly on cross platform (windows, max & linux). Built using **Python** and featuring a sleek **PyQt-based GUI**, this tool centralizes diverse AI functionalities into a single platform, enabling users to interact with various models efficiently. 

## Key Features


- **Assignment Generator**: Generates assignment solution when you provide keywords in your prompt like ["solve", "assignment", "solution"], it automatically opens up gateway for file upload and lateron provides a button for downloading the assignment file
- **UseCase Diagram**: Generates Usecase flowcharts and diagram on prompt. and offers unlimited chances to generate UML code.
- **Prompt Refining**: offers refine prompt feature to implement (prompt engineering effect).
- **Unified AI Integration**: Combine and operate multiple AI models under one interface.
- **PyQt-Powered GUI**: An intuitive and user-friendly interface inspired by modern IDEs like VS Code.
- **Customizable Workflows**: Tailor workflows by leveraging multiple AI models for different tasks.

## Technologies Used

- **Programming Language**: Python
- **GUI Framework**: PyQt
- **Version Control SYstem**: Git
- **AI Models**: A collection of state-of-the-art models for diverse tasks.

## Purpose

FusionAI is crafted to bridge the gap between AI enthusiasts, developers, and professionals by offering a cohesive platform to streamline AI-based operations. Whether you're working on natural language processing, computer vision, or data analysis, FusionAI provides the tools you need in one place.
<hr>

# Setup

## First install the repo and do the setup
```
https://github.com/me-is-mukul/jolly-joysticks.git
cd jolly-joysticks
touch .env
python -m venv venv
```
## activation on linux/mac
```
source venv/bin/activate
```
## activation on windows 
```
.\venv\Scripts\activate
```
## install dependencies 
```
pip install -r requirements.txt
```
## Installing Dependencies for PlantUML on different platforms
### Linux 
```
yay -S default-jdk
yay -S graphviz
yay -S plantuml
```
### Mac
```
brew install openjdk
export PATH="/usr/local/opt/openjdk/bin:$PATH"
brew install graphviz
brew install plantuml
```

### Windows
#### Step 1: Install Java
1. Download the JDK installer from [Oracle](https://www.oracle.com/java/technologies/javase-downloads.html) or [OpenJDK](https://jdk.java.net/).
2. Run the installer and follow the instructions.
3. Set the `JAVA_HOME` environment variable:
   - Go to **System Properties > Environment Variables**.


   - Add a new system variable:  
     Name: `JAVA_HOME`  
     Value: `C:\Program Files\Java\jdk-<version>`  
   - Add `%JAVA_HOME%\bin` to the `Path` variable.

#### Step 2: Install Graphviz
1. Download Graphviz from the [Graphviz website](https://graphviz.gitlab.io/_pages/Download/Download_windows.html).
2. Install it and add its `bin` directory (e.g., `C:\Program Files\Graphviz\bin`) to the `Path` variable.

#### Step 3: Download PlantUML
Download the `plantuml.jar` file from the [PlantUML website](https://plantuml.com/download).

## Setup Your API TOKKENS
1. Together API : [Together API get](https://www.together.ai/)
2. Gemini API : [Gemini API get](https://ai.google.dev/gemini-api/docs/api-key)
3. Hugging Face API : [Hugging Face API get](https://huggingface.co/docs/huggingface_hub/index)
### IN YOUR `.env` FILE.. SETUP ->
```
API_KEY_GEMINI = "KEY"
API_KEY_TOGETHER = "KEY"
API_KEY_HUGGING_FACE = "KEY"
```

# ALL SET.. GO AND RUN THE `main.py` FILE

```
python -m main
```
