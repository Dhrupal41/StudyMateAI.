
def get_quiz_questions(subject, level, topic):
    """
    Generate interactive quizzes for supported topics.
    Each quiz contains 10 MCQs.
    Answer index starts from 0.
    """

    subject_lower = subject.strip().lower()
    topic_lower = topic.strip().lower()

    # Identify quiz topic
    if "numpy" in topic_lower:
        quiz_topic = "numpy"

    elif "pandas" in topic_lower:
        quiz_topic = "pandas"

    elif "function" in topic_lower:
        quiz_topic = "functions"

    elif "loop" in topic_lower:
        quiz_topic = "loops"

    elif "list" in topic_lower:
        quiz_topic = "lists"

    else:
        return None

    # Python topics require Python subject
    if quiz_topic in ["functions", "loops", "lists"]:
        if subject_lower != "python":
            return None

    quizzes = {

        # =====================================
        # PYTHON FUNCTIONS
        # =====================================

        "functions": [

            {
                "question": "Which keyword is used to define a function in Python?",
                "options": ["function", "define", "def", "fun"],
                "answer": 2,
                "explanation": "Python uses the def keyword to define a function."
            },

            {
                "question": "Which symbol ends a function definition line?",
                "options": [";", ":", ".", ","],
                "answer": 1,
                "explanation": "A colon starts the indented body of a function."
            },

            {
                "question": "What does the return statement do?",
                "options": [
                    "Repeats a function",
                    "Sends a value back from a function",
                    "Defines a variable",
                    "Prints every value"
                ],
                "answer": 1,
                "explanation": "return sends a result back to the code that called the function."
            },

            {
                "question": "How do you call a function named greet?",
                "options": ["call greet", "greet[]", "greet()", "def greet()"],
                "answer": 2,
                "explanation": "A function is called using its name followed by parentheses."
            },

            {
                "question": "What is a parameter in a function?",
                "options": [
                    "A variable listed in the function definition",
                    "A comment",
                    "A loop",
                    "A print command"
                ],
                "answer": 0,
                "explanation": "A parameter is a variable that receives a value when the function is called."
            },

            {
                "question": "What is an argument?",
                "options": [
                    "The function name",
                    "A value passed to a function when it is called",
                    "The return keyword",
                    "A type of loop"
                ],
                "answer": 1,
                "explanation": "An argument is the actual value supplied to a function call."
            },

            {
                "question": "What does this function return: def add(a, b): return a + b?",
                "options": ["a", "b", "The sum of a and b", "None"],
                "answer": 2,
                "explanation": "The function returns the result of adding a and b."
            },

            {
                "question": "Which statement about functions is correct?",
                "options": [
                    "Functions cannot accept inputs",
                    "Functions help reuse code",
                    "Every function must contain a loop",
                    "Functions must always print"
                ],
                "answer": 1,
                "explanation": "Functions allow you to write reusable blocks of code."
            },

            {
                "question": "What is the output of a function that prints Hello when called?",
                "options": ["greet", "Hello", "Nothing", "Error"],
                "answer": 1,
                "explanation": "Calling the function executes its print statement."
            },

            {
                "question": "What does a Python function return if it has no return statement?",
                "options": ["0", "False", "None", "An empty string"],
                "answer": 2,
                "explanation": "Python functions return None automatically when no return value is specified."
            }

        ],

        # =====================================
        # PYTHON LOOPS
        # =====================================

        "loops": [

            {
                "question": "Which loop is commonly used to iterate over a sequence?",
                "options": ["if loop", "for loop", "switch loop", "define loop"],
                "answer": 1,
                "explanation": "A for loop iterates over items in a sequence."
            },

            {
                "question": "Which loop repeats while a condition is True?",
                "options": ["for", "while", "def", "class"],
                "answer": 1,
                "explanation": "A while loop continues as long as its condition remains True."
            },

            {
                "question": "What values does range(5) produce?",
                "options": [
                    "1, 2, 3, 4, 5",
                    "0, 1, 2, 3, 4",
                    "0, 1, 2, 3, 4, 5",
                    "5 only"
                ],
                "answer": 1,
                "explanation": "range(5) starts at 0 and stops before 5."
            },

            {
                "question": "Which keyword immediately exits a loop?",
                "options": ["skip", "stop", "break", "exitloop"],
                "answer": 2,
                "explanation": "break terminates the nearest enclosing loop."
            },

            {
                "question": "Which keyword skips the current loop iteration?",
                "options": ["pass", "continue", "break", "return"],
                "answer": 1,
                "explanation": "continue skips the rest of the current iteration."
            },

            {
                "question": "How many times does for i in range(3) execute?",
                "options": ["2", "3", "4", "It never runs"],
                "answer": 1,
                "explanation": "range(3) produces 0, 1 and 2."
            },

            {
                "question": "What is an infinite loop?",
                "options": [
                    "A loop that runs exactly once",
                    "A loop that never starts",
                    "A loop that does not reach its stopping condition",
                    "A loop inside a function"
                ],
                "answer": 2,
                "explanation": "An infinite loop continues indefinitely unless interrupted."
            },

            {
                "question": "Which loop is usually suitable when the number of repetitions is known?",
                "options": ["for", "while", "if", "try"],
                "answer": 0,
                "explanation": "A for loop is commonly used when iterating over a known sequence or range."
            },

            {
                "question": "What does the pass keyword do?",
                "options": [
                    "Ends the loop",
                    "Skips the entire program",
                    "Does nothing and acts as a placeholder",
                    "Repeats the previous iteration"
                ],
                "answer": 2,
                "explanation": "pass is a placeholder statement that performs no action."
            },

            {
                "question": "What is the output of for x in range(2): print(x)?",
                "options": ["1 and 2", "0 and 1", "0, 1 and 2", "2 only"],
                "answer": 1,
                "explanation": "range(2) produces 0 and 1."
            }

        ],

        # =====================================
        # PYTHON LISTS
        # =====================================

        "lists": [

            {
                "question": "Which brackets are used to create a Python list?",
                "options": ["()", "{}", "[]", "<>"],
                "answer": 2,
                "explanation": "Python lists are written using square brackets."
            },

            {
                "question": "Are Python lists mutable?",
                "options": [
                    "Yes, they can be changed",
                    "No, they cannot be changed",
                    "Only strings can change",
                    "Only numbers can change"
                ],
                "answer": 0,
                "explanation": "Lists are mutable, meaning their elements can be changed."
            },

            {
                "question": "What is the index of the first item in a Python list?",
                "options": ["1", "-1", "0", "It has no index"],
                "answer": 2,
                "explanation": "Python uses zero-based indexing."
            },

            {
                "question": "Which method adds an item to the end of a list?",
                "options": ["add()", "append()", "insert_end()", "push()"],
                "answer": 1,
                "explanation": "append() adds one item to the end of a list."
            },

            {
                "question": "What does len(my_list) return?",
                "options": [
                    "The last item",
                    "The number of items",
                    "The list index",
                    "The largest item"
                ],
                "answer": 1,
                "explanation": "len() returns the number of elements in a list."
            },

            {
                "question": "Which method removes an item by its value?",
                "options": ["delete()", "remove()", "clear_one()", "pop_value()"],
                "answer": 1,
                "explanation": "remove(value) removes the first matching value."
            },

            {
                "question": "What does my_list[0] access?",
                "options": ["The first item", "The second item", "The last item", "The list length"],
                "answer": 0,
                "explanation": "Index 0 refers to the first item."
            },

            {
                "question": "Which method sorts a list in place?",
                "options": ["order()", "sort()", "sorted_in()", "arrange()"],
                "answer": 1,
                "explanation": "sort() sorts the existing list in place."
            },

            {
                "question": "What does pop() do without an index?",
                "options": [
                    "Removes the first item",
                    "Removes and returns the last item",
                    "Deletes the whole list",
                    "Sorts the list"
                ],
                "answer": 1,
                "explanation": "pop() removes and returns the last item by default."
            },

            {
                "question": "Can a Python list contain different data types?",
                "options": ["Yes", "No", "Only integers", "Only strings"],
                "answer": 0,
                "explanation": "A Python list can contain different data types."
            }

        ],

        # =====================================
        # NUMPY BASICS
        # =====================================

        "numpy": [

            {
                "question": "What is NumPy mainly used for?",
                "options": [
                    "Building websites",
                    "Numerical computing and arrays",
                    "Sending emails",
                    "Creating presentations"
                ],
                "answer": 1,
                "explanation": "NumPy provides efficient arrays and numerical computing tools."
            },

            {
                "question": "Which statement commonly imports NumPy?",
                "options": [
                    "import numpy as np",
                    "include numpy",
                    "using numpy",
                    "import np as numpy"
                ],
                "answer": 0,
                "explanation": "The common convention is import numpy as np."
            },

            {
                "question": "Which function creates a NumPy array?",
                "options": ["np.list()", "np.array()", "np.make()", "np.table()"],
                "answer": 1,
                "explanation": "np.array() creates a NumPy array."
            },

            {
                "question": "What does the shape attribute tell you?",
                "options": [
                    "The array dimensions",
                    "The data type only",
                    "The largest value",
                    "The array sum"
                ],
                "answer": 0,
                "explanation": "shape gives the size of the array along each dimension."
            },

            {
                "question": "Which attribute gives the number of dimensions?",
                "options": ["size", "shape", "ndim", "dtype"],
                "answer": 2,
                "explanation": "ndim returns the number of dimensions."
            },

            {
                "question": "Which function calculates the average of array values?",
                "options": ["np.mean()", "np.middle()", "np.average_value()", "np.total()"],
                "answer": 0,
                "explanation": "np.mean() calculates the arithmetic mean."
            },

            {
                "question": "Which function returns the largest value?",
                "options": ["np.high()", "np.max()", "np.top()", "np.large()"],
                "answer": 1,
                "explanation": "np.max() returns the maximum value."
            },

            {
                "question": "Which is a one-dimensional NumPy array?",
                "options": [
                    "[[1, 2], [3, 4]]",
                    "[1, 2, 3]",
                    "((1, 2), (3, 4))",
                    "{1: 2, 3: 4}"
                ],
                "answer": 1,
                "explanation": "A one-dimensional array contains a single sequence of elements."
            },

            {
                "question": "What does dtype describe?",
                "options": [
                    "The array data type",
                    "The array shape",
                    "The number of rows",
                    "The average value"
                ],
                "answer": 0,
                "explanation": "dtype identifies the data type of array elements."
            },

            {
                "question": "What is broadcasting in NumPy?",
                "options": [
                    "Playing audio",
                    "Applying operations to compatible arrays of different shapes",
                    "Printing an array",
                    "Saving an array as a PDF"
                ],
                "answer": 1,
                "explanation": "Broadcasting allows operations between arrays with compatible shapes."
            }

        ],

        # =====================================
        # PANDAS BASICS
        # =====================================

        "pandas": [

            {
                "question": "What is Pandas mainly used for?",
                "options": [
                    "Data manipulation and analysis",
                    "Making video games",
                    "Designing web pages",
                    "Managing hardware"
                ],
                "answer": 0,
                "explanation": "Pandas provides tools for working with structured data."
            },

            {
                "question": "Which statement commonly imports Pandas?",
                "options": [
                    "import pandas as pd",
                    "include pandas",
                    "import pd as pandas",
                    "using pandas"
                ],
                "answer": 0,
                "explanation": "The standard convention is import pandas as pd."
            },

            {
                "question": "Which Pandas structure is two-dimensional?",
                "options": ["Series", "DataFrame", "Index", "Scalar"],
                "answer": 1,
                "explanation": "A DataFrame is a two-dimensional table."
            },

            {
                "question": "Which Pandas structure is one-dimensional?",
                "options": ["DataFrame", "Series", "Workbook", "MatrixFrame"],
                "answer": 1,
                "explanation": "A Series is a one-dimensional labeled array."
            },

            {
                "question": "Which function reads a CSV file?",
                "options": [
                    "pd.open_csv()",
                    "pd.read_csv()",
                    "pd.load_table()",
                    "pd.csv_read()"
                ],
                "answer": 1,
                "explanation": "pd.read_csv() loads data from a CSV file."
            },

            {
                "question": "Which command displays the first five rows by default?",
                "options": ["df.tail()", "df.first()", "df.head()", "df.start()"],
                "answer": 2,
                "explanation": "df.head() displays the first five rows by default."
            },

            {
                "question": "Which attribute reports rows and columns?",
                "options": ["df.shape", "df.size()", "df.dimension", "df.length"],
                "answer": 0,
                "explanation": "df.shape returns a tuple containing rows and columns."
            },

            {
                "question": "Which method gives summary statistics?",
                "options": ["df.summary()", "df.describe()", "df.info_values()", "df.statistics()"],
                "answer": 1,
                "explanation": "df.describe() provides statistics such as count, mean and standard deviation."
            },

            {
                "question": "How do you select a column named Age?",
                "options": ["df(Age)", "df['Age']", "df{Age}", "df->Age"],
                "answer": 1,
                "explanation": "Use df['Age'] to select the Age column."
            },

            {
                "question": "Which method is commonly used to find missing values?",
                "options": ["df.empty()", "df.isnull()", "df.missing()", "df.find_na()"],
                "answer": 1,
                "explanation": "df.isnull() returns True where values are missing."
            }

        ]

    }

    return quizzes.get(quiz_topic)


# =========================================
# GENERATE QUIZ AS TEXT
# =========================================

def generate_quiz(subject, level, topic):

    questions = get_quiz_questions(
        subject,
        level,
        topic
    )

    if not questions:
        return (
            "No quiz is available for this topic yet. "
            "Try Python Functions, Python Loops, Python Lists, "
            "NumPy Basics or Pandas Basics."
        )

    output = [
        f"# Quiz: {topic}",
        f"**Subject:** {subject}",
        f"**Level:** {level}",
        ""
    ]

    for index, question in enumerate(questions, start=1):

        output.append(
            f"## Q{index}. {question['question']}"
        )

        for option_index, option in enumerate(question["options"]):

            output.append(
                f"{chr(65 + option_index)}. {option}"
            )

        output.append("")

    return "\n".join(output)
