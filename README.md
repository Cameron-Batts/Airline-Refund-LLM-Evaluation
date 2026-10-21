# Airline Refund Decisions: LLM Prompt Evaluation

**Portfolio adaptation:** Cameron Batts  
**Source context:** Adapted instructional demonstration; original authorship and individual contributions were not established by the supplied notebook.

## Business Problem
Evaluate whether an LLM follows a fictional private refund policy, produces usable outputs, and resists an instruction embedded in customer text. This is a synthetic routing experiment, not airline law or a refund-processing service.

## Approach
- Evaluate 13 synthetic cases with REFUND, CREDIT, ESCALATE and DENY labels.
- Compare minimal, policy, and policy-plus-examples prompts.
- Separate tolerant parsing, strict-format checks, accuracy and injection behavior.
- Preserve an offline evidence mode and make paid live API calls opt-in.

## Historical Results
| Recorded model | Prompt | Correct | Accuracy |
|---|---|---:|---:|
| gpt-3.5-turbo | Minimal | 7/13 | 53.8% |
| gpt-3.5-turbo | Policy | 10/13 | 76.9% |
| gpt-3.5-turbo | Policy + examples | 10/13 | 76.9% |
| gpt-4o-mini | Policy + examples | 12/13 | 92.3% |

All configurations failed the injected case in the saved tables. Results are unverified historical notebook evidence. The original setup pairs gpt-3.5-turbo with Responses API code; that model/API pairing must be corrected before reproduction. Do not infer that the saved configuration works from its saved output.

## Run Offline
```bash
python -m pip install -r requirements.txt
jupyter lab notebooks/airline_refund_llm_evaluation.ipynb
```
Default `RUN_LIVE=False` makes no API calls. Predictions are reconstructed from original structured error/comparison tables, not untouched API responses. Offline checks reproduce 7/13, 10/13 and 10/13 counts but do not validate model behavior or original formatting.

## Optional Live Run
Set `OPENAI_API_KEY` and a compatible `OPENAI_MODEL` locally, then enable `RUN_LIVE`. This sends three synthetic prompts via Chat Completions and can incur charges. No key or model default is embedded. Historical model availability is not guaranteed. The corrected live API path is a changed, unexecuted experiment; no paid calls were made during preparation.

## Files
- `notebooks/airline_refund_llm_evaluation.ipynb`: offline/live experiment.
- `data/synthetic_cases.csv`: fictional cases and reference labels.
- `reports/reconstructed_predictions.csv`: reconstructed structured predictions.
- `reports/original_summary.csv`: historical metrics, including separate model test.
- `reports/airline_refund_llm_evaluation.html`: analysis report.
- `requirements.txt`: dependencies.
- `portfolio_card.html`: matching portfolio card.

## Limitations
One small synthetic set and single runs do not establish production accuracy, security or model superiority. Exact raw-response fidelity is not established. Repeat runs on unseen cases, audit provider/model configuration, and validate any injection defense before operational use. This project never issues refunds or sends real customer details.

API reference: https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create . Historical model reference: https://developers.openai.com/api/docs/models/gpt-3.5-turbo .

Portfolio: https://cameron-batts.github.io  
GitHub: https://github.com/Cameron-Batts
