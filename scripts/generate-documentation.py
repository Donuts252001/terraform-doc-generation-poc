import json
import os
from datetime import datetime, timezone
from litellm import completion


def load_plan(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def load_existing_documentation(path): 
    if os.path.exists(path): 
        with open(path, "r", encoding="utf-8") as file: 
            return file.read() 
    return ""


def generate_documentation(changed_resources, existing_documentation):
    generated_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    commit_id = os.environ.get("GITHUB_SHA", "Unknown")[:7]
    
    prompt = f"""
You are an AWS infrastructure documentation expert.

Update the EXISTING AWS infrastructure documentation if it exists using ONLY the Terraform resources that have changes or operations in the Terraform plan below.

Analyze the Terraform plan JSON below and generate detailed documentation for only the changes to be applied, well-structured Markdown documentation.
Don't involve documentation for the resources which are already created or have no change or action as no-op. Do not update documentation for the resources that have no changes.

# Include:

# AWS Infrastructure Documentation

- Infrastructure overview
- Documentation by: Terraform
- Generated date: {generated_date}
- Commit ID: {commit_id}
- Environment
- AWS region

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
- Preserve all existing documentation for resources that are not changed.
- Update only the sections corresponding to changed resources.
- Add documentation for newly created resources. 
- Update documentation for modified resources. 
- Remove documentation for deleted resources.
- Do not invent resources or configuration.
- Make the documentation suitable for a technical AWS infrastructure document.

# EXISTING DOCUMENTATION:
 {existing_documentation}

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
    existing_documentation = load_existing_documentation( "infrastructure.md" )
    documentation = generate_documentation(changed_resources,existing_documentation)

    with open("infrastructure.md", "w", encoding="utf-8") as file:
        file.write(documentation)

    print("Infrastructure documentation generated successfully.")


if __name__ == "__main__":
    main()
