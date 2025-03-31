
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
    return f"""Create a detailed narrative that defines the current challenges and opportunities in the market for {0}.
    
    Guidelines:
    1. Describe the existing situation and market environment, including trends, competitors, and external pressures.
    2. Identify key problems or challenges that potential users encounter, emphasizing any gaps or shortcomings in current solutions.
    3. Discuss the potential implications if these challenges are not addressed, highlighting both short-term and long-term consequences.
    4. Outline the benefits and positive impact that resolving these challenges would bring to users and the overall market.
    5. Envision how {0} can transform the current scenario, providing a forward-looking perspective that aligns with market needs.
    """.format(product_name).strip()

def vision_statement_prompt(product_name):
    return f"""Create a clear and compelling vision that shows the unique future and value of {0}. 
     
    Guidelines: 
    1. Define who will use this product and what they really need and want. 
    2. Explain what makes {0} different and better than other options out there.
    3. Show how {0} helps solve real problems that users face every day.
    4. Use this format: For [who will use it], Who [what they need/want], The [product_name] Is [what makes it special] That [main benefits].
    5. Make sure the vision is practical but forward-thinking.
    6. Keep it short and memorable - something people can easily repeat.
    7. Focus on the impact it will have, not just features.
    8. Make it exciting but realistic - avoid empty buzzwords.
    """.format(product_name).strip() 
 
def ecosystem_map_prompt(product_name):
    return f"""Create a complete map showing everyone and everything that connects with {0} in some way.
     
    Guidelines: 
    1. List all the people and systems that interact with {0} - both direct (users, interfaces, data) and indirect (regulators, market trends, competitors).
    2. Clearly explain what each person or system does and how they work with {0}.
    3. Talk about outside factors like tech changes, economic issues, or new regulations that might affect how the product works.
    4. Show the connections between different parts with simple explanations.
    5. Include potential future connections that might become important later.
    6. Consider both helpful connections and possible roadblocks.
    7. Don't forget to include end users at different levels of expertise.
    """.format(product_name).strip() 
 
def responsibility_matrix_prompt(product_name):
    return f"""Make a complete RACI Matrix that clearly shows who does what for {0}. 
     
    Guidelines: 
    1. List all the key people involved with {0} (like Product Owner, Developers, QA Team, Designers, Users, etc.).
    2. Show each person's role using: Responsible (R) = does the work, Accountable (A) = makes final decisions, Consulted (C) = gives input, Informed (I) = kept updated.
    3. Make sure the chart clearly shows who handles each task without any confusion.
    4. Break down responsibilities by project phases or major activities.
    5. Make sure every important task has someone Responsible and someone Accountable.
    6. Keep it simple - avoid having too many people in any one role.
    7. Include notes about when roles might change or overlap in special cases.
    8. Consider both ongoing maintenance and one-time setup tasks.
    """.format(product_name).strip()


