# 📜 Project Overview: Transaction Processing Backend (Flask + AWS)

This feature is a Flask-based microservice designed to process transactions done on client profiles and accounts,  store in database, and notifying of clients through email, fully integrated with AWS services like SQS, SES, and DynamoDB.

It powers key backend workflows for activities such as client onboarding, account updates, and secure notification delivery.

---

# ✨ Core Purpose:

- **Manage transaction records** securely in DynamoDB upon a transaction of an agent on a client.
- **Send personalized email notifications** through AWS SES for important events like account creation, updates, or deletions.
- **Integrate with SQS** for scalable, event-driven processing of queued actions.
- **Support automation** with serverless triggers (e.g., AWS Lambda + EventBridge scheduled calls).

This system ensures all client activities are logged, traceable, and clients are promptly informed through secure emails.

---

# 📚 Summary of Available Endpoints:

| Endpoint | Purpose |
| `/records` (POST) | Insert a **new transaction record** (e.g., a client creation or account update) into DynamoDB. |
| `/records` (GET) | Fetch **all transaction records**. Useful for viewing a full activity log. |
| `/records/{agentID}` (GET) | Retrieve all activities handled by a specific agent. Useful for tracking agent performance or activity history, used for the Agent Dashboard UI. |
| `/records/{transactionID}` (PUT) | Update details of an **existing transaction**. Enables correction of typos, metadata updates, etc. |
| `/records/{transactionID}` (DELETE) | Permanently delete a specific transaction by its ID. Supports data cleanup and correction processes. |
| `/process` (GET) | Core processing endpoint: Pulls messages from SQS. Records the transactions into DynamoDB. Sends corresponding emails to clients (only for Create/Update/Delete actions). Deletes messages from the queue after processing. |

---

# 🧐 How the Workflow Ties Together:

1. **Agent triggers an action** (e.g., Create Client, Update Account).
2. **The system publishes a message** into AWS SQS (queueing the action details).
3. **The Flask service's `/process` endpoint** (triggered manually or automatically) pulls the message from SQS.
4. **The service saves** the action into DynamoDB for permanent record.
5. **If applicable**, the service sends a **notification email** to the client using SES.
6. **The SQS message is deleted** after successful processing to ensure no duplicate work.

---

# 🛡️ Important Design Features:

- ✅ **Long polling** from SQS for efficiency.
- ✅ **Idempotent processing** — safe to re-trigger `/process` without causing duplicates.
- ✅ **Transactional logic** — emails are only sent for real transaction changes (not for reads).
- ✅ **Secure and flexible** — designed to work with authenticated API Gateway access (Cognito JWT tokens).
- ✅ **Cloud-native** — built for serverless/elastic architectures on AWS.

---

# 📬 Email Notification Behavior:

| Action Type | Behavior |
| Create | Sends a "Welcome" or "Account Created" email to the client. |
| Update | Sends a notification showing what was updated (before vs after values). |
| Delete | Sends a message informing the client their account/profile has been deleted. |
| Read | No email sent (purely read/logging action). |

---

# 🔥 Why It's Designed This Way:

- **SQS decoupling** allows handling spikes in client activity without overloading backend services.
- **DynamoDB storage** ensures every transaction is permanently stored and can be audited later.
- **Email notifications** keep clients informed instantly, enhancing trust and transparency.
- **Flexible microservice** architecture allows easy scaling and updates independently of other systems.

---

# ✨ Future Upgrades (Ideas):

- Adding retry queues for failed email sends.
- Integrating Slack or SMS notifications alongside email.
- Auto-archiving old transactions after X months to cheaper storage (e.g., S3).

---

# 🚀 Summary in 1 Line:

- A resilient, serverless backend that processes client activities, stores them securely, and automatically communicates key updates to clients — all fully powered by AWS.

---

