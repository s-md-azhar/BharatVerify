import os
from google import genai
from google.genai import types

def test_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    print("Testing connection...")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents="Say 'Hello, World!'"
    )
    print("Connection OK:", response.text)
    
    print("\nTesting structured output...")
    print("\nTesting Pydantic schema validation...")
    from pydantic import BaseModel, Field
    class PersonInfo(BaseModel):
        name: str = Field(description="The person's name")
        age: int = Field(description="The person's age")
        
    response2 = client.models.generate_content(
        model='gemini-2.5-flash',
        contents="My name is Alice and I am 30 years old.",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=PersonInfo,
            temperature=0.0
        ),
    )
    print("Pydantic Validation OK:", response2.text)
    
    print("\nTesting multi-step function calling...")
    def get_current_weather(location: str):
        return f"Weather in {location} is 72F."
    
    tool = types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="get_current_weather",
                description="Get the current weather in a given location",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "location": types.Schema(type=types.Type.STRING, description="The city and state, e.g. San Francisco, CA")
                    },
                    required=["location"]
                )
            )
        ]
    )
    
    chat = client.chats.create(model='gemini-2.5-flash', config=types.GenerateContentConfig(tools=[tool]))
    response3 = chat.send_message("What's the weather in San Francisco?")
    if response3.function_calls:
        func_call = response3.function_calls[0]
        print("Function Call OK:", func_call.name, func_call.args)
        
        # Step 2: Send function response
        func_resp = get_current_weather(func_call.args["location"])
        response4 = chat.send_message([types.Part.from_function_response(
            name=func_call.name,
            response={"result": func_resp}
        )])
        print("Multi-step Workflow Final Response OK:", response4.text)
    else:
        print("Function Call FAILED")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    test_gemini()
