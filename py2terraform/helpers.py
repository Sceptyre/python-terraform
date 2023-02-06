"""
  Helper functions, encoders, etc
"""
def encode_str(value: str) -> str:
  return f'"{value}"'

def encode_bool(value: bool) -> str:
  str(value).lower()

def encode_dict(value: dict) -> str:
  return str(TerraformDict(value)).replace("\n", "\n\t")

def encode_int(value: int) -> str:
  return str(value)

def encode_list(value: list) -> str:
  strings_list = []
  for i in value:
      strings_list.append(
          TerraformDict.encode_value(i)
      )

  list_items_string = ",\n\t\t".join(strings_list)

  return f"[\n\t\t{list_items_string}\n\t]"

def encode_value(value) -> str:
  out = str(value).replace('\n', '\n\t')

  if      isinstance(value, str):
      out = TerraformDict.encode_str(value)
  elif    isinstance(value, bool):
      out = TerraformDict.encode_bool(value)
  elif    isinstance(value, list):
      out = TerraformDict.encode_list(value)
  elif    isinstance(value, TerraformBlockBase):
      if not value.is_named:
          raise Exception(f"Unable to map unamed resource {repr(value)}")

      out = repr(value)

  return out

from .types import TerraformDict, TerraformBlockBase
