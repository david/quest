"""Write a session log for context.history_file from alternating user and assistant texts."""
import json, sys, uuid

def main(out, *turns):
    session = str(uuid.uuid4())
    parent = None
    with open(out, "w") as f:
        for i, text in enumerate(turns):
            role = "user" if i % 2 == 0 else "assistant"
            me = str(uuid.uuid4())
            entry = {
                "parentUuid": parent, "isSidechain": False, "type": role,
                "uuid": me, "timestamp": f"2026-10-29T09:{i:02d}:00.000Z",
                "userType": "external", "entrypoint": "cli", "cwd": "/home/user/cwd",
                "sessionId": session, "version": "2.1.312",
            }
            if role == "user":
                entry["message"] = {"role": "user", "content": text}
            else:
                entry["message"] = {
                    "model": "claude-opus-5-5", "id": f"msg_{uuid.uuid4().hex[:24]}",
                    "type": "message", "role": "assistant",
                    "content": [{"type": "text", "text": text}],
                    "stop_reason": "end_turn", "stop_sequence": None,
                    "usage": {"input_tokens": 0, "output_tokens": 0},
                }
            f.write(json.dumps(entry) + "\n")
            parent = me

if __name__ == "__main__":
    turns = json.load(open(sys.argv[2]))
    main(sys.argv[1], *turns)
