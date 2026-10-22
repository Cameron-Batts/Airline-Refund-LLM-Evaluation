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

## Offline verification
On October 22, 2026, all eight notebook code cells executed sequentially in a fresh Python namespace with live mode disabled and socket connections blocked. Reconstructed records reproduced 7/13, 10/13 and 10/13 correct, with zero invalid predictions and all three variants failing C13. Ten parser edge checks passed; no network attempt occurred during notebook execution. This checks local scoring and reconstructed records, not original raw responses, model behavior or API compatibility. The separate 12/13 model comparison remains historical only because its per-case records are not bundled. Jupyter-kernel execution and a clean-environment reinstall were not tested.

## Run Offline
```bash
python -m pip install -r requirements-offline.txt
python validation/verify_offline.py
```
The verification script requires no API key or OpenAI SDK. Install `requirements.txt` separately to use JupyterLab or the optional live path. Default `RUN_LIVE=False` makes no API calls. Predictions are reconstructed from original structured error/comparison tables, not untouched API responses. Offline checks reproduce 7/13, 10/13 and 10/13 counts but do not validate model behavior or original formatting.

## Optional Live Run
Set `OPENAI_API_KEY` and a compatible `OPENAI_MODEL` locally, then enable `RUN_LIVE`. This sends three synthetic prompts via Chat Completions and can incur charges. No key or model default is embedded. Historical model availability is not guaranteed. The corrected live API path is a changed, unexecuted experiment; no paid calls were made during preparation.

## Files
- `notebooks/airline_refund_llm_evaluation.ipynb`: offline/live experiment.
- `data/synthetic_cases.csv`: fictional cases and reference labels.
- `reports/reconstructed_predictions.csv`: reconstructed structured predictions.
- `reports/original_summary.csv`: historical metrics, including separate model test.
- `reports/airline_refund_llm_evaluation.html`: analysis report.
- [Offline verification script](validation/verify_offline.py): blocks network access, executes code cells and checks scores and parsing.
- [Validation record](reports/offline_validation.json): versions, input hashes and scope.
- [Verified offline summary](reports/offline_verified_summary.csv) and [predictions](reports/offline_verified_predictions.csv).
- `requirements-offline.txt`: pinned direct offline dependencies.
- `requirements.txt`: notebook editor and optional live dependencies.
- `portfolio_card.html`: matching portfolio card.

## Limitations
One small synthetic set and single runs do not establish production accuracy, security or model superiority. Exact raw-response fidelity is not established. Repeat runs on unseen cases, audit provider/model configuration, and validate any injection defense before operational use. This project never issues refunds or sends real customer details.

API reference: https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create . Historical model reference: https://developers.openai.com/api/docs/models/gpt-3.5-turbo .

Portfolio: https://cameron-batts.github.io  
GitHub: https://github.com/Cameron-Batts
