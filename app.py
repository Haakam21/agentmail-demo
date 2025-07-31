from agents import Agent, Runner
from flask import Flask, request

agent = Agent(
    name="Email Agent",
    instructions="You are an email agent named AgentMail. Respond as if you are writing an email. Do not include the subject, only the body.",
)

app = Flask(__name__)


@app.post("/chat")
def chat():
    result = Runner.run_sync(agent, request.json["message"])

    return result.final_output
