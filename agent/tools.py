from langchain.agents import Tool
from backend.db import get_today_total

def get_tools(goal_ml: int):
    def water_intake_history_tool(_: str) -> str:
        total = get_today_total()
        if total >= goal_ml:
            return f"🎉 You've met your hydration goal of {goal_ml} ml! Total intake: {total} ml."
        else:
            remaining = goal_ml - total
            return f"💧 You've consumed {total} ml today. {remaining} ml to go to reach your goal of {goal_ml} ml."

    def hydration_goal_tool(_: str) -> str:
        return f"Your current hydration goal is {goal_ml} ml per day."

    return [
        Tool(
            name="Water Intake History",
            func=water_intake_history_tool,
            description="Returns today's water intake. Input can be any string."
        ),
        Tool(
            name="Hydration Goal",
            func=hydration_goal_tool,
            description="Returns the daily hydration goal. Input can be any string."
        )
    ]
