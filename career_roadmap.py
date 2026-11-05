
import re


# =========================================
# CAREER CATEGORIES
# =========================================

CAREER_CATEGORIES = [
    "Auto-detect",
    "Technology & IT",
    "Business & Management",
    "Marketing & Media",
    "Commerce & Finance",
    "Creative & Design",
    "Education & Research",
    "Healthcare",
    "Law & Government",
    "Hospitality & Other Fields",
]


# =========================================
# CAREER EXAMPLES
# =========================================

CAREER_EXAMPLES = {
    "Auto-detect": [
        "AI Engineer",
        "Digital Marketing Specialist",
        "Data Analyst",
        "Graphic Designer",
    ],

    "Technology & IT": [
        "AI Engineer",
        "Machine Learning Engineer",
        "Python Developer",
        "Web Developer",
        "Data Scientist",
        "Cybersecurity Analyst",
        "Cloud Engineer",
        "Software Developer",
    ],

    "Business & Management": [
        "Business Analyst",
        "Project Manager",
        "Business Development Executive",
        "Product Manager",
        "Operations Manager",
    ],

    "Marketing & Media": [
        "Digital Marketing Specialist",
        "SEO Specialist",
        "Social Media Manager",
        "Content Marketing Manager",
        "Performance Marketing Specialist",
        "Brand Manager",
        "Content Creator",
        "Copywriter",
    ],

    "Commerce & Finance": [
        "Accountant",
        "Financial Analyst",
        "Investment Analyst",
        "Banking Professional",
        "Tax Consultant",
        "Business Finance Analyst",
    ],

    "Creative & Design": [
        "Graphic Designer",
        "UI/UX Designer",
        "Video Editor",
        "Motion Graphics Designer",
        "Web Designer",
        "Animator",
    ],

    "Education & Research": [
        "Teacher",
        "Research Assistant",
        "Academic Researcher",
        "Instructional Designer",
        "Education Consultant",
    ],

    "Healthcare": [
        "Healthcare Administrator",
        "Medical Laboratory Technologist",
        "Public Health Professional",
        "Healthcare Data Analyst",
    ],

    "Law & Government": [
        "Lawyer",
        "Legal Assistant",
        "Civil Services Officer",
        "Government Officer",
        "Legal Researcher",
    ],

    "Hospitality & Other Fields": [
        "Hotel Manager",
        "Event Manager",
        "Travel Consultant",
        "Hospitality Manager",
        "Entrepreneur",
    ],
}


# =========================================
# CAREER KEYWORDS FOR VALIDATION
# =========================================

CAREER_KEYWORDS = {
    "Technology & IT": [
        "ai engineer", "artificial intelligence",
        "machine learning", "ml engineer",
        "data scientist", "data analyst",
        "python developer", "software developer",
        "software engineer", "web developer",
        "frontend developer", "backend developer",
        "full stack developer", "cybersecurity",
        "cloud engineer", "devops", "database",
        "computer engineer", "it specialist",
        "programmer", "app developer",
    ],

    "Business & Management": [
        "business analyst", "business development",
        "project manager", "product manager",
        "operations manager", "management",
        "business manager", "entrepreneur",
    ],

    "Marketing & Media": [
        "marketing", "digital marketing",
        "seo specialist", "seo",
        "social media", "content marketing",
        "content creator", "copywriter",
        "brand manager", "performance marketing",
        "advertising", "media planner",
        "influencer", "public relations",
    ],

    "Commerce & Finance": [
        "accountant", "accounting",
        "financial analyst", "finance",
        "banking", "investment analyst",
        "tax consultant", "auditor",
        "stock market", "financial advisor",
    ],

    "Creative & Design": [
        "graphic designer", "ui designer",
        "ux designer", "ui/ux",
        "video editor", "animator",
        "motion graphics", "web designer",
        "illustrator", "photographer",
    ],

    "Education & Research": [
        "teacher", "professor", "researcher",
        "research assistant", "lecturer",
        "education consultant", "academic",
    ],

    "Healthcare": [
        "healthcare", "medical",
        "laboratory technologist", "public health",
        "health administrator",
        "healthcare analyst",
    ],

    "Law & Government": [
        "lawyer", "advocate", "legal assistant",
        "civil services", "government officer",
        "legal researcher", "judge",
    ],

    "Hospitality & Other Fields": [
        "hotel manager", "event manager",
        "travel consultant", "hospitality",
        "chef", "tourism", "entrepreneur",
    ],
}


# =========================================
# DETECT CAREER CATEGORY
# =========================================

def detect_career_category(career_goal):

    goal = career_goal.lower().strip()

    for category, keywords in CAREER_KEYWORDS.items():

        for keyword in keywords:

            if keyword in goal:
                return category

    return "Auto-detect"


# =========================================
# VALIDATE CAREER GOAL
# =========================================

def validate_career_goal(career_goal, selected_category):

    if not career_goal or not career_goal.strip():
        return False, "Please enter a career goal."

    detected_category = detect_career_category(career_goal)

    if selected_category == "Auto-detect":

        return True, detected_category

    if detected_category == "Auto-detect":

        # Unknown career names are allowed for manual categories.
        # The selected category is used as the user's intended stream.
        return True, selected_category

    if detected_category == selected_category:

        return True, detected_category

    return False, detected_category


# =========================================
# CAREER ROADMAP TEMPLATES
# =========================================

ROADMAPS = {}


ROADMAPS.update({

    "Technology & IT": {
        "skills": [
            "Programming fundamentals",
            "Problem solving and logical thinking",
            "Data structures and algorithms",
            "Git and GitHub",
            "Database management",
            "Software development practices",
        ],
        "tools": [
            "Python",
            "VS Code",
            "Git and GitHub",
            "SQL",
            "Postman",
            "Linux or macOS Terminal",
        ],
        "projects": [
            "Build a personal portfolio website",
            "Create a Python automation project",
            "Develop a database-based application",
            "Build a complete real-world application",
        ],
        "certifications": [
            "Python programming course",
            "SQL certification",
            "Git and GitHub course",
            "Relevant specialization course",
        ],
    },

    "Business & Management": {
        "skills": [
            "Business communication",
            "Problem solving",
            "Business strategy",
            "Leadership and teamwork",
            "Project management",
            "Decision making",
        ],
        "tools": [
            "Microsoft Excel",
            "PowerPoint",
            "Google Workspace",
            "Trello",
            "Notion",
            "Power BI",
        ],
        "projects": [
            "Prepare a business plan",
            "Create a market research report",
            "Develop a project management plan",
            "Build a business performance dashboard",
        ],
        "certifications": [
            "Business management course",
            "Project management fundamentals",
            "Excel certification",
            "Business communication course",
        ],
    },

    "Marketing & Media": {
        "skills": [
            "Digital marketing fundamentals",
            "Search Engine Optimization (SEO)",
            "Social media marketing",
            "Content writing and copywriting",
            "Paid advertising fundamentals",
            "Email marketing",
            "Marketing analytics",
            "Brand strategy and communication",
        ],
        "tools": [
            "Google Analytics",
            "Google Search Console",
            "Google Ads",
            "Meta Ads Manager",
            "Canva",
            "WordPress",
            "Google Trends",
            "Mailchimp",
        ],
        "projects": [
            "Create a social media marketing strategy for a local business",
            "Build and manage a sample Instagram content calendar",
            "Perform SEO research for a website",
            "Write SEO-friendly blog articles",
            "Create a sample Google Ads campaign plan",
            "Prepare a digital marketing performance report",
        ],
        "certifications": [
            "Google Digital Marketing course",
            "Google Analytics certification",
            "SEO fundamentals course",
            "Meta social media marketing course",
            "Content marketing course",
        ],
    },

    "Commerce & Finance": {
        "skills": [
            "Accounting fundamentals",
            "Financial analysis",
            "Excel and spreadsheets",
            "Financial reporting",
            "Taxation basics",
            "Business mathematics",
        ],
        "tools": [
            "Microsoft Excel",
            "Tally",
            "Power BI",
            "Google Sheets",
            "Accounting software",
        ],
        "projects": [
            "Prepare a sample balance sheet",
            "Create a monthly expense tracker",
            "Build a financial analysis report",
            "Develop a budgeting spreadsheet",
        ],
        "certifications": [
            "Advanced Excel course",
            "Accounting fundamentals",
            "Financial analysis course",
            "Relevant finance certification",
        ],
    },

    "Creative & Design": {
        "skills": [
            "Design fundamentals",
            "Color theory and typography",
            "Visual communication",
            "Creative thinking",
            "User experience principles",
            "Portfolio development",
        ],
        "tools": [
            "Canva",
            "Figma",
            "Adobe Photoshop",
            "Adobe Illustrator",
            "CapCut",
            "Adobe Premiere Pro",
        ],
        "projects": [
            "Design a personal portfolio",
            "Create a brand identity",
            "Design social media posts",
            "Build a mobile app interface",
            "Create a promotional video",
        ],
        "certifications": [
            "Graphic design fundamentals",
            "UI/UX design course",
            "Video editing course",
            "Relevant design specialization",
        ],
    },

    "Education & Research": {
        "skills": [
            "Subject knowledge",
            "Communication and presentation",
            "Research methodology",
            "Critical thinking",
            "Lesson planning",
            "Academic writing",
        ],
        "tools": [
            "Microsoft PowerPoint",
            "Google Classroom",
            "Microsoft Word",
            "Zotero",
            "Google Scholar",
        ],
        "projects": [
            "Prepare a sample lesson plan",
            "Create an educational presentation",
            "Write a research report",
            "Develop a learning resource",
        ],
        "certifications": [
            "Teaching fundamentals",
            "Research methodology",
            "Academic writing",
            "Relevant subject specialization",
        ],
    },

    "Healthcare": {
        "skills": [
            "Healthcare fundamentals",
            "Professional communication",
            "Medical terminology",
            "Healthcare data awareness",
            "Ethics and patient privacy",
            "Documentation",
        ],
        "tools": [
            "Microsoft Excel",
            "Healthcare information systems",
            "Documentation software",
            "Data reporting tools",
        ],
        "projects": [
            "Prepare a healthcare awareness presentation",
            "Create a sample healthcare administration report",
            "Study a public health case",
            "Build a non-clinical healthcare data dashboard",
        ],
        "certifications": [
            "Relevant healthcare qualification",
            "Healthcare administration course",
            "Medical terminology course",
            "Relevant accredited professional training",
        ],
    },

    "Law & Government": {
        "skills": [
            "Legal fundamentals",
            "Research and analysis",
            "Communication",
            "Critical thinking",
            "Constitutional knowledge",
            "Professional writing",
        ],
        "tools": [
            "Microsoft Word",
            "Google Scholar",
            "Legal research databases",
            "Microsoft PowerPoint",
        ],
        "projects": [
            "Prepare a legal case summary",
            "Write a research paper on a legal topic",
            "Create a constitutional studies presentation",
            "Prepare a public policy analysis",
        ],
        "certifications": [
            "Relevant law or public administration qualification",
            "Legal research course",
            "Communication skills course",
            "Relevant examination preparation",
        ],
    },

    "Hospitality & Other Fields": {
        "skills": [
            "Communication",
            "Customer service",
            "Problem solving",
            "Team management",
            "Planning and coordination",
            "Professional development",
        ],
        "tools": [
            "Microsoft Excel",
            "Google Workspace",
            "Canva",
            "Project planning software",
        ],
        "projects": [
            "Prepare an event management plan",
            "Create a sample travel itinerary",
            "Develop a customer service improvement plan",
            "Prepare a business proposal",
        ],
        "certifications": [
            "Customer service course",
            "Communication skills course",
            "Relevant hospitality training",
            "Project planning fundamentals",
        ],
    },

})


# =========================================
# CAREER-SPECIFIC SKILL ADDITIONS
# =========================================

def get_specialized_skills(career_goal):

    goal = career_goal.lower()

    if any(word in goal for word in ["seo", "search engine"]):

        return [
            "Keyword research",
            "On-page and off-page SEO",
            "Technical SEO",
            "Link building",
            "SEO performance analysis",
        ]

    if any(word in goal for word in ["social media", "content creator"]):

        return [
            "Content strategy",
            "Social media algorithms",
            "Audience engagement",
            "Content calendar planning",
            "Social media analytics",
        ]

    if any(word in goal for word in ["digital marketing", "performance marketing"]):

        return [
            "Campaign planning",
            "Paid advertising",
            "Conversion optimization",
            "Marketing funnels",
            "Campaign analytics",
        ]

    if any(word in goal for word in ["ai engineer", "machine learning"]):

        return [
            "Python programming",
            "NumPy and Pandas",
            "Statistics and mathematics",
            "Machine learning algorithms",
            "Model evaluation and deployment",
        ]

    if "data analyst" in goal or "data scientist" in goal:

        return [
            "Python",
            "SQL",
            "Statistics",
            "Data visualization",
            "Exploratory data analysis",
        ]

    if "ui/ux" in goal or "ui designer" in goal:

        return [
            "User research",
            "Wireframing",
            "Prototyping",
            "Usability testing",
            "Design systems",
        ]

    return []


# =========================================
# GENERATE CAREER ROADMAP
# =========================================

def generate_roadmap(
    career_goal,
    selected_category,
    roadmap_level
):

    career_goal = career_goal.strip()

    if not career_goal:
        raise ValueError("Please enter a career goal.")

    if selected_category == "Auto-detect":

        category = detect_career_category(career_goal)

        if category == "Auto-detect":
            category = "Technology & IT"

    else:
        category = selected_category

    if category not in ROADMAPS:
        category = "Technology & IT"

    roadmap = ROADMAPS[category]

    specialized_skills = get_specialized_skills(career_goal)

    skills = list(roadmap["skills"])

    for skill in specialized_skills:

        if skill not in skills:
            skills.insert(0, skill)

    level = roadmap_level.lower()

    if level == "beginner":

        phases = [
            (
                "Phase 1 — Foundation",
                "Weeks 1–4",
                [
                    "Understand the fundamentals of your career field.",
                    "Learn basic terminology and concepts.",
                    "Complete beginner-friendly tutorials.",
                    "Practise regularly with small exercises.",
                ],
            ),
            (
                "Phase 2 — Core Skills",
                "Weeks 5–8",
                [
                    "Learn the important tools used in the industry.",
                    "Build practical knowledge.",
                    "Study real-world examples.",
                    "Complete small practice assignments.",
                ],
            ),
            (
                "Phase 3 — Projects",
                "Weeks 9–12",
                [
                    "Build your first portfolio project.",
                    "Complete two practical projects.",
                    "Document your work.",
                    "Ask for feedback and improve your projects.",
                ],
            ),
            (
                "Phase 4 — Career Preparation",
                "Weeks 13–16",
                [
                    "Prepare your resume.",
                    "Create your portfolio.",
                    "Practise interview questions.",
                    "Apply for internships and entry-level opportunities.",
                ],
            ),
        ]

    elif level == "intermediate":

        phases = [
            (
                "Phase 1 — Skill Improvement",
                "Weeks 1–3",
                [
                    "Strengthen your existing knowledge.",
                    "Identify skill gaps.",
                    "Study intermediate concepts.",
                ],
            ),
            (
                "Phase 2 — Practical Experience",
                "Weeks 4–7",
                [
                    "Work with professional tools.",
                    "Complete realistic assignments.",
                    "Analyse real-world case studies.",
                ],
            ),
            (
                "Phase 3 — Advanced Projects",
                "Weeks 8–11",
                [
                    "Develop two advanced projects.",
                    "Create detailed project documentation.",
                    "Improve quality based on feedback.",
                ],
            ),
            (
                "Phase 4 — Professional Preparation",
                "Weeks 12–14",
                [
                    "Update your resume and portfolio.",
                    "Prepare for technical or role-specific interviews.",
                    "Apply for suitable jobs and internships.",
                ],
            ),
        ]

    else:

        phases = [
            (
                "Phase 1 — Advanced Knowledge",
                "Weeks 1–3",
                [
                    "Review advanced industry concepts.",
                    "Study emerging trends and practices.",
                    "Identify specialization opportunities.",
                ],
            ),
            (
                "Phase 2 — Specialization",
                "Weeks 4–6",
                [
                    "Choose a specific professional specialization.",
                    "Learn advanced tools and workflows.",
                    "Study industry standards.",
                ],
            ),
            (
                "Phase 3 — Professional Portfolio",
                "Weeks 7–10",
                [
                    "Build a high-quality professional project.",
                    "Document measurable outcomes.",
                    "Publish your work where appropriate.",
                ],
            ),
            (
                "Phase 4 — Career Advancement",
                "Weeks 11–12",
                [
                    "Improve your professional resume.",
                    "Prepare for advanced interviews.",
                    "Network with industry professionals.",
                    "Apply for relevant opportunities.",
                ],
            ),
        ]

    def make_list(items):

        return "\n".join(
            f"- {item}" for item in items
        )

    roadmap_text = f"""# 🚀 Career Roadmap: {career_goal}

**Career Category:** {category}

**Current Level:** {roadmap_level}

**Suggested Duration:** {phases[-1][1].split("–")[-1].strip()}

---

## 🎯 Career Objective

Your goal is to become a **{career_goal}**.

This roadmap provides a structured path to develop relevant knowledge,
practical skills, industry experience and a professional portfolio.

## 🧠 Important Skills to Learn

{make_list(skills)}

## 🛠️ Recommended Tools

{make_list(roadmap["tools"])}

---

## 📚 Your Learning Roadmap

"""

    for phase_title, duration, tasks in phases:

        roadmap_text += f"""### {phase_title}

**Duration:** {duration}

{make_list(tasks)}

"""

    roadmap_text += f"""---

## 💻 Recommended Portfolio Projects

Build these projects to demonstrate your practical abilities:

{make_list(roadmap["projects"])}

## 🎓 Recommended Courses and Certifications

{make_list(roadmap["certifications"])}

---

## 💼 Career Preparation

- Prepare a professional resume.
- Create a portfolio showcasing your best work.
- Practise communication and interview skills.
- Connect with professionals in your field.
- Look for internships and entry-level opportunities.
- Keep learning and updating your skills.

---

## 🏆 Portfolio Checklist

- [ ] Complete the foundation learning phase.
- [ ] Learn the important career-related skills.
- [ ] Practise with the recommended tools.
- [ ] Complete your first practical project.
- [ ] Complete at least two additional projects.
- [ ] Document your projects.
- [ ] Create a professional portfolio.
- [ ] Prepare and update your resume.
- [ ] Practise interview questions.
- [ ] Apply for internships or job opportunities.

---

## ⭐ Final Advice

Consistency is more important than speed. Practise regularly,
build real projects, ask for feedback and keep improving.

**Remember:** This roadmap is a learning guide. Actual qualifications,
licensing requirements and job expectations may vary by profession.
"""

    return roadmap_text
