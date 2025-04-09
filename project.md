# Lomen Project Implementation Guide

## Project Overview

Build a Python package `lomen` for managing blockchain/web3 tools through plugins. Each plugin:

- Contains related tools
- Manages its own credentials
- Provides framework-specific tool exports (LangChain/MCP)
- Validates credentials during initialization

## Technical Requirements

1. **Python**: 3.10+
2. **Dependencies**:
   - Pydantic &gt;=2.0
   - langchain &gt;=0.1.0
   - python-dotenv &gt;=1.0.0
   - aiohttp &gt;=3.9.0
3. **Tooling**:
   - UV for package management
   - pytest for testing
   - Black for formatting
   - Ruff for linting

## Directory Structure

```

src/
└── lomen/
├── **init**.py
├── adapters/
│ ├── **init**.py
│ ├── langchain.py
│ └── mcp.py
└── plugins/
├── **init**.py
├── base.py
├── 1inch/
│ ├── **init**.py
│ ├── tools.py
│ └── api.py
└── uniswap/
├── **init**.py
└── tools.py

```

## Core Components Implementation

### 1. Plugin Base Class

````

# plugins/base.py

from pydantic import BaseModel
from typing import List, Type, Dict, Any

class BasePlugin:
def **init**(self, credentials: Dict[str, Any]):
self.credentials = credentials
self.\_validate_credentials()

    @property
    def name(self) -&gt; str:
        raise NotImplementedError

    @property
    def required_credentials(self) -&gt; List[str]:
        return []

    def _validate_credentials(self):
        missing = [key for key in self.required_credentials
                  if key not in self.credentials]
        if missing:
            raise ValueError(f"Missing credentials: {missing}")
    class BaseTool:

@classmethod
@property
def name(cls) -> str:
raise NotImplementedError

    @classmethod
    def execute(cls, params: BaseModel, credentials: Dict[str, Any]):
        raise NotImplementedError
    ```

### 2. LangChain Adapter

````

# adapters/langchain.py

from langchain.tools import BaseTool as LCBaseTool

class LangChainAdapter:
@staticmethod
def convert(tool_cls, credentials):
class LCTool(LCBaseTool):
name = tool_cls.name
args_schema = tool_cls.Params

            def _run(self, **kwargs):
                return tool_cls.execute(kwargs, credentials)

        return LCTool()
    ```

### 3. 1inch Plugin Implementation

````

# plugins/1inch/**init**.py

from .tools import SwapTool
from ..base import BasePlugin

class OneInchPlugin(BasePlugin):
@property
def name(self):
return "1inch"

    @property
    def required_credentials(self):
        return ["API_KEY"]

    @property
    def tools(self):
        return [SwapTool]

# plugins/1inch/tools.py

from pydantic import BaseModel, Field

class SwapParams(BaseModel):
amount: int = Field(..., gt=0)

class SwapTool:
name = "1inch_swap"

    class Params(BaseModel):
        amount: int = Field(..., gt=0)

    @classmethod
    def execute(cls, params: Params, credentials: dict):
        api_key = credentials["API_KEY"]
        # Implementation
    ```

## Testing Requirements

1. **Credential Validation**:

```

def test_credential_validation():
with pytest.raises(ValueError):
OneInchPlugin(credentials={})

```

2. **Tool Execution**:

```

def test_swap_tool():
plugin = OneInchPlugin(credentials={"API_KEY": "test"})
tool = plugin.tools
assert tool.name == "1inch_swap"

```

## Usage Examples

```


# Initialize plugin with credentials

plugin = OneInchPlugin(credentials={"API_KEY": "123"})

# Get LangChain tools

lc_tools = [LangChainAdapter.convert(t, plugin.credentials)
for t in plugin.tools]

# Direct tool access

from lomen.plugins.1inch import SwapTool
params = SwapTool.Params(amount=100)
SwapTool.execute(params, {"API_KEY": "123"})

```

## Implementation Notes

1. **Error Handling**:
   - Raise `ValueError` with missing credential names
   - Use Pydantic validation for parameters
2. **Documentation**:
   - Add docstrings to all public methods
   - Generate API docs using MkDocs
3. **Packaging**:
   - Use `pyproject.toml` for modern packaging
   - Include type hints for better IDE support

## Deliverables

1. Complete Python package structure
2. Unit tests with 90%+ coverage
3. Example implementations for 1inch plugin
4. Documentation for plugin development
5. CI/CD pipeline configuration (GitHub Actions)

```

This prompt provides detailed specifications for a coding agent to implement the Lomen package while maintaining the core design principles of plugin-centric architecture and upfront credential validation.
````
