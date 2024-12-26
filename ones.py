import os
import subprocess

def generate_plantuml_code(description):
    """Generate PlantUML code dynamically based on the description."""
    description = description.lower()

    if "use case diagram" in description:
        # Extract actors and use cases
        actors = []
        use_cases = []
        words = description.split()
        
        for i, word in enumerate(words):
            if word in ["actor", "actors"]:
                actors_start = i + 1
                while actors_start < len(words) and words[actors_start] != "and":
                    actors.append(words[actors_start].strip(",").capitalize())
                    actors_start += 1

            if word in ["actions", "use cases"]:
                actions_start = i + 1
                while actions_start < len(words):
                    use_cases.append(words[actions_start].strip(",").capitalize())
                    actions_start += 1

        # Generate PlantUML code
        plantuml_code = "@startuml\n"
        for actor in actors:
            plantuml_code += f"actor {actor}\n"
        for use_case in use_cases:
            plantuml_code += f"usecase \"{use_case}\" as UC{use_cases.index(use_case) + 1}\n"
        for actor in actors:
            for use_case in use_cases:
                plantuml_code += f"{actor} --> UC{use_cases.index(use_case) + 1}\n"
        plantuml_code += "@enduml\n"
        return plantuml_code

    elif "flow diagram" in description:
        # Generate a basic flow diagram based on steps
        steps = [word.strip(",").capitalize() for word in description.split() if word not in ["for", "a", "an", "the", "with", "steps"]]
        plantuml_code = "@startuml\nstart\n"
        for step in steps:
            plantuml_code += f":{step};\n"
        plantuml_code += "stop\n@enduml\n"
        return plantuml_code

    else:
        # Default UML code for unsupported cases
        return "@startuml\n@enduml\n"

def get_user_input():
    """Prompt the user to enter a description."""
    print("Enter a description of your diagram:")
    return input("> ")

def save_plantuml_code(plantuml_code):
    """Save the PlantUML code to a temporary file."""
    with open("temp_diagram.puml", "w") as file:
        file.write(plantuml_code)

def generate_diagram():
    """Generate a diagram image using PlantUML."""
    try:
        subprocess.run(["plantuml", "temp_diagram.puml"], check=True)
        print("Diagram generated successfully: output_diagram.png")
    except subprocess.CalledProcessError as e:
        print(f"Error generating diagram: {e}")

def main():
    """Main function to drive the script."""
    description = get_user_input()
    plantuml_code = generate_plantuml_code(description)
    print("Generated PlantUML Code:\n", plantuml_code)
    save_plantuml_code(plantuml_code)
    generate_diagram()

if __name__ == "__main__":
    main()
