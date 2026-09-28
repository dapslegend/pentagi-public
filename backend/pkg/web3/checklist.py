CHECKLIST = [
    "Confirm chain id on your node",
    "Confirm bytecode present",
    "Match source to bytecode",
    "Map privileged roles and delays",
    "Trace value in and out",
    "Review external calls and reentrancy surfaces",
    "Review upgrade and initializer paths",
    "Write a fork test before claiming a finding",
]


def run() -> dict:
    return {"items": CHECKLIST, "status": "human_review_required"}
