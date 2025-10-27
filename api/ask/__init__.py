import json, os, logging
import azure.functions as func
from . import logic

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        q = (body.get("question") or "").strip()
        if not q:
            return func.HttpResponse(json.dumps({"error":"empty question"}), status_code=400, mimetype="application/json")
        answer, citations = logic.handle_ask(q)
        return func.HttpResponse(json.dumps({"answer":answer,"citations":citations}), mimetype="application/json")
    except Exception as e:
        logging.exception("ask failed")
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, mimetype="application/json")