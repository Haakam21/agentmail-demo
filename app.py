from agents import Agent, Runner
from flask import Flask, request
from agentmail import AgentMail, Message

client = AgentMail()

inbox = client.inboxes.create(
    username="demo",
    domain="agentmail.to",
    client_id="demo-inbox",
)

webhook = client.webhooks.create(
    url="https://agentmail.onrender.com/chat",
    inbox_ids=[inbox.inbox_id],
    event_types=["message.received"],
    client_id="demo-webhook",
)

agent = Agent(
    name="Email Agent",
    instructions="You are an email agent named AgentMail. Respond as if you are writing an email. Do not include the subject, only the body.",
)

app = Flask(__name__)


@app.post("/chat")
def chat():
    message = Message(**request.json["message"])
    result = Runner.run_sync(agent, message.model_dump_json())

    client.inboxes.messages.reply(
        inbox_id=message.inbox_id,
        message_id=message.message_id,
        text=result.final_output,
    )

    return result.final_output
