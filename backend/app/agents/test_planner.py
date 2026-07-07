from planner_agent import create_plan

queries = [
    "TCS",
    "RELIANCE",
    "INFY"
]

for q in queries:

    print("\n===================")
    print("QUERY:", q)

    result = create_plan(q)

    print(result)