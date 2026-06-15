from celery import shared_task

import time


@shared_task
def send_email():
    for x in range(10):
        time.sleep(1)
        # send email
        print(f"Sending email {x}")