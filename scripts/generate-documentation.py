import json
import os
from litellm import completion


def load_plan(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_documentation(plan):
    prompt = f"""
You are an AWS infrastructure documentation expert.

Analyze the Terraform plan JSON below and generate detailed, well-structured Markdown documentation.

Include:

# AWS Infrastructure Documentation

- Infrastructure overview
- Environment
- AWS region
- VPC and networking
- Subnets
- Route tables
- Internet/NAT gateways
- Security groups
- IAM resources
- Compute resources
- Storage resources
- Databases
- Load balancers
- Monitoring and logging
- Resource relationships
- Important configuration details

For each resource, include useful configuration details such as:
- Resource type
- Resource name
- Location
- Purpose
- Important settings
- Dependencies/relationships/connections
- Desired and current capacity/instances

Add a basic architecture diagram explaining all relations and connections between the resources which is well explanatory.

Rules:
- Document only resources present in the Terraform plan.
- Do not invent resources or configuration.
- Include all resources present in the plan.
- Use clear Markdown headings and tables where useful.
- Make the documentation suitable for a technical AWS infrastructure document.

Terraform Plan JSON:

{json.dumps(plan, indent=2)}
"""

    response = completion(
        model=os.environ["LLM_MODEL"],
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content


def main():
    plan = load_plan("terraform-iaac/tf-plan.json")

    documentation = generate_documentation(plan)

    with open("infrastructure.md", "w", encoding="utf-8") as file:
        file.write(documentation)

    print("Infrastructure documentation generated successfully.")


if __name__ == "__main__":
    main()
