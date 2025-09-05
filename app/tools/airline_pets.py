from typing import Dict, Any, List
import json, os

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "airline_policies.jsonl")

def get_policy(airline: str, pet_type: str, question: str | None = None) -> Dict[str, Any]:
    airline_norm = airline.strip().lower()
    pet_norm = pet_type.strip().lower()
    answers: List[Dict[str, Any]] = []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            if rec.get("airline","").lower() == airline_norm and pet_norm in rec.get("pet_types", []):
                answers.append(rec)
    if not answers:
        return {"answer": f"No policy found for {airline} ({pet_type}).", "citations": []}
    # naive: join summaries; include citations (urls or ids)
    snippets = [a.get("summary","") for a in answers]
    cites = [a.get("url") or a.get("id") for a in answers if a.get("url") or a.get("id")]
    answer = " ".join(snippets)
    if question:
        # tiny heuristic: if 'crate' asked, filter by that tag
        if "crate" in question.lower():
            crate = [a.get("summary","") for a in answers if "crate" in a.get("tags", [])]
            if crate:
                answer = " ".join(crate)
    return {"answer": answer, "citations": cites}
