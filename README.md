[10-Feb-2025] SNS + API Gateway features are added to this project and were directly integrated via AWS Console. 

21-Nov-2024
# **Building a Scalable Event-Driven System with Serverless Architecture**

Note: [AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) was leveraged to interact programatically, with all the AWS services that are used in this project.  

Functional and Non-functional requiremnts:

![image](https://github.com/user-attachments/assets/135e9801-4540-40ae-8b75-e5192e88e952)

A [custom Python library](https://pypi.org/project/maintenance-utils/)  was created and published to pypi.org. It needs to be installed and imported to be used within the application.
Library URL:   
![image](https://github.com/user-attachments/assets/8f0370ec-f678-40b6-ae44-cb7940338706)

Architecture Design
![test](https://github.com/user-attachments/assets/1d8f5fb4-66fb-44b5-9c64-dba2b00460d4)

App Screenshots:
![image](https://github.com/user-attachments/assets/ebdca855-4212-42cd-bde4-d5e16094a28e)
![image](https://github.com/user-attachments/assets/f933cb22-356f-4c08-bf97-3ec838ad492e)
![image](https://github.com/user-attachments/assets/a25f4511-6854-4781-9781-069f5a122156)

Vehicle Service Tracker, a web-based application is designed to assist users in managing and tracking the maintenance of their vehicles. The application provides a user-friendly interface that allows individuals to record and monitor essential vehicle data such as make, model, mileage,
maintenance history, and upcoming service schedule. Users can also generate maintenance reports and receive real-time notifications via email. The backend of the application uses Amazon Web Services (AWS) to ensure scalability, reliability, and security. AWS Cognito is utilized for user authentication, enabling secure login and account management with support for registration and password resets. The service leverages Amazon Simple Storage Service (S3) for
storing and retrieving maintenance reports. Amazon DynamoDB is used as the database for storing vehicle and service information. AWS Simple Queue Service (SQS) and Lambda are integrated to create an event-driven architecture, where Lambda function process incoming messages and trigger automated actions, such as generating and storing maintenance reports. The frontend of the application is built with React, offering a responsive and intuitive interface for users to interact with the vehicle records, service history, and other essential information. The application incorporates authentication flows, data validation, and dynamic report generation, making it an effective tool for vehicle owners. A custom Python library is incorporated that provides functionalities such as calculating upcoming maintenance schedules and generating maintenance reports. This library simplifies the backend workflows. Overall, the application aims to streamline vehicle maintenance tracking by offering users a centralized platform to monitor service schedules, and access reports on the maintenance status of their vehicles. 

CONCLUSION: Working on creating the initial prototype of Vehicle Service Scheduler application was an immense learning about how to build cloud based applications, and using some of the fundamental AWS cloud services. Specifically, use of SQS and Lambda together to create event driven architecture which is important to not only respond to changes in real time but also resources are used only when needed which saves up costs. Use of DynamoDB and S3 services provides insights into how data storage and retrieval works in the cloud environment. Organizing project components with each component having its own file, enhanced maintainability and reusability. Use of error logging and CloudWatch logs helped immensely throughout the project to debug the development issues. Setup
of Jenkins pipeline provides an easy way for server to pick up new changes to the code without any manual intervention. It is starting to make sense why applications have to have a scalable, highly available and low-latency architecture and more importantly as a developer it is thrilling to address these
requirements in the application with the use of cloud services. While there were some challenges that are already highlighted in the document above, overall the use of cloud services seems to be beneficial for today’s software applications due to ondemand nature of cloud services, pay as you go model, scalability, elasticity and the global infrastructure. While the learning curve can be a challenge for the beginners with no to less experience with cloud services, integrating services and designing complex architectures can become increasingly enjoyable and rewarding as one gains experience. Looking at the project retrospectively, I would improve security of the application by using REST APIs (with the help of API Gateway) instead of direct APIs in backend. I would also add elements of monitoring (CloudWatch) to measure load and performance metrics. I would setup SNS for sending reminders to users about upcoming service to enhance the user experience. I would use auto scaling, and host my code on at least two EC2 instances in two separate Availability Zones for
availability and scalability. Use of AWS Elastic Beanstalk for deployment and AWS Code Deploy for CI/CD, as I expect this setup to work seamlessly with AWS architecture, unlike Jenkins with configuration overhead. I could also potentially use DynamoDB streams to trigger Lambda function directly without the use of SQS to avoid code complexity. SQS would be more beneficial to use when application grows in user base and sees high traffic loads as it provides message buffering and retry functionalities.




