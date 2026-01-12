import ast # code into tree
import os # environment variables
import uvicorn # server
from fastapi import FastAPI # web framework
from pydantic import BaseModel # data validation
from dotenv import load_dotenv # load .env file

from aaa_analyzer import AAAAnalyzer # AAAAnalyzer class

# --- SEGMENT 1: SETUP & SECURITY ---
load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("GEMINI_API_KEY")  # Get API key from environment variable
if not api_key:
    raise ValueError ("❌ No API Key found! Check your .env file.")

# Configure AI model with secure API key
analyzer = AAAAnalyzer(api_key=api_key, model_name="gemini-3-flash-preview")

app = FastAPI()

class CodeSnippet(BaseModel): #pydantic model that stores the code snippet in the form of a string
    code: str

"""    Removed logic in favor of XML-based analysis via Gemini LLM
# -- THE LOGIC (AST) --
def check_structure(code_str):
    try:
        tree = ast.parse(code_str) # Parse code into AST
        for node in ast.walk(tree): # Walk through AST nodes
            if isinstance(node, ast.Assert): # Check for assert statements within the nodes
                return True
        return False # returns False if no assert statements are found
    except SyntaxError: #returns False if there is a syntax error
        return False
"""

# testing uvicorn server
@app.get("/")
def home():
    return {"message": "Server is Running! Use the VS Code extension to send data."}

# -- THE ENDPOINTS --
@app.post("/analyze")
async def analyze_code(snippet: CodeSnippet):
    print("Received code for analysis...")

    # 1. Generate the AST (Abstract Syntax Tree)
    # The System Prompt expects an <ast> block to understand the code structure.
    try:
        tree = ast.parse(snippet.code)
        # indent=2 makes it readable for the LLM
        ast_string = ast.dump(tree, indent=2)
    except SyntaxError:
        return {
            "message": "❌ Syntax Error",
            "analysis_result": "<analysis><error>Invalid Python Code</error></analysis>"
        }
    
    # 2. Format input as XML, matche the format expected in aaa_analyzer.py
    formatted_input = f"""
    <test_code>
    {snippet.code}
    </test_code>

    <ast>
    {ast_string}
    </ast>
    
    <<production_code>
    # Not provided in this context
    </production_code>
    """

    # 3. Call the Analyzer (Gemini)
    try:
        result = analyzer.analyze(formatted_input)

        return {
            "message": "✅ Analysis Complete",
            "analysis_result": result
        }
    except Exception as e:
        return {
            "message": "❌ Analysis Failed",
            "analysis_result": f"Error: {str(e)}"
        }

# --- RUNNER ---
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)