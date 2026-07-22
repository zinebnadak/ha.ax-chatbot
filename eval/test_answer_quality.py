# DeepEval 
# Run command (change results file name): DEEPEVAL_RESULTS_FOLDER=eval/eval_results/<label> uv run deepeval test run test_answer_quality.py

from schema import load_golden_set
from bot_adapter import answer

import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase 
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, ContextualRecallMetric, ContextualPrecisionMetric

JUDGE_MODEL = "gpt-4o-mini"

items = [item for item in load_golden_set("data/golden_set/golden_set.json") if item.category != "out_of_scope"]

@pytest.mark.parametrize("item", items, ids=lambda i:i.question[:40]) # pulls the first 40 characters of that item's .question field, and uses it as the label. A lambda function can take any number of arguments, but can only have one expression
def test_answer_quality(item): # @ calls this function one per item
    response = answer(item.question) #returns answer, retrieval_context

    test_case = LLMTestCase(
        input=item.question,
        expected_output=item.expected_answer,
        actual_output=response.answer,
        context=[item.expected_answer], #
        retrieval_context=response.retrieval_context,
    )

    answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.7, model=JUDGE_MODEL, include_reason=True)
    faithfulness_metric = FaithfulnessMetric(threshold=0.7, model=JUDGE_MODEL, include_reason=True)
    contextual_recall_metric = ContextualRecallMetric(threshold=0.7, model=JUDGE_MODEL, include_reason=True)
    contextual_precision_metric = ContextualPrecisionMetric(threshold=0.7, model=JUDGE_MODEL, include_reason=True)

    #using 4/4 metrics (no G-eval) for scoring content correctness 
    assert_test(test_case, [
        faithfulness_metric,        #the answer grounded in what was retrieved
        answer_relevancy_metric,    #the answer actually addresses the question
        contextual_recall_metric,   #does the retrieved context, collectively, contain everything needed to produce the expected answer? Completeness-sensitive.
        contextual_precision_metric #of the retrieved chunks, are the relevant ones ranked near the top? Order-sensitive.
    ])
