#!/usr/bin/env python3
"""
Working example using .env file for Azure OpenAI client.
"""

from dotenv import load_dotenv
from azure_openai_client import create_client_from_env

def main():
    print("Azure OpenAI Client - Working Example")
    print("=" * 50)
    
    # Load environment variables from .env file
    load_dotenv()
    
    try:
        # Create client
        print("Creating Azure OpenAI client...")
        client = create_client_from_env()
        print("✓ Client created successfully!\n")
        
        # Example 1: Simple chat
        print("=== Example 1: Simple Chat ===")
        response = client.chat(
            "What is the factory pattern in software design?",
            system_message="You are a software engineering expert. Provide clear, concise explanations."
        )
        print("Response:")
        print(response)
        print("\n" + "=" * 50 + "\n")
        
        # Example 2: Code review with template
        print("=== Example 2: Code Review with Template ===")
        code_to_review = """
                            def calculate_fibonacci(n):
                                if n <= 1:
                                    return n
                                return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
                        """
        
        response = client.chat_with_template(
            "Please review this {language} code for potential improvements:\n\n{code}",
            {
                "language": "Python",
                "code": code_to_review
            },
            system_message="You are a senior Python developer. Provide constructive feedback on code quality, performance, and best practices."
        )
        
        print("Code Review Result:")
        print(response)
        print("\n" + "=" * 50 + "\n")
        
        # Example 3: LangChain integration
        print("=== Example 3: LangChain Integration ===")
        try:
            from langchain_core.prompts import PromptTemplate
            from langchain_core.output_parsers import StrOutputParser
            
            llm = client.get_langchain()
            
            # Create a prompt template
            prompt = PromptTemplate(
                input_variables=["topic", "audience"],
                template="Explain {topic} to a {audience} in simple terms."
            )
            
            # Create a chain
            chain = prompt | llm | StrOutputParser()
            
            # Invoke the chain
            response = chain.invoke({
                "topic": "machine learning",
                "audience": "beginner programmer"
            })
            
            print("LangChain Chain Response:")
            print(response)
            
        except ImportError:
            print("LangChain integration example skipped (dependencies not available)")
        
        print("\n" + "=" * 50)
        print("✓ All examples completed successfully!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        print("Please check your .env file configuration.")

if __name__ == "__main__":
    main()
