from langflow.load import run_flow_from_json
TWEAKS = {
  "ChatOutput-3jIIu": {},
  "ChatInput-WAg9J": {},
  "AstraDBToolComponent-ON72a": {},
  "Agent-JO80F": {},
  "ParseData-JqM00": {},
  "Prompt-iitf3": {}
}

result = run_flow_from_json(flow="Basic Prompting (1).json",
                            input_value="message",
                            session_id="", # provide a session id if you want to use session state
                            fallback_to_env_vars=True, # False by default
                            tweaks=TWEAKS)

