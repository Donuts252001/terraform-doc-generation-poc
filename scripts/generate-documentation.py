import json
import os
from litellm import completion


def load_plan(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_documentation(changed_resources):
    prompt = f"""
You are an AWS infrastructure documentation expert.

Analyze the Terraform plan JSON below and generate detailed documentation for only the changes to be applied, well-structured Markdown documentation.
Don't involve documentation for the resources which are already created or have no change or action as no-op.

# Include:

# AWS Infrastructure Documentation

- Infrastructure overview
- Documentation by: Terraform
- Generated date: 
- Commit ID: 
# - Environment
# - AWS region
# - VPC and networking
# - Subnets
# - Route tables
# - Internet/NAT gateways
# - Security groups
# - IAM resources
# - Compute resources
# - Storage resources
# - Databases
# - Load balancers
# - Monitoring and logging
# - Resource relationships
# - Important configuration details

For each resource with opearations or changes to be done, include useful configuration details such as:
- Resource type
- Resource name
- Location
- Purpose
- Important settings
- Dependencies/relationships/connections
- Desired and current capacity/instances


Rules:
- Do not hallucinate.
- Document only resources present in the Terraform plan which are have some operation to be done or which have changes.
- Do not invent resources or configuration.
- Do not include resources which have no changes or action as no-op.
# - Include all resources present in the plan.
- Use clear Markdown headings and tables where useful.
- Make the documentation suitable for a technical AWS infrastructure document.

Terraform Plan JSON:

{json.dumps(changed_resources, indent=2)}
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
    changed_resources = plan.get("resource_changes", [])
    print('changed resources:', changed_resources)
    documentation = generate_documentation(changed_resources)

    with open("infrastructure.md", "w", encoding="utf-8") as file:
        file.write(documentation)

    print("Infrastructure documentation generated successfully.")


if __name__ == "__main__":
    main()
