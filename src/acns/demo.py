from acns import CognitiveCore, SQLiteMemoryStore


def main() -> None:
    memory = SQLiteMemoryStore()
    memory.put("welcome", {"text": "ACNS يعمل محليًا"}, memory_type="semantic", source="demo")
    state = CognitiveCore(memory).run("اختبر دورة معرفية محلية", context={"allow_learning": True})
    print(f"status={state.status} task_id={state.task_id} attempts={state.attempts}")
    print(f"cells={','.join(state.results)}")
    memory.close()


if __name__ == "__main__":
    main()
