import inspect
from agent import describe_tools, tool_map

def test_tool_parameters_match_actual_function_signature():
    for tool in describe_tools():
        tool_name = tool["name"]
        declared_params = set(tool["parameters"]["properties"].keys())

        actual_function = tool_map[tool_name]
        actual_params = set(inspect.signature(actual_function).parameters.keys())

        assert declared_params.issubset(actual_params), (
            f"{tool_name}: schema declares {declared_params}, "
            f"but actual function only accepts {actual_params}"
        )