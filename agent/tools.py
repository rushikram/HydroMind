from langchain.agents import Tool
from backend.db import get_today_total

def get_tools(goal_ml: int, user_id: str):
    # Tool to report today’s water intake
    def water_intake_history_tool(_: str) -> str:
        try:
            total = get_today_total(user_id)
            if total >= goal_ml:
                return f"🎉 You've met your hydration goal of {goal_ml} ml! Total intake: {total} ml."
            else:
                remaining = goal_ml - total
                return f"💧 You've consumed {total} ml today. {remaining} ml left to reach your goal of {goal_ml} ml."
        except Exception as e:
            return f"⚠️ Error retrieving water intake: {str(e)}"

    # Tool to report goal
    def hydration_goal_tool(_: str) -> str:
        return f"📌 Your current hydration goal is {goal_ml} ml per day."

    return [
        Tool.from_function(
            name="Water Intake History",
            func=water_intake_history_tool,
            description="Returns today's water intake. Input can be any string."
        ),
        Tool.from_function(
            name="Hydration Goal",
            func=hydration_goal_tool,
            description="Returns the daily hydration goal. Input can be any string."
        )
    ]
