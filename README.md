# G2T2 CS301 Project — Pegasus CRM

This project aims to build a CRM Architecture Landscape for a Global Bank, adhering to modern digital principles. The focus is to create a system that is:

- ☁️ Cloud-native
- 📊 Data-centric
- 🤝 Client-focused
- 🔒 Secure
- 🧩 Modular
- 🤖 Automated
- 🌐 Accessible
- 🌱 Sustainable

## Solution Architecture Diagram

<img width="1508" alt="Solution Architecture Diagram" src="./assets/v3NoAZ.drawio.png">

## Screenshots
<img width="1508" alt="Screenshot 1" src="./assets/agent_dashboard.png">
<img width="1508" alt="Screenshot 1" src="./assets/agent_manage_account.png">

## 🚀 Features

### Backend
- **Authentication**: Multi-factor authentication (MFA) with TOTP and user group management (`ROOT_ADMIN`, `ADMINS`, `AGENTS`).
- **Data Management**: CRUD operations for accounts, clients, and transactions.
- **API Endpoints**: Secure RESTful APIs for managing records and user data.

### Frontend
- **Agent Dashboard**: Manage client profiles, view transactions, and create new accounts.
- **Admin Dashboard**: Manage user accounts and oversee system operations.

### Document Upload
- **Secure Uploads**: Supports PDF, PNG, and JPG files up to 10MB.
- **Presigned URLs**: Backend integration for secure file uploads to AWS S3.

## 🛠️ Tech Stack

### Frontend
- **Vue 3**: Modern JavaScript framework for building user interfaces.
- **Vite**: Fast build tool for development and production.

### Backend
- **AWS Amplify**: Backend-as-a-Service for authentication, data, and storage.
- **Flask**: Lightweight Python framework for API development.
- **DynamoDB**: NoSQL database for scalable data storage.
- **AuroraDB**: Relational database for structured data.
- **RDS**: Managed relational database service for high availability.

### Deployment
- **AWS ECS on Fargate**: Serverless container orchestration for running Python-based backend services.
- **AWS Amplify**: Hosting and deployment for frontend and backend integration.
- **CI/CD**: Automated pipelines for building, testing, and deploying the application.

## 🔑 Authentication

- **Multi-Factor Authentication (MFA)**: Enabled with TOTP.
- **User Groups**: 
  - `ROOT_ADMIN`: Same as ADMINS but cannot be deleted.
  - `ADMINS`: Manage admins and agent accounts.
  - `AGENTS`: Manage client profiles and transactions.

## 🛡️ Security

- **Encryption**: All uploads are encrypted and stored securely in compliance with banking regulations.
- **Access Control**: Role-based access control (RBAC) for secure resource management.

## 🤝 Contributors

- **Team G2T2**: Dedicated to delivering a secure and scalable CRM solution.
- Lee Ka Yong
- Jabriel Ho Junwen
- Fermin Lim Jun Xian
- Quek De Wang
- Rainer Tan Wei Hang
- Nicholas Seah Chong Shiun
- Godewyn Goh
