import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import ToolContext

MODEL = LiteLlm(
    model=os.getenv("ADK_MODEL", "groq/qwen/qwen3.8-27b"),
    max_tokens=300,
    num_retries=5,
)

# Fake college timetable from the notebook
TIMETABLE = {
    "monday": [
        "09:00 Python Programming",
        "11:00 Engineering Maths",
        "14:00 Digital Logic Lab",
    ],
    "tuesday": [
        "09:00 Physics",
        "11:00 Python Programming",
        "14:00 Communication Skills",
    ],
    "wednesday": [
        "09:00 Engineering Maths",
        "11:00 Data Structures",
        "14:00 Sports",
    ],
    "thursday": [
        "09:00 Data Structures",
        "11:00 Physics Lab",
        "14:00 Library Hour",
    ],
    "friday": [
        "09:00 AI Club Workshop",
        "11:00 Engineering Maths",
        "14:00 Mentor Meeting",
    ],
}

CANTEEN_MENU = {
    "monday": "Idli, Sambar, Lemon Rice",
    "tuesday": "Poori, Aloo Curry, Curd Rice",
    "wednesday": "Dosa, Chutney, Veg Biryani",
    "thursday": "Upma, Rajma Chawal, Buttermilk",
    "friday": "Pongal, Chicken Biryani, Gulab Jamun",
}
def get_timetable(day: str) -> dict:
    """Returns the class timetable for a given weekday.

    Args:
        day: Full weekday name, for example "Monday".
    """
    classes = TIMETABLE.get(day.strip().lower())

    if not classes:
        return {
            "status": "error",
            "message": f"No classes found for '{day}'. Try Monday to Friday.",
        }

    return {
        "status": "success",
        "day": day.title(),
        "classes": classes,
    }
def get_canteen_menu(day: str) -> dict:
    """Returns the canteen menu for a given weekday.

    Args:
        day: Full weekday name, for example "Friday".
    """
    menu = CANTEEN_MENU.get(day.strip().lower())

    if not menu:
        return {
            "status": "error",
            "message": f"Canteen is closed on '{day}'.",
        }

    return {
        "status": "success",
        "day": day.title(),
        "menu": menu,
    }
def calculate_cgpa(grade_points: list[float], credits: list[int]) -> dict:
    """Calculates the CGPA (credit-weighted average of grade points).

    Args:
        grade_points: Grade point of each subject, for example [9, 8, 10].
        credits: Credits of each subject, in the same order, for example [4, 3, 3].
    """
    if len(grade_points) != len(credits) or not credits:
        return {
            "status": "error",
            "message": "Give one credit value for every grade point.",
        }

    total = sum(g * c for g, c in zip(grade_points, credits))
    cgpa = round(total / sum(credits), 2)

    return {
        "status": "success",
        "cgpa": cgpa,
    }
def add_reminder(task: str, tool_context: ToolContext) -> dict:
    """Saves a reminder for the student so it can be recalled later in the conversation.

    Args:
        task: What the student wants to be reminded about.
    """
    reminders = tool_context.state.get("reminders", [])
    reminders.append(task)
    tool_context.state["reminders"] = reminders

    return {
        "status": "success",
        "saved": task,
        "total_reminders": len(reminders),
    }

def list_reminders(tool_context: ToolContext) -> dict:
    """Lists all reminders the student has saved in this session."""
    return {
        "status": "success",
        "reminders": tool_context.state.get("reminders", []),
    }


root_agent = Agent(
    name="campus_buddy",
    model=MODEL,
    description="A friendly campus assistant for college students.",
    instruction="""
You are Campus Buddy, a helpful assistant for college students.

Use the appropriate tool for each request:
- Use get_timetable for class schedule questions.
- Use get_canteen_menu for canteen menu questions.
- Use calculate_cgpa for CGPA calculations.
- Use add_reminder when students want to save a reminder.
- Use list_reminders when students ask to see their saved reminders.

For calculations, report the result returned by the tool.
For reminders, confirm when a reminder is saved.
Answer clearly and concisely.
""",
    tools=[
        get_timetable,
        get_canteen_menu,
        calculate_cgpa,
        add_reminder,
        list_reminders,
    ],
)

