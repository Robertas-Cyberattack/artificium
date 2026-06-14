# Artificium

## Table of Contents

- [Introduction](#introduction)
- [Project Goals](#project-goals)
- [User Stories](#user-stories)
- [Database Design](#database-design)
- [Entity Relationship Diagram](#entity-relationship-diagram)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Automated Testing](#automated-testing)
- [Deployment](#deployment)
- [Stripe Integration](#stripe-integration)
- [Security](#security)
- [Future Improvements](#future-improvements)
- [Credits](#credits)

---

## Introduction

Artificium is a Full Stack Django web application developed for engineering and construction support services.

The platform allows clients to:

- Register and manage accounts.

  Related screenshots:

  - [Register for an Artificium account](screenshots/register_for_an_Artificium_account.png)
  - [Client dashboard](screenshots/client_dashboard.png)
  - [Admin dashboard](screenshots/admin_dashboard.png)


- Submit project requests

  Related screenshot:

  - [Request a quote](screenshots/request_a_quote.png)


- Upload project files

  Related screenshot:

  - [Request a quote](screenshots/request_a_quote.png)

- Communicate with administrators
- Make secure online payments using Stripe
- Download PDF invoices
- Track project progress

Administrators can:

- Manage clients
- Manage projects
- Upload and manage project files
- Communicate with clients
- Generate invoices
- Monitor project status

The application was developed as Milestone Project 4 for the Level 5 Diploma in Web Application Development.

---

## Project Goals

The purpose of Artificium is to provide a professional engineering project management platform where clients and administrators can communicate efficiently throughout a project's lifecycle.

### Client Goals

- Create project requests
- Upload project files
- Track project progress
- Send and receive messages
- Download invoices
- Make secure payments

### Administrator Goals

- Manage clients
- Manage projects
- Update project status
- Manage files
- Communicate with clients
- Generate invoices

---

## User Stories

### Client

- As a client, I want to register an account so that I can access the system.
- As a client, I want to log in securely.
- As a client, I want to create project requests.
- As a client, I want to upload project files.
- As a client, I want to edit my project before it is quoted.
- As a client, I want to delete my project before it is quoted.
- As a client, I want to communicate with administrators.
- As a client, I want to download invoices.
- As a client, I want to make online payments.
- As a client, I want to track project progress.

### Administrator

- As an administrator, I want to manage clients.
- As an administrator, I want to create projects.
- As an administrator, I want to update project information.
- As an administrator, I want to upload files.
- As an administrator, I want to communicate with clients.
- As an administrator, I want to manage invoices.
- As an administrator, I want to monitor project progress.

---

## Database Design

The application uses a relational database managed by Django ORM.

### User

The built-in Django User model is used for authentication and account management.

Fields include:

- username
- email
- password
- is_staff
- is_active

---

### ClientProject

Stores project information submitted by clients.

| Field | Description |
|---------|-------------|
| client | Linked Django User |
| title | Project title |
| description | Project description |
| price | Project value |
| invoice_number | Invoice reference |
| is_paid | Payment status |
| status | Current project status |
| progress | Project progress percentage |
| admin_notes | Internal notes |
| client_notes | Client notes |
| due_date | Target completion date |
| created_at | Creation date |
| updated_at | Last update |

---

### ProjectMessage

Stores messages between clients and administrators.

| Field | Description |
|---------|-------------|
| project | Related project |
| sender | Message sender |
| message | Message content |
| is_admin_message | Admin/client flag |
| is_read_by_admin | Read status |
| is_read_by_client | Read status |
| created_at | Message date |

---

### ProjectFile

Stores uploaded project files.

| Field | Description |
|---------|-------------|
| project | Related project |
| title | File title |
| file | Uploaded file |
| uploaded_by | User who uploaded |
| visible_to_client | Visibility flag |
| uploaded_at | Upload date |

---

### Invoice

Stores generated invoices.

| Field | Description |
|---------|-------------|
| client | Related client |
| project | Related project |
| invoice_number | Invoice reference |
| amount | Invoice amount |
| description | Invoice description |
| status | Invoice status |
| due_date | Due date |
| pdf_file | Generated PDF |
| created_at | Creation date |

---

## Entity Relationship Diagram

```text
User
│
├── ClientProject
│      │
│      ├── ProjectMessage
│      ├── ProjectFile
│      └── Invoice
```

An ER Diagram image is included within the project documentation.

---

## Features

### Authentication

The application uses Django Allauth for secure authentication.

Features include:

- User registration
- User login
- User logout
- Password management
- Session management

---

### Client Dashboard

Clients have access to a dedicated dashboard where they can:

- Create projects
- Edit projects
- Delete projects
- View project status
- View project progress
- Upload files
- Download files
- Delete files
- Send messages
- Receive messages
- Download invoices
- Make payments

---

### Admin Dashboard

Administrators have access to additional functionality:

- Manage all clients
- Manage all projects
- Manage messages
- Manage files
- Update project progress
- Update project status
- Generate invoices
- Monitor payments

---

### Project Management

The system provides full CRUD functionality.

#### Create

Clients and administrators can create projects.

#### Read

Projects can be viewed from dashboards.

#### Update

Projects can be edited before quotation and payment.

#### Delete

Projects can be deleted before quotation and payment.

---

### Messaging System

The application includes a built-in messaging system.

Features:

- Client to administrator communication
- Administrator to client communication
- Read status tracking
- Message editing
- Message deletion
- Notification badges

---

### File Management

Clients can upload project files directly from the dashboard.

Supported functionality:

- Upload files
- Download files
- Open files
- Delete files
- Store files against projects

Examples:

- PDF drawings
- DWG files
- Images
- ZIP files
- Engineering calculations

---

### Payment System

Stripe Checkout has been integrated.

Features include:

- Secure payment processing
- Card payments
- Payment confirmation
- Project payment tracking

---

### Invoice System

Invoices are automatically generated.

Features:

- PDF generation
- Invoice numbering
- Invoice download
- Invoice storage
- Invoice history

---

### Search Functionality

JavaScript search functionality allows users to quickly locate projects.

Users can search by:

- Project title
- Status
- Invoice number
- Messages

Search results update instantly without refreshing the page.

---

## Technologies Used


### Programming Languages

- Python
- HTML5
- CSS3
- JavaScript

---

### Frameworks

- Django 3.2

---

### Frontend Libraries

- Bootstrap 4
- Font Awesome
- jQuery

---

### Authentication

- Django Allauth

---

### Database

- SQLite

---

### Payment Processing

- Stripe Checkout

---

### PDF Generation

- ReportLab

---

### Development Tools

- Git
- GitHub
- Visual Studio Code

---

### Deployment

- Heroku

---


## Project Structure

The application was developed using a modular Django architecture.

The project consists of the following Django applications:

- home
- projects
- payments

During development, the majority of business logic was consolidated within the `home` application, including:

- Dashboard functionality
- Project management
- Messaging system
- File management
- Invoice generation
- Stripe payment integration

The remaining applications were retained to support future modular expansion and maintain a scalable project structure.


## Testing

Testing was carried out throughout the development process to ensure that all functionality worked correctly.

Both manual and automated testing methods were used.

---

### Manual Testing

| Feature | Test Performed | Result |
|----------|----------|----------|
| Registration | Create new user account | Pass |
| Login | Login with valid credentials | Pass |
| Logout | Logout from system | Pass |
| Dashboard Access | Access dashboard after login | Pass |
| Create Project | Create new project | Pass |
| Edit Project | Edit project details | Pass |
| Delete Project | Delete project | Pass |
| Create Message | Send project message | Pass |
| Edit Message | Edit own message | Pass |
| Delete Message | Delete own message | Pass |
| Admin Dashboard | Access admin dashboard | Pass |
| Client Management | Create client | Pass |
| Client Management | Edit client | Pass |
| Client Management | Delete client | Pass |
| File Upload | Upload project file | Pass |
| File Download | Open uploaded file | Pass |
| File Delete | Delete uploaded file | Pass |
| Invoice Download | Generate PDF invoice | Pass |
| Stripe Checkout | Redirect to Stripe | Pass |
| Search Function | Search projects | Pass |
| User Permissions | Prevent unauthorized access | Pass |

---

### Responsiveness Testing

The application was tested on:

| Device | Result |
|----------|----------|
| Desktop | Pass |
| Laptop | Pass |
| Tablet | Pass |
| Mobile Phone | Pass |

---

### Browser Testing

The application was tested using:

| Browser | Result |
|----------|----------|
| Google Chrome | Pass |
| Microsoft Edge | Pass |
| Mozilla Firefox | Pass |

---

## Automated Testing

Automated testing was implemented using Django's built-in testing framework.

The following tests were created:

### Dashboard Tests

- Client can access dashboard
- Administrator can access admin dashboard
- Client cannot access admin dashboard

### Project Tests

- Client can create project
- Client cannot edit another client's project

### Invoice Tests

- Invoice download creates invoice

### File Tests

- Client can upload project file
- Client can delete project file

---

### Automated Test Results

Command used:

```bash
python manage.py test
```

Result:

```text
Creating test database for alias 'default'...
System check identified no issues (0 silenced).

........
----------------------------------------------------------------------
Ran 8 tests in 5.791s

OK

Destroying test database for alias 'default'...
```

All automated tests passed successfully.

---

## Security

Several security measures have been implemented within the application.

### Authentication Security

- Django Authentication System
- Django Allauth
- Secure password hashing
- Session management

### Access Control

- Login required decorators
- Role based access control
- Client project ownership validation
- Admin-only functionality protection

### Payment Security

- Stripe hosted checkout
- Secure payment processing
- Secret keys stored in environment variables

### CSRF Protection

Django CSRF middleware is enabled to protect forms from Cross-Site Request Forgery attacks.

### Sensitive Data Protection

Sensitive information is stored using environment variables:

- SECRET_KEY
- STRIPE_SECRET_KEY
- STRIPE_PUBLIC_KEY
- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD

---

## Deployment

The application was deployed using Heroku.

### Deployment Steps

1. Create Heroku application.
2. Connect GitHub repository.
3. Configure environment variables.
4. Configure Stripe credentials.
5. Deploy application.
6. Run database migrations.
7. Verify application functionality.

### Environment Variables

The following environment variables were configured:

```text
SECRET_KEY
STRIPE_SECRET_KEY
STRIPE_PUBLIC_KEY
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL
CONTACT_EMAIL
DOMAIN
```

### Final Deployment Checks

- Static files served correctly
- Media files uploaded correctly
- Authentication working
- Stripe checkout working
- PDF invoices generating correctly

---

---

## Stripe Integration

Stripe Checkout was integrated to provide secure online payment processing.

### Stripe Features

The implementation includes:

- Secure card payments
- Stripe Checkout Sessions
- Payment success page
- Payment cancellation page
- Project payment tracking
- Invoice generation after payment
- Secure payment processing hosted by Stripe

### Payment Workflow

1. Administrator creates a project and quotation.
2. Client receives project information.
3. Client selects **Pay Now**.
4. Stripe Checkout Session is created.
5. Client completes payment securely on Stripe.
6. Payment confirmation is received.
7. Project status is updated.
8. Invoice becomes available for download.

### Stripe Security

Sensitive Stripe credentials are stored in environment variables and are not exposed within the source code.

Example:

```env
STRIPE_PUBLIC_KEY=
STRIPE_SECRET_KEY=
```

---

## Future Improvements

Several additional features could be implemented in future versions of the application.

### Planned Enhancements

- Email notifications
- Password reset email integration
- Multiple file uploads
- Client profile management
- Project timeline view
- Advanced search and filtering
- Administrator file visibility controls
- Project activity history
- PDF quotation generation
- Dashboard analytics
- Mobile application integration

### Long-Term Improvements

- PostgreSQL database
- AWS file storage
- Real-time messaging
- Two-factor authentication
- API integration
- Multi-user organisations

---

## Credits

### Frameworks

- Django
- Bootstrap

### Authentication

- Django Allauth

### Payments

- Stripe

### PDF Generation

- ReportLab

### Icons

- Font Awesome

### JavaScript Libraries

- jQuery

### Version Control

- Git
- GitHub

### Development Environment

- Visual Studio Code

---

## Author

### Student

Robertas Sladkevicius

### Course

Level 5 Diploma in Web Application Development

### Project

Milestone Project 4 – Full Stack Django Application

### Project Name

Artificium

---

## Disclaimer

This project was developed for educational purposes as part of the Level 5 Diploma in Web Application Development.

The application demonstrates:

- Full Stack Development
- Database Design
- Authentication Systems
- File Management
- Payment Processing
- PDF Generation
- Automated Testing
- Responsive User Interface Design

while following modern web development practices and Django framework conventions.
