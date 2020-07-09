import json
import logging

import azure.functions as func


def main(event: func.EventGridEvent):
    result = json.dumps({
        'id': event.id,
        'data': event.get_json(),
        'topic': event.topic,
        'subject': event.subject,
        'event_type': event.event_type,
    })

    result_obj = json.loads(result)
    base = result_obj['data']['base']
    exp = result_obj['data']['exp']
    total = result_obj['data']['total']
    run_num = result_obj['data']['runId']
    val = base**exp

    result_data = f"Base: {base}, Exp: {exp}, Total: {total}, Val: {val}, Run: {run_num}"

    logging.info(f'Python EventGrid trigger processed an event: {result}, result_data: {result_data}')
