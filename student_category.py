# Name: Luke Pring
# Student ID: A00012218
# Last Update: 25 November 2024 6:16pm

# Imports
import datetime
import os
import tabulate
import math

# Initialise student data dictionary
studentData = {}

# Initialise Valid Categorical Grades to Round
categoricalGrades = [100, 92, 85, 82, 78, 75, 72, 68, 65, 62, 58, 55, 52, 48, 45, 42, 38, 35, 32, 25, 15, 5, 0]

def get_validated_grade(field):
    """
    Returns a validated grade input, ensuring the range 1 - 100
    """
    try:
        grade = float(input(field))
    except Exception:
        print("An error occurred while calculating the overall score")
        return 0
    while grade < 0 or grade > 100:
        print("The input you entered was invalid")
        # Prevent program crashing if alphabetical characters are entered incorrectly
        try:
            grade = float(input(field))
        except Exception:
            print("The input you entered was invalid")
    return grade

def round_to_category(score):
    """
    Rounds the given score to the nearest ctageorical grade to be mapped to the approrpriate category.
    Returns the rounded score and category.
    """
    score = math.floor(score)
    up = score
    down = score
    # Find nearest grade in categorical grades list
    while up not in categoricalGrades and down not in categoricalGrades:
        up += 1
        down -= 1
    if up in categoricalGrades:
        return up, determine_category(up)
    elif down in categoricalGrades:
        return down, determine_category(down)
    else:
        print("The input you entered was invalid")

def calculate_overall_score(scores, weights):
    """
    Calculates the overall score based on the given scores list and weights list.
    Returns the overall score.
    """
    try:
        if scores == [] or weights == []:
            return 0
        if len(scores) != len(weights):
            raise ValueError("The input you entered was invalid")
        overallScore = 0
        # Calculate weighted overall score
        for index, score in enumerate(scores):
            overallScore += score * weights[index]
        return overallScore
    except IndexError:
        return 0
    except TypeError:
        return 0

def determine_category(overallScore):
        """
        Returns a category based on the overall score parameter.
        """
        if overallScore == 0:
            return "Defecit Opus"
        elif overallScore == 5 or overallScore == 15 or overallScore == 25:
            return "Fail"
        elif overallScore == 32 or overallScore == 35 or overallScore == 38:
            return "Condonable Fail"
        elif overallScore == 42 or overallScore == 45 or overallScore == 48:
            return "Third"
        elif overallScore == 52 or overallScore == 55 or overallScore == 58:
            return "2:2"
        elif overallScore == 62 or overallScore == 65 or overallScore == 68:
            return "2:1"
        elif overallScore == 72 or overallScore == 75 or overallScore == 78:
            return "First"
        elif overallScore == 82 or overallScore == 85 or overallScore == 92:
            return "Upper First"
        elif overallScore == 100:
            return "Aurum Standard"
        else:
            return "Ungraded"
        
def print_table(data):
    """
    Returns a table based on the data in the parameter. 
    """
    if len(data) < 1:
        print("The input you entered was invalid")
        return
    # Extract headers from the first student's data
    headers = ["UID"] + list(next(iter(data.values())).keys())

    # Convert dictionary to list of lists
    table_data = []
    for studentID, studentInfo in data.items():
        row = [studentID] + list(studentInfo.values())
        table_data.append(row)

    #print(table_data)

    # Create table
    table = tabulate.tabulate(table_data, headers=headers)

    # Print table
    print(table)
    
    return table

def setup_module():
    # Ask the user if they want to set up a module
    ans = input("Would you like to setup a module? (y/n): ")
    components = []
    weights_total = 0
    if ans.lower() != "y" and ans.lower() != "yes":
        # If the user does not want to set up a module, use default values
        print("\nSkipping module setup, using default values.\n")
        return 
    else:
        try:
            # Get the module name and number of assessment components
            module_name = input("Enter module name: ")
            components_count = int(input("\nHow many assessment components does this module have?: "))
        except ValueError:
            print("Error")
            return
        for i in range(1, components_count+1):
            if weights_total == 1:
                # If the total weight reaches 100, stop adding components
                print("Weights are at 100, skipping rest of components.")
                break
            # Get the component name and weight
            component_name = input(f"Component {i} name: ")
            try:
                component_weight = float(input(f"Component {i} weight (%): ")) / 100
            except ValueError:
                    print("Error")
                    return
            weights_total += component_weight
            while weights_total > 1:
                # Ensure the total weight does not exceed 100
                print("Error")
                weights_total -= component_weight
                try:
                    component_weight = float(input(f"Component {i} weight (%): ")) / 100
                    print(weights_total)
                except ValueError:
                    print("Error")
                    return
                weights_total += component_weight
            components.append([component_name, component_weight])
        # Confirm module configuration is complete
        print("Module configuration complete.")
        return module_name, components

def main():
    print("\n------------------------\nStudent Grading System\n------------------------")
    module = setup_module()
    if module is None:
        # If module not setup, set defaults
        module = ["Software Development 1", [["Coursework 1", 0.10], ["Coursework 2", 0.20], ["Coursework 3", 0.30], ["Final Exam", 0.40]]]
    components = module[1]
    #print(components)
    studentID = ""
    while True:
        if len(studentData) > 2:
            break
        
        # Input and store student ID
        studentID = input("Enter the student ID: ")

        # Check if end is entered to prevent adding another student
        if studentID == "end":
            break
        # Prevent Student IDs longer or shorter than 2 from being entered
        while len(studentID) != 2:
            print("The input you entered was invalid")
            studentID = input("Enter the student ID: ")
        
        studentData[studentID] = {}

        studentData[studentID]["Name"] = input("Student name: ")

        # Get valid date of birth
        validate = None
        while validate is None:
            studentData[studentID]["D.o.B"] = input("Date of birth: ")
            try:
                validate = datetime.date.fromisoformat(studentData[studentID]["D.o.B"])
            except ValueError:
                print("The input you entered was invalid")

        #studentData[studentID]["Age"] = math.floor((datetime.date.today() - datetime.date.fromisoformat(studentData[studentID]["D.o.B"])).days / 365)
        studentData[studentID]["Age"] = datetime.datetime.now().year - datetime.date.fromisoformat(studentData[studentID]["D.o.B"]).year
        
        # User module grades - input validated to range 0 to 100
        grades = []
        weights = []
        for component in components:
            grades.append(get_validated_grade(f"{component[0]} Grade: "))
            weights.append(component[1])

        # Calculate raw score from grades and weights taken from module component data
        studentData[studentID]["Raw Score"] = calculate_overall_score(grades, weights)

        # Get rounded score and category values from round_to_category function
        category_rounded = round_to_category(studentData[studentID]["Raw Score"])
        studentData[studentID]["Rounded Score"] = category_rounded[0]
        studentData[studentID]["Category"] = category_rounded[1]

    # Generate and print table from student data
    print_table(studentData)

def advanced(filename, weights):
    
    # Get student data from file
    file = open(filename)
    studentFile = file.readlines()
    # Remove \n from strings
    for index, student in enumerate(studentFile):
        studentFile[index] = student.strip("\n")
    
    for student in studentFile:
        student = student.split(",")
        studentID = student[0]
        studentData[studentID] = {}
        studentData[studentID]["Name"] = student[1]
        studentData[studentID]["D.o.B"] = student[2]
        # Check date of birth is valid. If not, remove student entry and skip to next
        validate = None
        try:
                validate = datetime.date.fromisoformat(studentData[studentID]["D.o.B"])
        except ValueError:
                studentData.pop(studentID)
                continue
        studentData[studentID]["Age"] = datetime.datetime.now().year - datetime.date.fromisoformat(student[2]).year
        studentData[studentID]["Raw Score"] = student[4]
        studentData[studentID]["Rounded Score"] = student[5]
        studentData[studentID]["Category"] = determine_category(int(studentData[studentID]["Rounded Score"]))

    file.close()
        
    output = open("students.txt", "x")

    output.write(print_table(studentData))  

    output.close()
    
if __name__ == "__main__":
    main()
