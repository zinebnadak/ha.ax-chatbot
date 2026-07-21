# run_eval will run RAGAS evaluation on all questions except "out of scope" which will use check_refusal instead

from schema import load_golden_set
from check_refusal import check_out_of_scope


def run_eval(answer_fn, golden_path="data/golden_set/golden_set.json", eval_label="v1-baseline"):
    items = load_golden_set(golden_path)

    standard_question = [i for i in items if i.category != "out_of_scope"]
    out_of_scope_question = [i for i in items if i.category == "out_of_scope"]

    print(f"{len(standard_question)} standard, {len(out_of_scope_question)} out_of_scope")

    ragas_results = []
    refusal_results = []


    for item in standard_question:
        result = answer_fn(item.question)
        #the dict pattern RAGAS expects
        ragas_results.append({
            "question": item.question,
            "answer": result["answer"],
            "contexts": result["contexts"],
            "reference": item.expected_answer,
        })
    
    for item in out_of_scope_question:
        answer = answer_fn(item.question)["answer"] #call the function with the question, then acess the dict key
        refusal_results.append(check_out_of_scope(item, answer))

    return (ragas_results, refusal_results) 

    

'''
returns fake but shaped-correctly output used in the dict for RAGAS, to test the loop above
before v1_adapter exists
'''
def stub_answer_fn(question: str) -> AnswerResult:
    return {
        "answer": "Jag kan tyvärr bara hjälpa till med frågor om Högskolan på Åland och dess utbildningar. För övriga frågor kan du kontakta info@ha.ax.",
        "contexts": ["[STUB CONTEXT 1]", "[STUB CONTEXT 2]"],
    }
        
if __name__ == "__main__":
    ragas_results, refusal_results = run_eval(stub_answer_fn, "data/golden_set/golden_set.json", "stub-test")
    print(f"Collected {len(ragas_results)} RAGAS results, and {len(refusal_results)} out of scope results!")
    print(ragas_results[0])
    print(refusal_results[0])