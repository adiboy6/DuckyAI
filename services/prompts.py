import re

def quick_chat_system_prompt() -> str:
    return f"""
            Forget all previous instructions.
        You are a chatbot named Fred. You are assisting a software developer
        with their software development tasks.
        Each time the user converses with you, make sure the context is about
        * software development,
        * or coding,
        * or debugging,
        * or code reviewing,
        and that you are providing a helpful response.

        If the user asks you to do something that is not
        concerning one of those topics, you should refuse to respond.
        """

def system_learning_prompt() -> str:
    return """
    You are assisting a user with their general software development tasks.
Each time the user converses with you, make sure the context is generally about software development,
or creating a course syllabus about software development,
and that you are providing a helpful response.
If the user asks you to do something that is not concerning software
in the least, you should refuse to respond.
"""


def learning_prompt(learner_level: str, answer_type: str, topic: str) -> str:
    return f"""
Please disregard any previous context.

The topic at hand is ```{topic}```.
Analyze the sentiment of the topic.
If it does not concern software development or creating an online course syllabus about software development,
you should refuse to respond.

You are now assuming the role of a highly acclaimed software engineer specializing in the topic
 at a prestigious software company.  You are assisting a fellow software engineer with
 their software development tasks.
You have an esteemed reputation for presenting complex ideas in an accessible manner.
Your colleague wants to hear your answers at the level of a {learner_level}.

Please develop a detailed, comprehensive {answer_type} to teach me the topic as a {learner_level}.
The {answer_type} should include high level advice, key learning outcomes,
detailed examples, step-by-step walkthroughs if applicable,
and major concepts and pitfalls people associate with the topic.

Make sure your response is formatted in markdown format.
Ensure that embedded formulae are quoted for good display.
"""

############################################################################################################
# Requirements prompts
############################################################################################################

def system_requirements_prompt(product_name, product_description):
    """
    Generate a system requirements prompt based on the product name and description
    Args:
        product_name: The name of a product described in a system prompt
        product_description: A description of the product

    Returns:
        A prompt to use as a system prompt for making requirements documents for the product name and description.

    """
    return f"""
    Forget all previous instructions and context.

    You are an expert in requirements engineering.

    Your job is to learn and understand the following text about a product named {product_name}.
    ```
    {product_description}
    ```
    """

def requirements_prompt(product_name, requirement_type):
    """
    Generate a requirements prompt based on the requirement type and product name.
    Args:
        product_name: the name of a product described in a system prompt
        requirement_type: ["Business Problem Statement", "Vision Statement", "Ecosystem map", "RACI Matrix"]

    Returns:
        A prompt to use to generate a requirements document
        for the requirement type and product name.
    """
    if requirement_type not in ["Business Problem Statement", "Vision Statement", "Ecosystem map", "RACI Matrix"]:
        raise ValueError(f"Invalid requirement type.")
    if requirement_type == "Business Problem Statement":
        return business_problem_prompt(product_name)
    if requirement_type == "Vision Statement":
        return vision_statement_prompt(product_name)
    if requirement_type == "Ecosystem map":
        return ecosystem_map_prompt(product_name)
    if requirement_type == "RACI Matrix":
        return responsibility_matrix_prompt(product_name)

def business_problem_prompt(product_name):
    """
    Derive a business problem statement prompt using textbook guidelines.
    """
    try:
        with open("data/textbook.txt", "r", encoding="utf-8") as f:
            textbook_content = f.read()
    except Exception as e:
        textbook_content = "Textbook content not available."
    return (
        f"Based on the following textbook excerpt:\n\n{textbook_content}\n\n"
        f"Please develop a detailed Business Problem Statement for the product '{product_name}'. "
        "Include descriptions of the underlying business challenges, the market need, and any operational or financial issues that the product addresses."
    )


def vision_statement_prompt(product_name):
    """
    Derive a vision statement prompt using textbook guidelines.
    """
    try:
        with open("data/textbook.txt", "r", encoding="utf-8") as f:
            textbook_content = f.read()
    except Exception as e:
        textbook_content = "Textbook content not available."
    return (
        f"Using the insights provided in the following textbook excerpt:\n\n{textbook_content}\n\n"
        f"Create a compelling Vision Statement for the product '{product_name}'. "
        "The statement should capture the product's long-term aspirations, strategic direction, and overall impact."
    )


def ecosystem_map_prompt(product_name):
    """
    Derive an ecosystem map prompt using textbook guidelines.
    """
    try:
        with open("data/textbook.txt", "r", encoding="utf-8") as f:
            textbook_content = f.read()
    except Exception as e:
        textbook_content = "Textbook content not available."
    return (
        f"Referencing the guidelines below from the textbook:\n\n{textbook_content}\n\n"
        f"Develop a detailed Ecosystem Map for the product '{product_name}'. Include all relevant stakeholders, partners, and resources that interact with or support the product."
    )


def responsibility_matrix_prompt(product_name):
    """
    Derive a responsibility (RACI) matrix prompt using textbook guidelines.
    """
    try:
        with open("data/textbook.txt", "r", encoding="utf-8") as f:
            textbook_content = f.read()
    except Exception as e:
        textbook_content = "Textbook content not available."
    return (
        f"Based on the methodologies described in the textbook excerpt below:\n\n{textbook_content}\n\n"
        f"Generate a Responsibility Matrix (RACI Matrix) for the product '{product_name}'. "
        "Clearly outline the roles involved and identify who is Responsible, Accountable, Consulted, and Informed for each key task or decision."
    )


############################################################################################################
# Code Generation prompts
############################################################################################################

def parse_code_and_request(user_input: str):
    """
    Parses the user's composite input to extract the code (delimited by triple backticks)
    and the plain-text request. Returns (extracted_code, request_text).
    """
    code_blocks = re.findall(r"```(.*?)```", user_input, flags=re.DOTALL)
    if code_blocks:
        code_extracted = code_blocks[0].strip()
    else:
        code_extracted = ""

    # Remove code blocks from the original input
    request_text = re.sub(r"```.*?```", "", user_input, flags=re.DOTALL).strip()
    return code_extracted, request_text

def classify_user_prompt(user_input: str) -> str:
    
    return f"""
    You are an AI classification system. A user provides a short request related to code and software development. 
    Your task is to categorize the request into one of the following four classes:
    Here's the prompt: {user_input}

    review – if the user is asking to critique, evaluate, or highlight problems in the code.
    modify – if the user is asking to change, alter, or update the code.
    debug – if the user is asking to fix or troubleshoot an error in the code.
    misc – if the user’s request does not clearly fit any of the above categories.

    Output only the single category (“review,” “modify,” “debug,” or “misc”) 
    that best represents the user’s request, based on the content of their prompt. 
    Provide no additional explanation or commentary.
    """.format(user_input)

def review_prompt(existing_code: str) -> str:
    # Implementing a code review prompt that includes the existing code snippet
    review = f"""
    Code Review for:
    {existing_code}

    1. Ensure proper naming conventions are followed.
    2. Check for any unused imports or variables.
    3. Verify that the code is properly documented.
    4. Ensure that the code follows PEP 8 guidelines.
    5. Check for any potential performance improvements.
    """
    return review

def modify_code_prompt(user_prompt: str, existing_code: str) -> str:
    # Implementing a code modification prompt that includes the existing code snippet
    # and the user's requested modification
    modified_code = f"""
    Original Code:
    {existing_code}

    # User requested modification: {user_prompt}
    """
    return modified_code

def debug_prompt(debug_error_string: str, existing_code: str) -> str:
    # Implementing a debug prompt that includes the existing code snippet
    # and suggestions for debugging based on the provided error string
    debug_suggestions = f"""
    Debugging Suggestions for error '{debug_error_string}' in:
    {existing_code}

    1. Check the line number mentioned in the error message.
    2. Verify the variable names and their values.
    3. Ensure that all necessary imports are included.
    4. Check for any syntax errors or typos.
    5. Use print statements or a debugger to trace the issue.
    """
    return debug_suggestions



