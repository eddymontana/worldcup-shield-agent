## 🧪 Evaluation & Automated Auditing

To ensure our autonomous security agent executes correct mitigations without hallucinating parameters, we implemented a custom LLM-as-a-Judge validation loop. The evaluation utilizes a golden dataset of critical security incidents to verify agent decision accuracy against ground-truth policies.

### Evaluation Criteria
1. **Tool Alignment:** Did the agent choose the precise, expected remediation capability?
2. **Parameter Integrity:** Did the agent extract the exact target variable (IP, hash, username) without dropping or altering characters?

### Execution Logs
Below is the verification output from running the validation suite (`src/test_heal_loop.py`):

```text
🚀 Running Local Gemini Experiment for worldcup-shield-agent...
============================================================

[Incident #1] Alert: Brute force SSH attack detected on IP 192.168.1.55 from external IP 203.0.113.5.
🤖 Agent Output: {
  "tool_to_execute": "block_ip",
  "parameter_value": "203.0.113.5"
}
⚖️ Judge Result: PASS (Score: 1.0)
📝 Explanation: The agent executed the correct tool and passed the exact target parameter value.
------------------------------------------------------------

[Incident #2] Alert: High CPU utilization and cryptomining signature detected on Docker container hash c3f92a1.
🤖 Agent Output: {
  "tool_to_execute": "isolate_container",
  "parameter_value": "c3f92a1"
}
⚖️ Judge Result: PASS (Score: 1.0)
📝 Explanation: The agent executed the correct tool 'isolate_container' with the exact target parameter 'c3f92a1'.
------------------------------------------------------------

[Incident #3] Alert: Unauthorized database access attempt detected from user guest_account on Production DB.
🤖 Agent Output: {
  "tool_to_execute": "revoke_user_access",
  "parameter_value": "guest_account"
}
⚖️ Judge Result: PASS (Score: 1.0)
📝 Explanation: The agent executed the correct tool with the exact target parameter.
------------------------------------------------------------

✅ All incident evaluations complete! Local validation successful.

### Evaluation Summary

| Incident ID | Threat Profile | Selected Mitigation Tool | Extracted Parameter | Audit Status | Evaluation Score |
| :---: | :--- | :--- | :--- | :---: | :---: |
| **#1** | SSH Brute Force | `block_ip` | `203.0.113.5` | 🟢 PASS | `1.0` |
| **#2** | Cryptomining Activity | `isolate_container` | `c3f92a1` | 🟢 PASS | `1.0` |
| **#3** | Unauthorized Database Hit | `revoke_user_access` | `guest_account` | 🟢 PASS | `1.0` |
