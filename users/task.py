from celery import shared_task

@shared_task(name="users.tasks.send_late_notification")
def send_late_notification(employee_id):
    print(f"Lateness notification sent for employee {employee_id}.")

