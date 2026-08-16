import unittest

try:
    from mcp import Client
    from okitsok.mcp_server import mcp
    HAS_MCP = True
except (ImportError, RuntimeError):
    HAS_MCP = False


@unittest.skipUnless(HAS_MCP, "optional MCP dependencies are not installed")
class MCPServerTests(unittest.IsolatedAsyncioTestCase):
    async def test_about_tool_is_available(self):
        async with Client(mcp) as client:
            result = await client.call_tool("about_isdomainok", {})

        payload = result.structured_content or {}
        self.assertEqual(payload.get("name"), "IsDomainOK")
        self.assertFalse(payload.get("purchasing_supported"))
        self.assertTrue(payload.get("local_first"))


if __name__ == "__main__":
    unittest.main()
