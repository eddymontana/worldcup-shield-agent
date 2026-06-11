import os
import json
import pandas as pd
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Import Arize Phoenix dependencies
from phoenix.client import Client
from phoenix.experiments import run_experiment

# 1. Load environment variables
load_dotenv()  

# 2. Initialize Clients
# Explicit key routing prevents system variable collisions
genai_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Phoenix automatically connects to Arize Cloud using PHOENIX_API_KEY from .env
px_client = Client()  

# 3. Define security incidents dataset (Ground Truth)
data = {
    "security_alert": [
        "Brute force SSH attack detected on IP 192.168.1.55 from external IP 203.0.113.5.",
        "High CPU utilization and cryptomining signature detected on Docker container hash c3f92a1.",
        "Unauthorized database access attempt detected from user guest_account on Production DB."
    ],
    "expected_tool": ["block_ip", "isolate_container", "revoke_user_access"],
    "expected_param": ["203.0.113.5", "c3f92a1", "guest_account"]
}

df = pd.DataFrame(data)

# Register the golden dataset with the Arize platform instance
dataset = px_client.datasets.create_dataset(
    name="worldcup_shield_agent_gold_v1",
    dataframe=df,
    input_keys=["security_alert"],
    output_keys=["expected_tool", "expected_param"]
)

# 4. Define the Agent Task using Gemini 2.5 Flash
def security_agent_task(security_alert):
    system_prompt = (
        "You are an automated security shield agent. Analyze the security alert and select "
        "the single most effective tool to mitigate it. Your output must strictly be a JSON object "
        "with 'tool_to_execute' and 'parameter_value'. "
        "Available Tools: block_ip, isolate_container, revoke_user_access, restart_server."
    )
    
    response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=security_alert,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            temperature=0.0
        ),
    )
    
    return response.text

# 5. Define the Custom LLM-as-a-Judge Evaluator using Gemini 2.5 Pro
# Naming arguments 'output' and 'expected' allows Phoenix to map tracking streams natively
def tool_selection_judge(output, expected):
    expected_tool = expected["expected_tool"]
    expected_param = expected["expected_param"]
    
    judge_prompt = f"""
    You are an automated Security Audit Judge. Your job is to verify if an incident response agent
    executed the correct remediation tool and did not hallucinate parameters.

    ---
    GROUND TRUTH POLICY:
    - Expected Tool to Run: {expected_tool}
    - Critical Target Parameter: {expected_param}
    ---
    AGENT EXECUTION OUTPUT PATH:
    {output}
    ---

    CRITERIA:
    1. Did the agent execute the EXACT expected tool?
    2. Did the agent pass the EXACT target parameter value without missing digits, hashes, or altering IPs?

    Output your evaluation strictly in this JSON format:
    {{
       "score": 1,
       "explanation": "A short sentence explaining why it passed or failed."
    }}
    """
    
    response = genai_client.models.generate_content(
        model="gemini-2.5-pro",
        contents=judge_prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.0
        ),
    )
    
    result = json.loads(response.text)
    
    # Return a structured dictionary mapping directly to Phoenix evaluation specs
    return {
        "score": float(result["score"]),
        "label": "PASS" if result["score"] == 1 else "FAIL",
        "explanation": result["explanation"]
    }

# 6. Execute Cloud Experiment Pipeline
if __name__ == "__main__":
    print("🚀 Starting Arize Phoenix Cloud Experiment Pipeline...")
    print("="*60)
    
    experiment = run_experiment(
        dataset=dataset,
        task=security_agent_task,
        evaluators=[tool_selection_judge],
        experiment_name="worldcup-reremediation-accuracy"
    )
    
    print("\n✅ Experiment execution complete!")
    print("🔗 Check your Arize Phoenix Cloud dashboard to view metrics and traces.")