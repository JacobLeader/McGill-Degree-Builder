import json

def loadCourseData(file_path='/Users/jacobleader/Desktop/Code/Python/McGill-Degree-Builder/data/courses.json'):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        raise
    except Exception as e:
        print(f"An error occurred while loading course data: {e}")
        raise