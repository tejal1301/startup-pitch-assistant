def generate_prompt(industry, idea, audience):
    return f"""
    Act as a startup founder. I have an idea in the {industry} industry.

    Idea: {idea}

    Help me prepare a startup pitch for an audience of {audience}. Please return:

    1. Elevator Pitch
    2. Problem Statement
    3. Solution Overview
    4. Target Customer
    5. Unique Value Proposition
    6. Market Potential
    """
