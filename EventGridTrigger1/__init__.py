import json
import logging
import redis
import requests
import os


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
    eventid = result_obj['id']
    base = result_obj['data']['base']
    exp = result_obj['data']['exp']
    total = result_obj['data']['total']
    run_num = result_obj['data']['runId']
    val = base**exp

    result_data = f"Base: {base}, Exp: {exp}, Total: {total}, Val: {val}, Run: {run_num}"

    logging.warn(f'Python EventGrid trigger processed an event: {result}, result_data: {result_data}')

    # derived from application property
    host = os.environ.get("redishost")
    key = os.environ.get("rediskey")

    r = redis.StrictRedis(host=host, port=6380, db=0, password=key, ssl=True)
    ping_result = r.ping()
    logging.warn("Ping returned : " + str(ping_result))

    record_key = str(run_num) + "-" + str(eventid)
    r.set(record_key, val)    

    # get the keys for this run
    keys = r.keys(str(run_num) + '*')

    if len(keys) == total:
        vals = []
        for reskey in keys:
            val = r.get(reskey)
            vals.append(int(val.decode("utf-8")))
            r.delete(reskey)    
        
        total_result = sum(vals)
        logging.warn("###### TOTAL: " + total_result + " ######")

        # push total to display function
        result_host = os.environ.get("resulthost")
        r = requests.post(result_host + "?run=" + str(run_num) + "&total=" + str(total_result))

        

    




