# Author: Sai Shankar
# TID: T0159ZN
# Date: 2024-03-17
# Description: BCA-BSW IOHWAB Test Automation Framework Report Generation

from jinja2 import Template
import os

class html_report_generator:
    def __init__(self, data:dict):
        self.report_data:dict = data

    def generate_report(self):
        template_path:str = os.path.join(os.path.dirname(__file__), '../inputs/report_tempate.html')
        with open(template_path, '+r') as file:
            template = Template(file.read())

        html_report:str = template.render(data=self.report_data)
        report_path:str = os.path.join(os.path.dirname(__file__), '../out/BCA_test_report.html')

        with open(report_path, "w") as f:
            f.write(html_report)

        print("Successfully report generated")
        