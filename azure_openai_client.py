#!/usr/bin/env python3
"""
Standalone Azure OpenAI Client
A minimal, self-contained implementation for using Azure OpenAI.
"""

import os
import logging
from typing import Dict, Any, Optional
from azure.identity import ClientSecretCredential
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AzureOpenAIClient:
    """
    Standalone Azure OpenAI client with direct secret configuration.
    """
    
    def __init__(self, secrets: Dict[str, str]):
        """
        Initialize Azure OpenAI client with provided secrets.
        
        Args:
            secrets: Dictionary containing Azure configuration
                Required keys:
                - azure_tenant_id: Azure tenant ID
                - azure_client_id: Azure client ID  
                - azure_client_secret: Azure client secret
                - azure_endpoint: Azure OpenAI endpoint
                - azure_deployment_name: Model deployment name (optional, defaults to 'gpt-4')
                - azure_api_version: API version (optional, defaults to '2024-02-15-preview')
        """
        self.secrets = secrets
        self._validate_secrets()
        self._setup_azure_credentials()
        self._initialize_langchain_client()
    
    def _validate_secrets(self):
        """Validate that all required secrets are provided."""
        required_keys = [
            'azure_tenant_id',
            'azure_client_id', 
            'azure_client_secret',
            'azure_endpoint'
        ]
        
        missing_keys = [key for key in required_keys if not self.secrets.get(key)]
        if missing_keys:
            raise ValueError(f"Missing required secrets: {missing_keys}")
    
    def _setup_azure_credentials(self):
        """Setup Azure credentials using client secret authentication."""
        self.credential = ClientSecretCredential(
            tenant_id=self.secrets['azure_tenant_id'],
            client_id=self.secrets['azure_client_id'],
            client_secret=self.secrets['azure_client_secret']
        )
        
        logger.info("Azure credentials configured successfully")
    
    def _initialize_langchain_client(self):
        """Initialize the LangChain Azure OpenAI client."""
        self.llm = AzureChatOpenAI(
            azure_endpoint=self.secrets['azure_endpoint'],
            azure_deployment=self.secrets.get('azure_deployment_name', 'gpt-4'),
            api_version=self.secrets.get('azure_api_version', '2024-02-15-preview'),
            azure_ad_token_provider=lambda: self.credential.get_token("https://cognitiveservices.azure.com/.default").token,
            temperature=0.1,
            max_tokens=4000
        )
        logger.info("LangChain Azure OpenAI client initialized")
    
    def get_langchain(self):
        """Get the LangChain client instance."""
        return self.llm
    
    def chat(self, message: str, system_message: Optional[str] = None) -> str:
        """
        Simple chat interface.
        
        Args:
            message: User message
            system_message: Optional system message
            
        Returns:
            AI response as string
        """
        messages = []
        
        if system_message:
            messages.append(SystemMessage(content=system_message))
        
        messages.append(HumanMessagePromptTemplate.from_template(message))
        
        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | self.llm
        
        response = chain.invoke({})
        return response.content.strip()
    
    def chat_with_template(self, template: str, variables: Dict[str, str], system_message: Optional[str] = None) -> str:
        """
        Chat using a template with variables.
        
        Args:
            template: Prompt template with {variable} placeholders
            variables: Dictionary of variables to substitute
            system_message: Optional system message
            
        Returns:
            AI response as string
        """
        messages = []
        
        if system_message:
            messages.append(SystemMessage(content=system_message))
        
        messages.append(HumanMessagePromptTemplate.from_template(template))
        
        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | self.llm
        
        response = chain.invoke(variables)
        return response.content.strip()


def create_client_from_env() -> AzureOpenAIClient:
    """
    Create client using environment variables.
    
    Required environment variables:
    - AZURE_TENANT_ID
    - AZURE_CLIENT_ID
    - AZURE_CLIENT_SECRET
    - AZURE_ENDPOINT
    - AZURE_DEPLOYMENT_NAME (optional)
    - AZURE_API_VERSION (optional)
    """
    secrets = {
        'azure_tenant_id': os.getenv('AZURE_TENANT_ID'),
        'azure_client_id': os.getenv('AZURE_CLIENT_ID'),
        'azure_client_secret': os.getenv('AZURE_CLIENT_SECRET'),
        'azure_endpoint': os.getenv('AZURE_ENDPOINT'),
        'azure_deployment_name': os.getenv('AZURE_DEPLOYMENT_NAME', 'gpt-4'),
        'azure_api_version': os.getenv('AZURE_API_VERSION', '2024-02-15-preview')
    }
    
    return AzureOpenAIClient(secrets)


def create_client_from_dict(secrets: Dict[str, str]) -> AzureOpenAIClient:
    """
    Create client using provided secrets dictionary.
    
    Args:
        secrets: Dictionary with Azure configuration
    """
    return AzureOpenAIClient(secrets)


# Example usage
if __name__ == "__main__":
    # Method 1: Using environment variables
    try:
        client = create_client_from_env()
        
        # Simple chat
        response = client.chat(
            "Hello! Can you explain what a factory pattern is?",
            system_message="You are a helpful software engineering assistant."
        )
        print("Response:", response)
        
    except Exception as e:
        logger.error(f"Error: {e}")
        print("Make sure to set the required environment variables:")
        print("- AZURE_TENANT_ID")
        print("- AZURE_CLIENT_ID") 
        print("- AZURE_CLIENT_SECRET")
        print("- AZURE_ENDPOINT")
        print("- AZURE_DEPLOYMENT_NAME (optional)")
        print("- AZURE_API_VERSION (optional)")
