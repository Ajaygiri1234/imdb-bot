import base64
from typing_extensions import runtime
from robot.libraries.BuiltIn import BuiltIn
import mimetypes
import Constants
from Communicate import RunItem
import Utils

runitem_lib = RunItem(identifier=Utils.get_identifier(),
                      URL=Utils.get_base_url())


def get_attachment(*path):
    attachments = []

    for p in path:
        data = open(p, "rb").read()
        encoded_image = base64.b64encode(data)
        type = mimetypes.guess_type(p)[0]
        decoded_image = f"data:{type};base64," + encoded_image.decode("UTF-8")
        attachments.append(decoded_image)

    return attachments


def get_runitem_notification(
    subject=None,
    data={},
    attachments=None,
):

    notification = {}

    if subject:
        notification["subject"] = subject
    if attachments:
        notification["attachments"] = attachments

    notification["data"] = data

    return notification


def get_runitem(
    started_at,
    status,
    report_data={},
    completed_at=BuiltIn().get_time(),
    notification=None,
    log_text="",
    is_ticket=True,
):

    run_item = {
        "started_at": started_at,
        "completed_at": completed_at,
        "status": status,
        "report_data": report_data,
        "log_text": log_text,
        "is_ticket": is_ticket,
    }

    if notification:
        run_item["notification"] = notification

    return run_item


def post_complete_run_item(
    started_at,
    report_data={},
    completed_at=BuiltIn().get_time(),
    notification=None,
    log_text="",
    is_ticket=True,
):
    run_items = get_runitem(
        started_at,
        status=Constants.COMPLETED,
        report_data=report_data,
        completed_at=completed_at,
        notification=notification,
        log_text=log_text,
        is_ticket=is_ticket,
    )
    Utils.log_to_console(run_items)
    # runitem_lib.create_run_items(run_items)


def post_error_run_item(
    started_at,
    report_data={},
    completed_at=BuiltIn().get_time(),
    notification=None,
    log_text="",
    is_ticket=True,
):
    run_items = get_runitem(
        started_at,
        status=Constants.ERROR,
        report_data=report_data,
        completed_at=completed_at,
        notification=notification,
        log_text=log_text,
        is_ticket=is_ticket,
    )
    Utils.log_to_console(run_items)

    # runitem_lib.create_run_items(run_items)
