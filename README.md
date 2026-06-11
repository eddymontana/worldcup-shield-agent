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

<h3>Evaluation Summary</h3>

<table width="100%">
  <thead>
    <tr>
      <th align="center">Incident ID</th>
      <th align="left">Threat Profile</th>
      <th align="left">Selected Mitigation Tool</th>
      <th align="left">Extracted Parameter</th>
      <th align="center">Audit Status</th>
      <th align="center">Evaluation Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center"><b>#1</b></td>
      <td align="left">SSH Brute Force</td>
      <td align="left"><code>block_ip</code></td>
      <td align="left"><code>203.0.113.5</code></td>
      <td align="center">🟢 PASS</td>
      <td align="center"><code>1.0</code></td>
    </tr>
    <tr>
      <td align="center"><b>#2</b></td>
      <td align="left">Cryptomining Activity</td>
      <td align="left"><code>isolate_container</code></td>
      <td align="left"><code>c3f92a1</code></td>
      <td align="center">🟢 PASS</td>
      <td align="center"><code>1.0</code></td>
    </tr>
    <tr>
      <td align="center"><b>#3</b></td>
      <td align="left">Unauthorized Database Hit</td>
      <td align="left"><code>revoke_user_access</code></td>
      <td align="left"><code>guest_account</code></td>
      <td align="center">🟢 PASS</td>
      <td align="center"><code>1.0</code></td>
    </tr>
  </tbody>
</table>
