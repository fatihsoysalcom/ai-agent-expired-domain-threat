import urllib.request
import json
import ssl

# WARNING: Disabling SSL certificate verification for simplicity in this example.
# In a real-world scenario, you should ALWAYS verify SSL certificates.
# This is done here to avoid potential certificate issues with various public domains
# and focus on the expired domain concept. For actual production AI agents,
# robust certificate validation is absolutely crucial.
ssl._create_default_https_context = ssl._create_unverified_context

def fetch_config(url: str, agent_name: str):
    """
    Simulates an AI agent fetching configuration from a given URL.
    """
    print(f"\n--- {agent_name} attempting to fetch configuration from: {url} ---")
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = response.read().decode('utf-8')
            status_code = response.getcode()
            print(f"[{agent_name}] Received status code: {status_code}")

            if status_code == 200:
                try:
                    config = json.loads(data)
                    print(f"[{agent_name}] Successfully parsed configuration:")
                    # In a real AI agent, this config might contain API keys,
                    # instructions, or URLs for further actions.
                    print(json.dumps(config, indent=2))
                    print(f"[{agent_name}] Configuration loaded. Agent is ready to operate based on this config.")
                    # --- ARTICLE'S CONCEPT ILLUSTRATION ---
                    # If this domain were expired and re-registered by an attacker,
                    # the agent would still fetch and process this potentially malicious config.
                    # This could lead to:
                    # 1. Data leakage (e.g., sending internal data to attacker's server)
                    # 2. Malicious instructions (e.g., performing unwanted actions)
                    # 3. Loading compromised models or data.
                except json.JSONDecodeError:
                    print(f"[{agent_name}] Error: Could not parse JSON from response. Content might be unexpected or malicious.")
                    print(f"[{agent_name}] Raw content snippet (first 200 chars): {data[:200]}...")
            else:
                print(f"[{agent_name}] Warning: Received non-200 status code. Configuration might be unavailable or compromised.")

    except urllib.error.URLError as e:
        print(f"[{agent_name}] Network Error: Could not reach {url}. Reason: {e.reason}")
        print(f"[{agent_name}] This could happen if the domain expired and is now unreachable, or points to a server that's down.")
    except Exception as e:
        print(f"[{agent_name}] An unexpected error occurred: {e}")

if __name__ == "__main__":
    # --- Scenario 1: AI Agent fetches config from a trusted, active domain ---
    # This simulates a normal operation where the agent gets its instructions/data.
    trusted_config_url = "https://httpbin.org/json"
    fetch_config(trusted_config_url, "Trusted AI Agent")

    print("\n" + "="*80)
    print("--- SIMULATING EXPIRED DOMAIN THREAT ---")
    print("Imagine 'https://example.com' was originally a trusted config source for your AI agent.")
    print("It expired, was re-registered by an attacker, and now serves unexpected/malicious content.")
    print("The AI agent, still configured to use this URL, will blindly attempt to fetch from it.")
    print("This demonstrates the risk of processing unexpected content (e.g., HTML instead of JSON).")
    print("="*80)

    # --- Scenario 2: AI Agent fetches config from a hypothetically expired and re-registered domain ---
    # This URL (example.com) typically returns HTML, not JSON. This simulates an attacker
    # re-registering an expired domain and serving unexpected content, which the AI agent
    # might blindly attempt to parse, leading to errors or worse, execution of malicious code.
    compromised_config_url = "https://example.com"
    fetch_config(compromised_config_url, "Vulnerable AI Agent")

    print("\n--- Mitigation Notes ---")
    print("To prevent this, AI agents and systems should:")
    print("1. Implement strict content validation (e.g., expect specific JSON schema, content-type headers).")
    print("2. Use domain monitoring tools to detect upcoming expirations of critical dependencies.")
    print("3. Pin certificates or use DNSSEC for critical endpoints to prevent domain hijacking.")
    print("4. Regularly audit and update external dependencies and their configurations.")
