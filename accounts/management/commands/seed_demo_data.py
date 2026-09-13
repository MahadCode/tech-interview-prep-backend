from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Create demo users, companies, job roles, tags, and questions."

    @transaction.atomic
    def handle(self, *args, **options):
        from accounts.models import User
        from taxonomy.models import Company, JobRole, Tag
        from questions.models import Question


        # ============================================================
        # 1. USERS
        # ============================================================

        users_data = [
            {
                "username": "aisha_khan",
                "first_name": "Aisha",
                "last_name": "Khan",
                "email": "aisha.khan.demo@example.com",
                "phone": "+923001100001",
                "bio": "Backend engineer focused on Python, Django, APIs, and distributed systems.",
            },
            {
                "username": "hamza_ahmed",
                "first_name": "Hamza",
                "last_name": "Ahmed",
                "email": "hamza.ahmed.demo@example.com",
                "phone": "+923001100002",
                "bio": "Full stack developer interested in scalable web applications and developer tooling.",
            },
            {
                "username": "sara_malik",
                "first_name": "Sara",
                "last_name": "Malik",
                "email": "sara.malik.demo@example.com",
                "phone": "+923001100003",
                "bio": "Frontend engineer specializing in React, JavaScript, and accessible user interfaces.",
            },
            {
                "username": "usman_raza",
                "first_name": "Usman",
                "last_name": "Raza",
                "email": "usman.raza.demo@example.com",
                "phone": "+923001100004",
                "bio": "Software engineer working with cloud infrastructure, Docker, and backend systems.",
            },
            {
                "username": "noor_fatima",
                "first_name": "Noor",
                "last_name": "Fatima",
                "email": "noor.fatima.demo@example.com",
                "phone": "+923001100005",
                "bio": "Data engineer passionate about PostgreSQL, pipelines, distributed processing, and analytics.",
            },
            {
                "username": "bilal_hassan",
                "first_name": "Bilal",
                "last_name": "Hassan",
                "email": "bilal.hassan.demo@example.com",
                "phone": "+923001100006",
                "bio": "Python developer building APIs and automation systems with Django and FastAPI.",
            },
            {
                "username": "zoya_ali",
                "first_name": "Zoya",
                "last_name": "Ali",
                "email": "zoya.ali.demo@example.com",
                "phone": "+923001100007",
                "bio": "Machine learning engineer interested in production ML systems and data platforms.",
            },
            {
                "username": "omar_siddiqui",
                "first_name": "Omar",
                "last_name": "Siddiqui",
                "email": "omar.siddiqui.demo@example.com",
                "phone": "+923001100008",
                "bio": "Senior software engineer focused on system design, APIs, and high-scale applications.",
            },
            {
                "username": "maryam_haider",
                "first_name": "Maryam",
                "last_name": "Haider",
                "email": "maryam.haider.demo@example.com",
                "phone": "+923001100009",
                "bio": "React developer with an interest in performance, testing, and frontend architecture.",
            },
            {
                "username": "ali_shah",
                "first_name": "Ali",
                "last_name": "Shah",
                "email": "ali.shah.demo@example.com",
                "phone": "+923001100010",
                "bio": "DevOps-minded engineer working with cloud deployments, CI/CD, and containerized applications.",
            },
        ]

        users = []

        for data in users_data:
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "email": data["email"],
                    "phone": data["phone"],
                    "bio": data["bio"],
                    "role": User.UserRole.USER,
                    "account_status": User.AccountStatus.ACTIVE,
                    "is_active": True,
                },
            )

            if created:
                user.set_password("DemoPassword123!")
                user.save()

            users.append(user)

        print(f"Users ready: {len(users)}")


        # ============================================================
        # 2. COMPANIES
        # ============================================================

        company_names = [
            "Google",
            "Microsoft",
            "Amazon",
            "Meta",
            "Apple",
            "Netflix",
            "Stripe",
            "Uber",
            "Airbnb",
            "Spotify",
        ]

        companies = {}

        for name in company_names:
            company, _ = Company.objects.get_or_create(
                name=name,
                defaults={"is_active": True},
            )
            companies[name] = company

        print(f"Companies ready: {len(companies)}")


        # ============================================================
        # 3. JOB ROLES
        # ============================================================

        role_names = [
            "Backend Engineer",
            "Frontend Engineer",
            "Full Stack Engineer",
            "Software Engineer",
            "Python Developer",
            "Django Developer",
            "React Developer",
            "DevOps Engineer",
            "Data Engineer",
            "Machine Learning Engineer",
        ]

        roles = {}

        for name in role_names:
            role, _ = JobRole.objects.get_or_create(
                name=name,
                defaults={"is_active": True},
            )
            roles[name] = role

        print(f"Job roles ready: {len(roles)}")


        # ============================================================
        # 4. TAGS
        # ============================================================

        tag_names = [
            "Python",
            "Django",
            "React",
            "JavaScript",
            "PostgreSQL",
            "REST API",
            "System Design",
            "Docker",
            "AWS",
            "Algorithms",
        ]

        tags = {}

        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(
                name=name,
                defaults={"is_active": True},
            )
            tags[name] = tag

        print(f"Tags ready: {len(tags)}")


        # ============================================================
        # 5. QUESTIONS
        #
        # 3 questions per user = 30 questions
        #
        # Each question has:
        # - one author
        # - one job role
        # - multiple companies
        # - multiple tags
        # - realistic difficulty
        # ============================================================

        questions_data = [

            # --------------------------------------------------------
            # AISHA
            # --------------------------------------------------------

            {
                "author": "aisha_khan",
                "title": "How would you optimize a slow Django API endpoint?",
                "description": (
                    "A Django API endpoint has started taking several seconds to respond "
                    "as the database grows. Walk through how you would identify the "
                    "bottleneck and improve the endpoint without changing its behavior."
                ),
                "difficulty": "medium",
                "role": "Django Developer",
                "companies": ["Google", "Microsoft", "Amazon"],
                "tags": ["Django", "Python", "PostgreSQL", "REST API"],
            },
            {
                "author": "aisha_khan",
                "title": "What is the difference between select_related and prefetch_related?",
                "description": (
                    "Explain how Django's select_related and prefetch_related work, "
                    "when you would use each one, and how they help prevent unnecessary "
                    "database queries."
                ),
                "difficulty": "medium",
                "role": "Backend Engineer",
                "companies": ["Amazon", "Microsoft", "Uber"],
                "tags": ["Django", "PostgreSQL", "Python"],
            },
            {
                "author": "aisha_khan",
                "title": "How would you design authentication for a REST API?",
                "description": (
                    "Design an authentication system for a production REST API. "
                    "Discuss sessions versus tokens, credential storage, CSRF, "
                    "authorization, and common security mistakes."
                ),
                "difficulty": "hard",
                "role": "Backend Engineer",
                "companies": ["Google", "Stripe", "Amazon"],
                "tags": ["REST API", "System Design", "Python"],
            },

            # --------------------------------------------------------
            # HAMZA
            # --------------------------------------------------------

            {
                "author": "hamza_ahmed",
                "title": "How would you structure a large full stack application?",
                "description": (
                    "You are starting a full stack application that will be maintained "
                    "by several developers. Explain how you would organize the frontend, "
                    "backend, shared interfaces, authentication, and deployment."
                ),
                "difficulty": "medium",
                "role": "Full Stack Engineer",
                "companies": ["Microsoft", "Airbnb", "Spotify"],
                "tags": ["React", "Django", "REST API", "System Design"],
            },
            {
                "author": "hamza_ahmed",
                "title": "What happens when you enter a URL in a browser?",
                "description": (
                    "Trace the major steps that occur after a user enters a URL and "
                    "presses Enter, including DNS resolution, TCP/TLS, HTTP, server "
                    "processing, and browser rendering."
                ),
                "difficulty": "medium",
                "role": "Software Engineer",
                "companies": ["Google", "Amazon", "Netflix"],
                "tags": ["REST API", "System Design"],
            },
            {
                "author": "hamza_ahmed",
                "title": "How would you handle API versioning?",
                "description": (
                    "A public API is already being used by thousands of clients, but "
                    "you need to introduce breaking changes. Explain different API "
                    "versioning strategies and how you would migrate existing clients."
                ),
                "difficulty": "hard",
                "role": "Full Stack Engineer",
                "companies": ["Stripe", "Microsoft", "Uber"],
                "tags": ["REST API", "System Design", "JavaScript"],
            },

            # --------------------------------------------------------
            # SARA
            # --------------------------------------------------------

            {
                "author": "sara_malik",
                "title": "Why does changing React state trigger a re-render?",
                "description": (
                    "Explain React's state update model and reconciliation process. "
                    "Discuss why directly mutating state is problematic and how React "
                    "determines which parts of the UI need to update."
                ),
                "difficulty": "medium",
                "role": "React Developer",
                "companies": ["Meta", "Airbnb", "Spotify"],
                "tags": ["React", "JavaScript"],
            },
            {
                "author": "sara_malik",
                "title": "How would you improve the performance of a React application?",
                "description": (
                    "A React application has become noticeably slower as it grows. "
                    "Describe how you would profile the application and identify "
                    "unnecessary renders, expensive computations, and large bundles."
                ),
                "difficulty": "hard",
                "role": "Frontend Engineer",
                "companies": ["Meta", "Netflix", "Google"],
                "tags": ["React", "JavaScript"],
            },
            {
                "author": "sara_malik",
                "title": "What is the difference between authentication and authorization?",
                "description": (
                    "Explain authentication and authorization using a web application "
                    "as an example. Describe how the frontend should interact with "
                    "the backend when a user signs in."
                ),
                "difficulty": "easy",
                "role": "Frontend Engineer",
                "companies": ["Google", "Microsoft", "Meta"],
                "tags": ["React", "REST API"],
            },

            # --------------------------------------------------------
            # USMAN
            # --------------------------------------------------------

            {
                "author": "usman_raza",
                "title": "What problem do Docker containers solve?",
                "description": (
                    "Explain containers, Docker images, and why containerization can "
                    "make development and deployment more predictable."
                ),
                "difficulty": "easy",
                "role": "DevOps Engineer",
                "companies": ["Amazon", "Microsoft", "Netflix"],
                "tags": ["Docker", "AWS"],
            },
            {
                "author": "usman_raza",
                "title": "How would you design a CI/CD pipeline?",
                "description": (
                    "Design a CI/CD pipeline for a web application. Include testing, "
                    "building, containerization, deployment, rollback strategy, and "
                    "environment management."
                ),
                "difficulty": "hard",
                "role": "DevOps Engineer",
                "companies": ["Amazon", "Netflix", "Spotify"],
                "tags": ["Docker", "AWS", "System Design"],
            },
            {
                "author": "usman_raza",
                "title": "How would you troubleshoot a production deployment failure?",
                "description": (
                    "A deployment succeeds during the build stage but the production "
                    "application fails to start. Explain the systematic steps you would "
                    "take to identify and fix the problem."
                ),
                "difficulty": "medium",
                "role": "DevOps Engineer",
                "companies": ["Microsoft", "Amazon", "Uber"],
                "tags": ["Docker", "AWS", "System Design"],
            },

            # --------------------------------------------------------
            # NOOR
            # --------------------------------------------------------

            {
                "author": "noor_fatima",
                "title": "What is database normalization and when can you avoid it?",
                "description": (
                    "Explain database normalization and its benefits. Then discuss "
                    "situations where controlled denormalization might improve the "
                    "performance of a production system."
                ),
                "difficulty": "medium",
                "role": "Data Engineer",
                "companies": ["Google", "Amazon", "Stripe"],
                "tags": ["PostgreSQL", "System Design"],
            },
            {
                "author": "noor_fatima",
                "title": "How do database indexes improve query performance?",
                "description": (
                    "Explain how an index allows a database to find rows more efficiently "
                    "and discuss the trade-offs of adding too many indexes."
                ),
                "difficulty": "easy",
                "role": "Data Engineer",
                "companies": ["Amazon", "Uber", "Airbnb"],
                "tags": ["PostgreSQL"],
            },
            {
                "author": "noor_fatima",
                "title": "How would you build a reliable data pipeline?",
                "description": (
                    "Design a pipeline that receives data from multiple sources and "
                    "loads it into an analytical database. Discuss validation, retries, "
                    "idempotency, monitoring, and failure recovery."
                ),
                "difficulty": "hard",
                "role": "Data Engineer",
                "companies": ["Google", "Spotify", "Amazon"],
                "tags": ["PostgreSQL", "AWS", "System Design"],
            },

            # --------------------------------------------------------
            # BILAL
            # --------------------------------------------------------

            {
                "author": "bilal_hassan",
                "title": "What are Python decorators and when would you use them?",
                "description": (
                    "Explain how Python decorators work and give practical examples "
                    "where decorators can simplify application code."
                ),
                "difficulty": "medium",
                "role": "Python Developer",
                "companies": ["Google", "Microsoft", "Spotify"],
                "tags": ["Python"],
            },
            {
                "author": "bilal_hassan",
                "title": "How does Django's request-response cycle work?",
                "description": (
                    "Walk through what happens when a request reaches a Django "
                    "application, including middleware, URL resolution, views, "
                    "database access, and the response."
                ),
                "difficulty": "medium",
                "role": "Django Developer",
                "companies": ["Amazon", "Microsoft", "Uber"],
                "tags": ["Django", "Python", "REST API"],
            },
            {
                "author": "bilal_hassan",
                "title": "How would you protect a Django API from common attacks?",
                "description": (
                    "Discuss practical defenses against CSRF, SQL injection, broken "
                    "authentication, excessive requests, insecure permissions, and "
                    "other common API security problems."
                ),
                "difficulty": "hard",
                "role": "Django Developer",
                "companies": ["Stripe", "Google", "Amazon"],
                "tags": ["Django", "Python", "REST API"],
            },

            # --------------------------------------------------------
            # ZOYA
            # --------------------------------------------------------

            {
                "author": "zoya_ali",
                "title": "What is the difference between training and inference?",
                "description": (
                    "Explain the difference between training a machine learning model "
                    "and running inference, including the computational and deployment "
                    "requirements of each."
                ),
                "difficulty": "easy",
                "role": "Machine Learning Engineer",
                "companies": ["Google", "Meta", "Microsoft"],
                "tags": ["Python", "AWS"],
            },
            {
                "author": "zoya_ali",
                "title": "How would you deploy a machine learning model to production?",
                "description": (
                    "Describe how you would package, deploy, monitor, and update a "
                    "machine learning model used by a production API."
                ),
                "difficulty": "hard",
                "role": "Machine Learning Engineer",
                "companies": ["Google", "Amazon", "Meta"],
                "tags": ["Python", "Docker", "AWS", "System Design"],
            },
            {
                "author": "zoya_ali",
                "title": "How do you prevent data leakage during model training?",
                "description": (
                    "Explain what data leakage is, provide examples of how it can "
                    "happen during feature engineering or dataset preparation, and "
                    "describe ways to prevent it."
                ),
                "difficulty": "medium",
                "role": "Machine Learning Engineer",
                "companies": ["Meta", "Google", "Spotify"],
                "tags": ["Python"],
            },

            # --------------------------------------------------------
            # OMAR
            # --------------------------------------------------------

            {
                "author": "omar_siddiqui",
                "title": "How would you design a URL shortening service?",
                "description": (
                    "Design a URL shortening service capable of handling millions of "
                    "requests. Discuss API design, ID generation, storage, caching, "
                    "availability, and scaling."
                ),
                "difficulty": "hard",
                "role": "Software Engineer",
                "companies": ["Google", "Amazon", "Microsoft"],
                "tags": ["System Design", "REST API", "PostgreSQL"],
            },
            {
                "author": "omar_siddiqui",
                "title": "How would you design a rate limiter?",
                "description": (
                    "Design a rate limiting system for a public API. Compare approaches "
                    "such as fixed windows, sliding windows, and token buckets, and "
                    "discuss how you would scale the solution."
                ),
                "difficulty": "hard",
                "role": "Backend Engineer",
                "companies": ["Stripe", "Uber", "Amazon"],
                "tags": ["System Design", "REST API", "PostgreSQL"],
            },
            {
                "author": "omar_siddiqui",
                "title": "What makes a distributed system difficult to design?",
                "description": (
                    "Discuss common challenges in distributed systems, including "
                    "network failures, consistency, latency, replication, and "
                    "coordination between services."
                ),
                "difficulty": "hard",
                "role": "Software Engineer",
                "companies": ["Google", "Netflix", "Amazon"],
                "tags": ["System Design", "AWS"],
            },

            # --------------------------------------------------------
            # MARYAM
            # --------------------------------------------------------

            {
                "author": "maryam_haider",
                "title": "What is the difference between controlled and uncontrolled inputs in React?",
                "description": (
                    "Explain controlled and uncontrolled form inputs in React and "
                    "describe when each approach might be appropriate."
                ),
                "difficulty": "easy",
                "role": "React Developer",
                "companies": ["Meta", "Airbnb", "Spotify"],
                "tags": ["React", "JavaScript"],
            },
            {
                "author": "maryam_haider",
                "title": "How would you test a React component?",
                "description": (
                    "Describe a practical testing strategy for a React component, "
                    "including user interactions, asynchronous behavior, and deciding "
                    "what should and should not be mocked."
                ),
                "difficulty": "medium",
                "role": "Frontend Engineer",
                "companies": ["Meta", "Microsoft", "Airbnb"],
                "tags": ["React", "JavaScript"],
            },
            {
                "author": "maryam_haider",
                "title": "How would you handle authentication state in a React application?",
                "description": (
                    "Explain how you would represent authentication state on the "
                    "frontend, handle expired sessions, protect routes, and keep the "
                    "frontend synchronized with the backend."
                ),
                "difficulty": "medium",
                "role": "React Developer",
                "companies": ["Google", "Meta", "Microsoft"],
                "tags": ["React", "JavaScript", "REST API"],
            },

            # --------------------------------------------------------
            # ALI
            # --------------------------------------------------------

            {
                "author": "ali_shah",
                "title": "What is the difference between horizontal and vertical scaling?",
                "description": (
                    "Explain horizontal and vertical scaling and discuss the advantages "
                    "and limitations of each approach for a web application."
                ),
                "difficulty": "easy",
                "role": "DevOps Engineer",
                "companies": ["Amazon", "Google", "Netflix"],
                "tags": ["AWS", "System Design"],
            },
            {
                "author": "ali_shah",
                "title": "How would you design a highly available web application?",
                "description": (
                    "Describe how you would architect a web application to remain "
                    "available when individual application servers or infrastructure "
                    "components fail."
                ),
                "difficulty": "hard",
                "role": "DevOps Engineer",
                "companies": ["Amazon", "Netflix", "Google"],
                "tags": ["AWS", "Docker", "System Design"],
            },
            {
                "author": "ali_shah",
                "title": "What is the purpose of health checks in production systems?",
                "description": (
                    "Explain liveness and readiness checks and how they can be used "
                    "by deployment and orchestration systems to detect unhealthy "
                    "application instances."
                ),
                "difficulty": "medium",
                "role": "DevOps Engineer",
                "companies": ["Microsoft", "Amazon", "Spotify"],
                "tags": ["Docker", "AWS", "System Design"],
            },
        ]


        # ============================================================
        # CREATE QUESTIONS
        # ============================================================

        created_count = 0
        updated_count = 0

        for data in questions_data:

            author = next(
                user for user in users
                if user.username == data["author"]
            )

            question, created = Question.objects.get_or_create(
                title=data["title"],
                defaults={
                    "author": author,
                    "job_role": roles[data["role"]],
                    "difficulty_level": data["difficulty"],
                    "description": data["description"],
                    "status": Question.QuestionStatus.PUBLISHED,
                    "is_deleted": False,
                },
            )

            # Make sure the data is correct even if the question already existed.
            question.author = author
            question.job_role = roles[data["role"]]
            question.difficulty_level = data["difficulty"]
            question.description = data["description"]
            question.status = Question.QuestionStatus.PUBLISHED
            question.is_deleted = False
            question.save()

            # Multiple companies per question
            question.company.set([
                companies[name]
                for name in data["companies"]
            ])

            # Multiple tags per question
            question.tag.set([
                tags[name]
                for name in data["tags"]
            ])

            if created:
                created_count += 1
            else:
                updated_count += 1


        # ============================================================
        # FINAL SUMMARY
        # ============================================================

        print("")
        print("=" * 55)
        print("DATABASE SEED COMPLETE")
        print("=" * 55)

        print(f"Users:     {User.objects.count()}")
        print(f"Companies: {Company.objects.count()}")
        print(f"Job Roles: {JobRole.objects.count()}")
        print(f"Tags:      {Tag.objects.count()}")
        print(f"Questions: {Question.objects.count()}")

        print("")
        print(f"Questions created: {created_count}")
        print(f"Questions updated: {updated_count}")

        print("")
        print("Demo password for all newly created users:")
        print("DemoPassword123!")

        print("")
        print("Users:")
        for user in users:
            print(f"  {user.username} -> {user.email}")

        print("")
        print("Each user has 3 questions.")
        print("Total seeded questions: 30")
        print("=" * 55)
