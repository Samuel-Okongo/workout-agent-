import os
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.commands import Command

class  FitnessTrainerAgent(Command):
    def __init__(self):
        super().__init__()
        self.name = "fitness_trainer"
        self.description = "This agent is pretending to be highly knowleglable trainer, that create personalized workout plans."
        self.history = []
        load_dotenv()
        API_KEY = os.getenv('OPEN_AI_KEY')
        # you can try GPT4 but it costs a lot more money than the default 3.5
        self.llm = ChatOpenAI(openai_api_key=API_KEY, model="gpt-3.5-turbo")  # Initialize once and reuse
        # This is default 3.5 chatGPT
        # self.llm = ChatOpenAI(openai_api_key=API_KEY)  # Initialize once and reuse

    def calculate_tokens(self, text):
        # More accurate token calculation mimicking OpenAI's approach
        return len(text)

    def interact_with_ai(self, user_input, character_name):
        # Generate a more conversational and focused prompt
        era = '17th century england'
        prompt_text = f"Imagine you are a distinguished teacher with a deep knowledge of {era}, tasked with guiding a learner's exploration of this subject. Begin the interaction by posing an initial question that covers a foundational aspect of {era} history, ensuring it is accessible for a broad range of knowledge levels. Based on the learner's response, if they answer correctly, increase the complexity of the next question to challenge them further. Conversely, if the answer is incorrect, maintain or slightly decrease the difficulty to build their confidence and understanding. Proceed with this adaptive approach through three questions, each time providing feedback that includes corrections or additional insights as necessary. After the third question, offer a comprehensive assessment of their performance, highlighting their strengths, areas for improvement, and encouragement for their continued learning and curiosity about {era} history."
        prompt = ChatPromptTemplate.from_messages(self.history + [("system", prompt_text)])
        
        output_parser = StrOutputParser()
        chain = prompt | self.llm | output_parser

        response = chain.invoke({"input": user_input})

        # Token usage logging and adjustment for more accurate counting
        tokens_used = self.calculate_tokens(prompt_text + user_input + response)
        logging.info(f"OpenAI API call made. Tokens used: {tokens_used}")
        return response, tokens_used

    def execute(self, *args, **kwargs):
        print("Welcome to Fitness Trainer Agent!")

    age = input("Enter your age: ")
    height = input("Enter your height in cm: ")
    weight = input("Enter your weight in kg: ")
    goals = input("Describe your fitness goals: ")
    limitations = input("List any physical limitations or health concerns: ")
            
    try:
        # Generate the workout plan based on the user's input
        response, tokens_used = self.interact_with_ai(age, height, weight, goals, limitations)
        print(f"Fitness Trainer Agent:\n{response}")
        print(f"This interaction used {tokens_used} tokens.")
        self.history.append(("system", response))
    except Exception as e:
        print("Sorry, there was an error processing your workout plan. Please try again.")
        logging.error(f"Error during interaction: {e}")
        
    print("Thank you for using the Fitness Trainer Agent. Goodbye!")

