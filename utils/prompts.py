from typing import Any

class Prompt:
    """提示抽象類別"""

    def __init__(self, template, variables=None):
        self.template = template
        self.variables = variables or {}

    def format(self):
        """格式化提示"""
        return self.template.format(**self.variables)
    
    def set_variable(self, name: str, value: Any):
        self.variables[name] = value

    @classmethod
    def from_template(cls, template):
        """從模板創建提示"""
        return cls(template)

    @classmethod
    def from_template_and_variables(cls, template, variables):
        """從模板和變數創建提示"""
        return cls(template, variables)