# Using Lomen with UVX as an MCP Server

This example demonstrates how to set up and use Lomen with UVX as an MCP server, particularly for integrating with tools like Cursor or Visual Studio Code.

## Prerequisites

1. Install Lomen: `pip install lomen`
2. Set up your environment variables (API keys) - create a `.env` file based on the project's `.env.example`

## Running Lomen MCP Server

You can start the Lomen MCP server using the `uvx` command:

```bash
# Run with all available plugins
uvx lomen --all

# Or run with specific plugins
uvx lomen --plugins oneinch,blockchain

# Customize host and port if needed
uvx lomen --all --host 127.0.0.1 --port 8080
```

## Integrating with Cursor

To integrate Lomen with Cursor, you'll need to update your Cursor configuration to include Lomen as an MCP server. Here's how to set it up:

1. Open Cursor settings
2. Navigate to the MCP Servers section
3. Add a new MCP server configuration:

```json
"mcpServers": {
  "Lomen": {
    "command": "uvx",
    "args": [
      "lomen",
      "--all"
    ],
    "env": {
      "ONEINCH_API_KEY": "your_1inch_api_key",
      "BLOCKCHAIN_API_KEY": "your_blockchain_api_key"
    }
  }
}
```

4. Save the configuration

## Testing the Integration

Once integrated, you can test the connection by asking Cursor to perform blockchain-related tasks. For example:

1. Ask about Ethereum's current block number
2. Request token info for a specific symbol
3. Query balance information for a wallet address

The MCP integration allows Cursor to directly use Lomen's tools and execute blockchain operations based on your natural language requests.

## Troubleshooting

If you encounter issues:

1. **API Key Errors**: Ensure your environment variables are set correctly
2. **Connection Issues**: Check that the Lomen server is running and accessible
3. **Tool Errors**: Review the server logs for specific error messages

For more detailed information, refer to the [Lomen documentation](https://github.com/username/lomen#readme).
