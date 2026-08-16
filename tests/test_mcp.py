import json
import unittest

try:
    from mcp import Client
    from mcp.types import TextContent
    from okitsok.mcp_server import mcp
    HAS_MCP = True
except (ImportError, RuntimeError):
    HAS_MCP = False


def _payload_from_result(result):
    payload = result.structured_content
    if isinstance(payload, dict) and isinstance(payload.get("result"), dict):
        return payload["result"]
    if isinstance(payload, dict):
        return payload

    for block in result.content:
        if HAS_MCP and isinstance(block, TextContent):
            try:
                decoded = json.loads(block.text)
            except (TypeError, json.JSONDecodeError):
                continue
            if isinstance(decoded, dict) and isinstance(decoded.get("result"), dict):
                return decoded["result"]
            if isinstance(decoded, dict):
                return decoded
    return {}


@unittest.skipUnless(HAS_MCP, "optional MCP dependencies are not installed")
class MCPServerTests(unittest.IsolatedAsyncioTestCase):
    async def test_about_tool_is_available(self):
        async with Client(mcp) as client:
            tools = await client.list_tools()
            tool_names = {tool.name for tool in tools.tools}
            self.assertIn("about_isdomainok", tool_names)
            self.assertIn("screen_names", tool_names)

            result = await client.call_tool("about_isdomainok", {})

        self.assertFalse(result.is_error)
        payload = _payload_from_result(result)
        self.assertEqual(payload.get("name"), "IsDomainOK")
        self.assertFalse(payload.get("purchasing_supported"))
        self.assertTrue(payload.get("local_first"))


if __name__ == "__main__":
    unittest.main()
