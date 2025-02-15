[10-Feb-2025] SNS + API Gateway features are added to this project and were directly integrated via AWS Console. 

21-Nov-2024
# **Building a Scalable Event-Driven System with Serverless Architecture**

Note: 
* [AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) was leveraged to interact programatically, with all the AWS services that are used in this project.
* A [custom Python library](https://pypi.org/project/maintenance-utils/)  was created and published to pypi.org. It needs to be installed and imported to be used within the application.
![image](https://github.com/user-attachments/assets/8f0370ec-f678-40b6-ae44-cb7940338706)

## Functional and Non-functional requiremnts:

![image](https://github.com/user-attachments/assets/135e9801-4540-40ae-8b75-e5192e88e952)

## Architecture Design
![test](https://github.com/user-attachments/assets/1d8f5fb4-66fb-44b5-9c64-dba2b00460d4)

Modern applications demand scalability, resilience, and efficiency—qualities that traditional architectures often struggle to provide. Managing infrastructure, handling unpredictable workloads, and ensuring real-time responsiveness can quickly become complex and costly. This is where event-driven architectures and serverless computing shine.

### Why Event-Driven?

Traditional systems rely on synchronous, request-response communication, where services directly call one another. While this model works in some cases, it introduces tight coupling, making it harder to scale and maintain. Event-driven architectures, on the other hand, decouple components, allowing services to communicate through events rather than direct API calls. This increases system flexibility and resilience.

### Why Serverless?

This architecture is entirely serverless, offering benefits such as:
✅ No infrastructure management – No need to provision or scale servers✅ Automatic scaling – Resources scale based on workload demand✅ Pay-per-use pricing – No costs for idle resources✅ High availability & fault tolerance – AWS handles failovers automatically

Instead of worrying about provisioning capacity, I could focus purely on writing application logic.

For this project, I needed a system that could:
* Process events asynchronously while maintaining data integrity
* Scale dynamically without manual intervention
* Handle failures and retries without disrupting workflows
* Optimize cost by eliminating idle compute resources

To achieve this, I built an event-driven workflow using AWS services. The architecture consists of:

* Frontend: Hosted on Amazon S3 for static content delivery
* API Gateway: Acts as the entry point for requests
* AWS Lambda: Processes events and business logic
* DynamoDB: Stores event data and application state
* SQS: Ensures reliable message processing and decouples services
* SNS: Handles real-time notifications and broadcasts events
* Cognito: Manages authentication and user sessions

With this setup, the system becomes fully serverless, eliminating the need to manage servers while ensuring automatic scaling.

### Top Challenges & Solutions

No system is perfect, and I ran into a few roadblocks. Here’s what I encountered and how I solved it:

1. Event Duplication

Some events were processed multiple times, leading to inconsistent data and redundant operations. This was mainly due to retries triggered by transient failures or duplicate event triggers.Solution:
✔ Idempotency checks in AWS Lambda – Implemented idempotency keys by storing processed event IDs in DynamoDB and checking them before executing the same event again.
✔ FIFO SQS Queues – Replaced standard SQS queues with FIFO queues to ensure each message was delivered exactly once and in order.

2. Debugging Distributed Events

Since the system involved multiple AWS services (Lambda, API Gateway, SQS, SNS, DynamoDB), tracking an event’s journey across these components was difficult. Debugging issues required tracing the entire event lifecycle.Solution:
✔ Structured logging in CloudWatch – Standardized logs with a common request ID across all services and used CloudWatch Log Insights for query-based troubleshooting.
✔ Custom logging in Lambda – Added detailed logs with timestamps, event source, and execution context to capture the entire event processing flow.

3. Handling Failures & Retries

Some events failed due to temporary issues (e.g., network failures, API timeouts). Without proper handling, this could lead to data loss or stuck workflows.Solution:
✔ Dead Letter Queues (DLQs) for failed messages – Configured DLQs in SQS to capture failed messages, allowing for later reprocessing.
✔ SNS Retry Policy – Set up SNS with exponential backoff retries, ensuring failed event notifications were retried automatically.

### Key Takeaways

From this project, I learned:

* Decoupling components with SQS improved reliability and reduced interdependencies.
* Event-driven processing enabled real-time, asynchronous execution.
* Proper logging & tracing made debugging distributed workflows easier.
* Automated failure handling reduced manual intervention and improved reliability.

### Final Thoughts

Event-driven architectures powered by serverless computing provide a flexible, scalable, and cost-effective way to build modern applications. By leveraging AWS Lambda, SQS, DynamoDB, and API Gateway, I was able to build a system that is reliable, scalable, and easy to maintain. If I were to improve this further, I’d explore Step Functions for orchestrating more complex workflows and Kinesis for real-time streaming. 

App Screenshots:
![image](https://github.com/user-attachments/assets/ebdca855-4212-42cd-bde4-d5e16094a28e)
![image](https://github.com/user-attachments/assets/f933cb22-356f-4c08-bf97-3ec838ad492e)
![image](https://github.com/user-attachments/assets/a25f4511-6854-4781-9781-069f5a122156)





