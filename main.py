# A place where all your calenders become one 
# main.py
# This code is for the Google Calendar API, it will allow you to access your calendar and create events
{"installed":{"client_id":"574449305317-vs32pbtp31voa2b1rrk2hdv4dujrmam9.apps.googleusercontent.com","project_id":"project-99ea6f66-1876-4b75-886","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}}
# This is the code for the to do list
import datetime
import os.path
#This is the code for tkinter to make the graphical interface
import tkinter as tk
from tkinter import ttk

# This is the code for the Google Calendar API, it will allow you to access your calendar and create events
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
# If modifying these scopes, delete the file token.json.
def get_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        flow= InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)
# This function will get the events from the calendar and return them as a list
def get_events(service, calender_id):
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId=calender_id, timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    return events_result.get('items', [])
# This function will take the events and create a to do list from them
def make_todo_list(events):
    all_todos = []

    if not events:
        return ["No upcoming events found."]
    for event in events:
        title = event.get('summary', 'No Title')
        
        start = event.get("start",{})
        start_time = start.get("dateTime", start.get("date", "No Date"))


        todo = f"Prepare for {title} at {start_time}"
        all_todos.append({"task":todo,"date":start_time})

    return all_todos
# This function will create a window to display the to do list
def main():
    service = get_calendar_service()
    calendars = {"Personal":"primary"}
    all_todos = []

    for name, cal_id in calendars.items():
        events = get_events(service, cal_id)
        todos = make_todo_list(events)
        all_todos.extend(todos)

        print(f"To-Do List for {name} Calendar:")
        for todo in todos:
            print(f"- {todo}")  
                  
        all_todos.extend(todos)
        show_todo_window(all_todos)
from datetime import datetime
# This function will create a window to display the to do list, it will sort the dates from closest/recent to farthest
def show_todo_window(todos):
# Sort dates from closest/recent to farthest
    todos.sort(key=lambda todo: datetime.fromisoformat(todo["date"]))
    
    window = tk.Tk()
    window.title("To-Do List")
    window.geometry("600x400")

    title = ttk.Label(window, text = "Your To-Do List", font=("Helvetica", 16, "bold"))
    title.pack(pady=10)

    frame = ttk.Frame(window)
    frame.pack(fill= "both", expand=True, padx=20, pady=10)

    for todo in todos:
        checked = tk.BooleanVar()
        checkbox = ttk.Checkbutton(frame, text=todo, variable=checked)
        checkbox.pack(anchor="w", pady=5)

    close_button = ttk.Button(window, text="Close", command=window.destroy)
    close_button.pack(pady=10)

    window.mainloop()

main()
# END MAIN PROGRAM
