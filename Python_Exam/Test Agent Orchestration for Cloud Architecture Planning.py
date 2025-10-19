# Agent Orchestration for Cloud Architecture Planning
# Format: Problem statement + Written response

"""
AGENT ORCHESTRATION CHALLENGE

You need to design a multi-agent system that can analyze business problems and recommend 
cloud architecture solutions. Focus on the orchestration strategy, not implementation details.

SAMPLE SCENARIOS (choose 2 to address):

1. "Simple E-commerce Site"
   - Online store for small business (1000 daily users)
   - Product catalog, shopping cart, payment processing
   - Basic admin dashboard for inventory management

2. "Customer Support Chatbot"
   - AI chatbot for customer service 
   - Integration with existing CRM system
   - Handle 500+ conversations per day
   - Escalate complex issues to human agents

3. "Employee Expense Tracker"
   - Mobile app for expense reporting
   - Receipt photo upload and processing
   - Approval workflow for managers
   - Integration with payroll system

YOUR TASK:
Design an agent orchestration approach that can take these problems and output 
a cloud architecture recommendation including basic services needed (database, 
API gateway, compute, storage, etc.).
"""

# Your Code Here

problem_statement = """
I picked two sample problems: the Simple E-commerce Site and the Customer Support Chatbot.
The goal is to guide a team of software agents so they can turn loose ideas into a clear
cloud design that covers the basics: compute, data storage, networking, security, and monitoring.
"""

agent_design = [
    {
        "name": "Context Collector",
        "role": "Reads the business description and pulls out user counts, must-have features, and any limits that jump out.",
        "input": "Original problem statement, any follow-up notes from stakeholders.",
        "output": "Plain-language summary with user scale, key features, and possible red flags."
    },
    {
        "name": "Requirement Mapper",
        "role": "Turns that summary into a simple checklist of technical needs.",
        "input": "Context Collector summary plus industry hints (for example, PCI for stores).",
        "output": "Checklist covering functions, data needs, expected traffic, compliance clues, and integration touchpoints."
    },
    {
        "name": "Solution Sketcher",
        "role": "Drafts a first pass at the cloud building blocks and how they talk to each other.",
        "input": "Requirement Mapper checklist.",
        "output": "Service map that matches each requirement to cloud services (compute, storage, network, security)."
    },
    {
        "name": "Cost and Risk Checker",
        "role": "Looks at the sketch for rough monthly cost, overkill choices, and missing safety nets.",
        "input": "Solution Sketcher service map plus any known budget guardrails.",
        "output": "Notes on estimated spend tiers, cheaper swap suggestions, and key risks to flag back to the team."
    },
    {
        "name": "Report Assembler",
        "role": "Turns all inputs into a tidy recommendation with diagrams, bullet lists, and next steps.",
        "input": "Outputs from Requirement Mapper, Solution Sketcher, and Cost and Risk Checker.",
        "output": "Human-friendly architecture brief that can be sent to stakeholders."
    }
]

agent_collaboration = """
For the Simple E-commerce Site, the Context Collector spots daily shoppers, the need for payment
processing, and inventory edits. The Requirement Mapper tags PCI concerns, peak traffic during
sales, and recurring jobs such as order confirmation emails. The Solution Sketcher lines up web
servers, a managed database, object storage for images, a payments gateway, and an admin API. The
Cost and Risk Checker double-checks that we stay on auto-scaling services to keep the small
business budget in check, then the Report Assembler packages everything.

For the Customer Support Chatbot, the Context Collector highlights high chat volume and the CRM tie-in.
The Requirement Mapper adds NLP handling, intent logging, and human hand-offs. The Solution Sketcher
brings in a managed chatbot service, serverless APIs, a knowledge base, and queueing for escalations.
The Cost and Risk Checker pays extra attention to message costs and data privacy, and the Report
Assembler shapes the plan so the support lead can sign off quickly.
"""

workflow_simple_ecommerce = """
Step 1: Context Collector reads the shop owner brief and, if something is vague (for example, payment
provider not named), it asks a clarifying question or notes the gap.
Step 2: Requirement Mapper translates the summary into clear items: web traffic numbers, checkout flow,
admin edits, data retention, compliance hints, and integrations (payments, email).
Step 3: Solution Sketcher matches each item to cloud parts: content delivery for speed, auto-scaling
compute for the web front, managed database for orders, object storage for product photos, and IAM
roles for admin access.
Step 4: Cost and Risk Checker reviews the sketch. If something looks off (say, costly dedicated servers),
it flags the issue and sends it back to the Solution Sketcher with a comment like “switch to serverless.”
Step 5: Report Assembler gathers the cleaned inputs and writes the final recommendation, adding a short
diagram and a to-do list for next steps.
If any agent fails or returns unclear info, the orchestrator re-runs that agent with the latest notes or
escalates to a human reviewer. The orchestrator also checks that every requirement has at least one
matching service before the report goes out.
"""

cloud_services_simple_ecommerce = """
- Compute: Use managed containers or serverless functions (for example, AWS Fargate or AWS Lambda) so
  the store can grow during flash sales without manual scaling.
- Storage: A managed SQL database (like Amazon RDS or Cloud SQL) for orders and customers; object storage
  (such as Amazon S3) for product images; optional Redis cache to speed up product catalog reads.
- Networking: An API gateway to handle checkout and admin APIs, a load balancer for web traffic, and a CDN
  to keep product pages fast worldwide.
- Security and Monitoring: Managed identity and access management, web application firewall, automated
  backups, CloudWatch-style metrics, and alerting for failed payments or slow pages.
Each pick keeps operations light for a small team, satisfies payment security, and can expand as the shop
gains more shoppers.
"""

reusability_plan = """
- Standardize: Keep shared templates for agent prompts, the requirement checklist format, and the report
  layout so every project starts with the same baseline.
- Customize: Allow the Context Collector and Solution Sketcher to plug in industry-specific playbooks
  (retail, finance, healthcare) that tweak their tips without rewriting agents.
- Learning: Save final recommendations, actual costs, and post-launch notes in a knowledge base. Agents
  reference this history when similar projects appear.
- Feedback: After each engagement, gather stakeholder comments and production metrics. Feed that back
  into the Cost and Risk Checker thresholds and the architecture templates so the system improves over time.
"""

practical_considerations = """
- Conflicting recommendations: The orchestrator runs a quick comparison meeting between Solution Sketcher
  and Cost and Risk Checker outputs, nudging them to agree or logging a clear trade-off note for a human decision.
- Vague problem statements: The Context Collector raises a clarification request list. If answers do not arrive,
  Report Assembler includes the open questions so expectations stay aligned.
- Hidden budget limits: Cost and Risk Checker provides tiered pricing (low, medium, stretch) so teams can pick
  the right fit even when budgets surface late.
- Legacy system integration: Requirement Mapper tags legacy services and passes interface details to Solution
  Sketcher, which adds hybrid connectors or VPN links as part of the design.
- New cloud services: Keep a lightweight registry of new offerings and price changes. Agents refresh from this
  registry on a schedule so recommendations stay current without manual digging.
"""



# === WRITTEN RESPONSE QUESTIONS ===

"""
QUESTION 1: AGENT DESIGN (20 points)
What agents would you create for this orchestration? Describe:
- 3-5 specific agents and their roles
- How they would collaborate on the sample problems
- What each agent's input and output would be

Example format:
Agent Name: Requirements Analyst
Role: Break down business requirements into technical needs
Input: Problem description + business context
Output: List of functional requirements, expected load, compliance needs

QUESTION 2: ORCHESTRATION WORKFLOW (25 points)
For ONE of the sample scenarios, walk through your complete workflow:
- Step-by-step process from problem statement to final recommendation
- How agents hand off information to each other
- What happens if an agent fails or produces unclear output
- How you ensure the final solution is complete and feasible

QUESTION 3: CLOUD RESOURCE MAPPING (20 points)
For your chosen scenario, what basic cloud services would your system recommend?
- Compute (serverless functions, containers, VMs)
- Storage (databases, file storage, caching)
- Networking (API gateways, load balancers, CDN)
- Security and monitoring basics
- Justify why each service fits the requirements

QUESTION 4: REUSABILITY & IMPROVEMENT (15 points)
How would you make this system work across different projects?
- What would you standardize vs. customize per project?
- How would the system learn from previous recommendations?
- What feedback mechanisms would improve future solutions?

QUESTION 5: PRACTICAL CONSIDERATIONS (20 points)
What challenges would you expect and how would you handle:
- Conflicting recommendations between agents
- Incomplete or vague problem statements
- Budget constraints not mentioned in requirements
- Integration with existing legacy systems
- Keeping up with new cloud services and pricing
"""

answer_q1 = """
Agent Name: Context Collector
Role: Turn the messy problem note into plain facts about users, features, and guardrails.
Input: Original scenario write-up, any clarifying replies.
Output: Short summary with audience size, mission-critical features, compliance hints, missing info.

Agent Name: Requirement Mapper
Role: Translate the summary into a checklist engineers can build from.
Input: Context Collector summary, industry playbooks (for example, retail or support).
Output: Functional checklist covering user stories, data needs, load expectations, integrations, compliance.

Agent Name: Solution Sketcher
Role: Pick fitting cloud building blocks and show how they connect.
Input: Requirement Mapper checklist.
Output: Draft architecture map tying each requirement to compute, storage, networking, IAM, and resilience pieces.

Agent Name: Cost and Risk Checker
Role: Stress-test the sketch for cost surprises, weak spots, or missing safety nets.
Input: Solution Sketcher map, known budget envelopes.
Output: Notes on spend tiers, cheaper alternatives, flagged risks, open questions for the team.

Agent Name: Report Assembler
Role: Package the findings into a human-friendly recommendation.
Input: Outputs from Requirement Mapper, Solution Sketcher, Cost and Risk Checker.
Output: Final report with summary, architecture diagram, service list, risks, and next actions.

Collaboration: The Context Collector kicks things off and hands its summary to the Requirement Mapper.
The Requirement Mapper cleans and structures the needs, then passes them to the Solution Sketcher.
The Solution Sketcher drafts the cloud layout and forwards it to the Cost and Risk Checker for review.
Once approved or adjusted, the Report Assembler bundles everything into the final recommendation.
"""

answer_q2 = """
Chosen Scenario: Simple E-commerce Site

1. Intake: Context Collector reads the shop brief, flags gaps (like missing payment provider), and gathers key facts: daily shoppers, need for secure checkout, admin portal.
2. Requirement Sweep: Requirement Mapper turns those facts into a checklist: user registration, product catalog CRUD, payment workflows, inventory updates, email confirmations, PCI awareness.
3. Architecture Draft: Solution Sketcher maps the checklist to services (auto-scaling web front end, managed SQL database, object storage for photos, payment gateway integration, CDN for speed, IAM roles for admins).
4. Review Loop: Cost and Risk Checker estimates cost tiers, verifies scaling strategy, checks backup and monitoring coverage. If something is off, it highlights the issue and the orchestrator re-runs Solution Sketcher with the feedback.
5. Final Package: Report Assembler builds the final document with the approved design, including a diagram placeholder, cost notes, and open questions such as “confirm preferred payment processor.”

Failures and Quality: If any agent produces vague output, the orchestrator either re-prompts that agent with more context or pings a human reviewer. Before sign-off, the orchestrator verifies that every item in the requirements checklist is matched to at least one cloud component so the recommendation is complete and realistic.
"""

answer_q3 = """
Scenario: Simple E-commerce Site

- Compute: Use a managed container platform or serverless functions (for example, AWS Fargate or Lambda) so the store scales up during flash sales without manual work.
- Storage: A managed relational database (Amazon RDS or GCP Cloud SQL) holds orders, users, and inventory; object storage (Amazon S3) keeps product photos, while a Redis-style cache speeds up product browsing.
- Networking: An API Gateway sits in front of the checkout and admin APIs; a managed load balancer spreads incoming web traffic; a CDN (CloudFront or Cloud CDN) keeps page loads snappy worldwide.
- Security and Monitoring: IAM for least-privilege access, a Web Application Firewall for common attacks, managed secrets storage for API keys, automated backups, plus CloudWatch-like monitoring and alerting for slow checkout pages or failed payments.

Each service keeps operations light for a small team, satisfies payment security needs, and can grow as the business takes off.
"""

answer_q4 = """
- Standardize: Keep shared agent prompts, requirement templates, and report layouts so every project follows the same playbook.
- Customize: Swap in industry-specific rule packs (retail, finance, healthcare) for Context Collector and Requirement Mapper to catch unique needs without retraining agents from scratch.
- Learning: Store final recommendations, real costs, and post-mortem notes in a knowledge base. Agents consult this history when facing similar cases.
- Feedback: After delivery, gather stakeholder feedback and production metrics. Feed those back into the Cost and Risk Checker thresholds and the solution templates so future runs get smarter.
"""

answer_q5 = """
- Conflicting recommendations: When Solution Sketcher and Cost and Risk Checker disagree, the orchestrator holds a comparison round, records the trade-offs, and either nudges a compromise or flags it for a human call.
- Vague requirements: Context Collector lists clarification questions up front. If answers stay missing, Report Assembler marks the open items so decision makers know the risk.
- Hidden budget limits: Cost and Risk Checker provides good/better/best cost tiers so stakeholders can pick an option even if budgets appear late.
- Legacy integrations: Requirement Mapper logs legacy systems and interface details; Solution Sketcher adds hybrid connectors (VPN, Direct Connect, integration middleware) to keep everything connected.
- Rapid cloud changes: Maintain a light-weight catalog of new services and price updates. Agents refresh from it on a schedule so their advice stays current without manual research every time.
"""
