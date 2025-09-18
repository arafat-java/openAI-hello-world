# Standalone Azure OpenAI Client

A minimal, self-contained Azure OpenAI client that you can easily port to any project.

## Files

- `azure_openai_client.py` - The main client implementation
- `example.py` - Usage examples with your credentials
- `requirements.txt` - Minimal dependencies
- `config_template.env` - Configuration template

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Credentials

#### Option A: Environment Variables
Copy `config_template.env` to `.env` and fill in your values:

```bash
cp config_template.env .env
```

#### Option B: Direct Configuration
Update the secrets dictionary in `example.py` with your actual credentials.

### 3. Run Examples

```bash
python example.py
```

## Usage

### Basic Chat

```python
from azure_openai_client import create_client_from_dict

secrets = {
    'azure_tenant_id': 'your-tenant-id',
    'azure_client_id': 'your-client-id',
    'azure_client_secret': 'your-client-secret',
    'azure_endpoint': 'https://your-resource.openai.azure.com/',
    'azure_deployment_name': 'gpt-4'
}

client = create_client_from_dict(secrets)
response = client.chat("Hello, how are you?")
print(response)
```

### Template-based Chat

```python
response = client.chat_with_template(
    "Review this {language} code: {code}",
    {
        "language": "Python",
        "code": "def hello():\n    print('Hello')"
    },
    system_message="You are a code reviewer."
)
```

### LangChain Integration

```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = client.get_langchain()
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} in simple terms."
)
chain = prompt | llm | StrOutputParser()
response = chain.invoke({"topic": "machine learning"})
```

## Porting to New Project

1. Copy these 4 files to your new project:
   - `azure_openai_client.py`
   - `requirements.txt`
   - `config_template.env`
   - `README.md` (optional)

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your Azure credentials

4. Import and use:
   ```python
   from azure_openai_client import create_client_from_dict
   ```

That's it! No external dependencies or complex setup required.
