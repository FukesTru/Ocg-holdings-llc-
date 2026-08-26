"""Page manifest for the OCG Financial site build.

Canonical structure: 4 service pages, 8 market pages + hub, core pages.
Retired URLs (cfo-services, financial-strategy, tax-services, and the
dropped city pages) are 301-redirected in vercel.json.
"""

BASE = "https://www.ocgfinancial.com/"


def svc_schema(name, slug, desc):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "serviceType": name,
        "description": desc,
        "url": BASE + "services/" + slug,
        "provider": {"@type": "FinancialService", "name": "OCG Financial", "url": BASE},
        "areaServed": {"@type": "Country", "name": "United States"},
    }


def faq_schema(pairs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in pairs
        ],
    }


def loc_schema(city, state, slug):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": "Financial Services for %s Businesses" % city,
        "serviceType": "Bookkeeping, Fractional CFO, Business Funding Readiness, Tax Preparation",
        "url": BASE + "locations/" + slug,
        "description": ("Bookkeeping, fractional CFO support, business funding readiness, and tax "
                        "preparation for businesses in and connected to the %s, %s market." % (city, state)),
        "provider": {"@type": "FinancialService", "name": "OCG Financial", "url": BASE},
        "areaServed": {"@type": "City", "name": city,
                       "containedInPlace": {"@type": "AdministrativeArea", "name": state}},
    }


def article_schema(title, slug, desc, date):
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "url": BASE + "resources/" + slug,
        "datePublished": date,
        "author": {"@type": "Person", "name": "Oscar Cancino"},
        "publisher": {"@type": "Organization", "name": "OCG Financial", "url": BASE},
    }


PAGES = [
    # ---------------- CORE ----------------
    dict(
        out="index.html", prefix="", nav="home", fragment="home.html", priority="1.0",
        title="Bookkeeping, Fractional CFO & Business Funding Support | OCG Financial",
        desc="Strategic financial partner for business owners: bookkeeping, fractional CFO support, funding readiness, and tax preparation built on real cash flow clarity.",
    ),
    dict(
        out="about.html", prefix="", nav="about", fragment="about.html", priority="0.8",
        title="About OCG Financial | Built by an Operator, for Business Owners",
        desc="OCG Financial was founded by Oscar Cancino, who grew up around business and has started, bought, and sold companies. Learn the philosophy behind the firm.",
        crumbs=[("About", None)],
    ),
    dict(
        out="contact.html", prefix="", nav="contact", fragment="contact.html", priority="0.9",
        title="Contact OCG Financial | Schedule a Consultation",
        desc="Get in touch with OCG Financial about bookkeeping, fractional CFO support, business funding readiness, or tax preparation. We reply personally, usually within a day.",
        crumbs=[("Contact", None)],
    ),
    dict(
        out="faqs.html", prefix="", nav="insights", fragment="faqs.html", priority="0.7",
        title="FAQs | Working With OCG Financial",
        desc="How OCG Financial engagements work: scope, onboarding timelines, bookkeeping cleanup, fractional CFO support, funding readiness, and business tax preparation.",
        crumbs=[("FAQs", None)],
        schema=[faq_schema([
            ("What does OCG Financial do?", "OCG Financial is a strategic financial partner for established business owners. The firm combines bookkeeping, fractional CFO support, business funding readiness, and tax preparation so that reporting, cash flow planning, and tax work all run off one clean set of numbers."),
            ("How is this different from a traditional bookkeeping or tax office?", "A bookkeeping or tax office records and files. OCG Financial builds the financial systems owners use to make decisions: cash flow visibility, margin clarity, forward forecasting, and reporting that holds up in front of a lender or investor."),
            ("Do I need to be in a specific city to work with OCG Financial?", "No. OCG Financial works with businesses across the United States, including companies in and connected to New York City, San Francisco, Boston, Chicago, Dallas, Miami, Los Angeles, and Washington, DC."),
            ("How quickly can we get started?", "Engagements begin with a consultation. From there, most clients reach financial clarity, meaning live reporting and a forward view of cash, early in the engagement."),
            ("How are engagements scoped?", "Every engagement is scoped to the business after a consultation. We look at transaction volume, entity structure, reporting needs, and the current state of your records, then agree the scope with you before any work begins."),
            ("Do you replace my CPA?", "Not necessarily. OCG Financial keeps books clean and tax-ready year round and can prepare returns directly or work alongside the CPA you already trust."),
        ])],
    ),
    dict(
        out="industries.html", prefix="", nav="", fragment="industries.html", priority="0.8",
        title="Industries We Serve | OCG Financial",
        desc="Financial systems for ecommerce and consumer brands, retail, real estate, professional services, and hospitality, built around how each industry moves cash.",
        crumbs=[("Industries", None)],
    ),
    dict(
        out="client-results.html", prefix="", nav="", fragment="client-results.html", priority="0.8",
        title="Client Results & Testimonials | OCG Financial",
        desc="What clients say about working with OCG Financial, alongside the firm's reporting, margin, and cash collection benchmarks across its client base.",
        crumbs=[("Client Results", None)],
    ),
    dict(
        out="tax-news.html", prefix="", nav="insights", fragment="tax-news.html", priority="0.8",
        title="Tax & Accounting News for Business Owners | OCG Financial",
        desc="Tax and accounting headlines from the Journal of Accountancy, Accounting Today, CPA Practice Advisor and Thomson Reuters, gathered in one place and refreshed daily.",
        crumbs=[("News", None)],
    ),
    dict(
        out="privacy-policy.html", prefix="", nav="", fragment="privacy.html", priority="0.3",
        title="Privacy Policy | OCG Financial",
        desc="How OCG Financial (OCG Holdings LLC) collects, uses, and protects your information when you use this website or engage the firm's services.",
        crumbs=[("Privacy Policy", None)],
    ),
    dict(
        out="terms-of-service.html", prefix="", nav="", fragment="terms.html", priority="0.3",
        title="Terms of Service | OCG Financial",
        desc="The terms that govern your use of the OCG Financial website and engagement of the firm's services.",
        crumbs=[("Terms of Service", None)],
    ),

    # ---------------- SERVICES (4 canonical) ----------------
    dict(
        out="services/bookkeeping.html", prefix="../", nav="", fragment="svc-bookkeeping.html", priority="0.9",
        title="Bookkeeping Services for Business Owners | OCG Financial",
        desc="Professional bookkeeping built for decisions, not just compliance: monthly close, account reconciliations, historical cleanup, and reporting your business can act on.",
        crumbs=[("Services", None), ("Bookkeeping", None)],
        schema=[
            svc_schema("Bookkeeping Services", "bookkeeping",
                       "Professional bookkeeping: monthly close, account reconciliations, historical cleanup, and investor-ready financial reporting for established businesses."),
            faq_schema([
                ("My books are months behind. Can that be fixed?", "Yes. Historical cleanup is one of the most common ways engagements begin. Records are rebuilt, every account is reconciled, and you end up with a clean, current baseline to work from."),
                ("What accounting software do you work in?", "Modern cloud accounting stacks, primarily QuickBooks Online and the tools that connect to it, including ecommerce platforms, payment processors, and inventory systems."),
                ("How fast is the monthly close?", "Once onboarded, most clients receive reconciled financials and reporting in the first half of the following month, on a consistent schedule."),
                ("Is bookkeeping enough on its own?", "It depends on what you need from your numbers. Bookkeeping tells you where the business has been. If you also need to plan where it is going, fractional CFO support adds forecasting, margin strategy, and decision cadence on top."),
                ("How is bookkeeping scoped?", "Scope depends on transaction volume, how many accounts and sales channels are involved, and whether historical cleanup is needed. It is agreed with you in the consultation before work begins."),
            ]),
        ],
    ),
    dict(
        out="services/fractional-cfo.html", prefix="../", nav="", fragment="svc-fractional.html", priority="0.9",
        title="Fractional CFO Services for Growing Businesses | OCG Financial",
        desc="Fractional CFO services deliver cash flow forecasting, margin clarity, financial reporting, and strategic guidance without the cost of a full-time CFO hire.",
        crumbs=[("Services", None), ("Fractional CFO Services", None)],
        schema=[
            svc_schema("Fractional CFO Services", "fractional-cfo",
                       "Fractional CFO services: cash flow forecasting, margin and unit economics analysis, financial strategy, KPI reporting, and investor-ready financial packages."),
            faq_schema([
                ("What is a fractional CFO?", "An experienced financial executive who works with your business on an ongoing basis without joining as a full-time hire. You get forecasting, cash flow strategy, margin analysis, and investor-ready reporting scoped to what the business actually needs."),
                ("How is this different from bookkeeping?", "Bookkeeping records what already happened. Fractional CFO work uses those numbers to plan what happens next: pricing, hiring, inventory, expansion, and capital decisions."),
                ("How long until I have real financial clarity?", "Most clients reach financial clarity early in the engagement, meaning live reporting, current books, and a forward view of cash."),
                ("Do I need clean books first?", "Not before you start. If the books need work, cleanup is handled as part of onboarding so the CFO layer is built on numbers you can trust."),
                ("What does fractional CFO support include?", "A monthly reporting and close cadence, rolling cash flow forecasting, margin and KPI review, scenario planning for major decisions, investor and lender reporting, and standing strategy sessions."),
                ("How is a fractional CFO engagement scoped?", "Engagements are scoped to outcomes rather than hours: a defined reporting and forecasting cadence, standing strategy sessions, and availability between them. Scope reflects the complexity of the business and is agreed before work begins."),
            ]),
        ],
    ),
    dict(
        out="services/business-funding.html", prefix="../", nav="", fragment="svc-funding.html", priority="0.9",
        title="Business Funding & Loan Readiness Support | OCG Financial",
        desc="Funding readiness for business owners: organized documentation, investor-ready reporting, and financial preparation so capital conversations start from a position of strength.",
        crumbs=[("Services", None), ("Business Funding", None)],
        schema=[
            svc_schema("Business Funding Readiness", "business-funding",
                       "Business funding readiness: financial documentation preparation, investor-ready reporting packages, and strategic guidance ahead of lender and investor conversations."),
            faq_schema([
                ("Does OCG Financial provide funding directly?", "No. OCG Financial is not a lender, broker, or investor. The work is preparation: organized financials, clear documentation, and reporting that stands up to review so you enter capital conversations prepared."),
                ("Can you guarantee I will get approved?", "No. No one honestly can. Approvals, rates, and terms are decided entirely by lenders and investors based on their own criteria. What preparation does is make sure your numbers are not the reason a conversation stalls."),
                ("What does funding readiness actually involve?", "Reviewing your current financial position, cleaning and reconciling the underlying books, assembling documentation lenders and investors typically request, building a defensible forward forecast, and preparing you for the questions that come up in review."),
                ("When should I start preparing?", "Well before you need capital. Clean books, consistent reporting, and a credible forecast take months to establish, and preparation is far harder once a deadline is already in front of you."),
                ("Do you work with my existing lender or advisor?", "Yes. Preparation work is designed to make every other professional in the conversation more effective, whether that is your banker, CPA, or attorney."),
            ]),
        ],
    ),
    dict(
        out="services/tax-preparation.html", prefix="../", nav="", fragment="svc-tax.html", priority="0.9",
        title="Business Tax Preparation Services | OCG Financial",
        desc="Business tax preparation supported by organized, reconciled records and year-round financial clarity, so filing is a checkpoint rather than a scramble.",
        crumbs=[("Services", None), ("Tax Preparation", None)],
        schema=[
            svc_schema("Business Tax Preparation", "tax-preparation",
                       "Business tax preparation supported by clean bookkeeping, organized year-round records, and coordinated filing for established business owners."),
            faq_schema([
                ("What makes tax preparation here different?", "The books underneath it. When records are reconciled and organized all year, preparation starts from clean data instead of a reconstruction project, and nothing has to be rebuilt under deadline pressure."),
                ("Do you replace my CPA?", "Not necessarily. OCG Financial can prepare returns directly or support the CPA you already work with by supplying clean, organized, filing-ready records."),
                ("Can you help if I am behind on filings?", "Yes. That work starts by rebuilding clean books for the affected periods, which is the foundation any catch-up filing requires, then coordinating the path back to current."),
                ("Will this reduce my tax bill?", "No one can promise a specific tax outcome. What clean records and year-round organization do is make sure legitimate deductions are documented rather than missed, and that decisions with tax consequences are made deliberately instead of discovered in April."),
                ("What affects the scope of tax preparation?", "Entity type, filing complexity, and the condition of the underlying records. All of it is reviewed and agreed in the consultation before work begins."),
            ]),
        ],
    ),

    # ---------------- LOCATIONS HUB ----------------
    dict(
        out="locations/index.html", prefix="../", nav="", fragment="locations-hub.html", priority="0.9",
        title="Markets We Serve | OCG Financial",
        desc="OCG Financial supports businesses in and connected to the country's major financial centers: New York, San Francisco, Boston, Chicago, Dallas, Miami, LA, and DC.",
        crumbs=[("Markets We Serve", None)],
    ),
]

# ---------------- LOCATIONS (8 target markets) ----------------
_LOC = [
    ("new-york", "New York City", "NY",
     "Bookkeeping, fractional CFO support, funding readiness, and tax preparation for New York City businesses operating at the pace their market demands."),
    ("san-francisco", "San Francisco", "CA",
     "Financial systems for San Francisco businesses: investor-ready reporting, burn and runway clarity, margin discipline, and funding readiness."),
    ("boston", "Boston", "MA",
     "Bookkeeping, fractional CFO support, funding readiness, and tax preparation for Boston businesses held to institutional standards of financial rigor."),
    ("chicago", "Chicago", "IL",
     "Financial clarity for Chicago businesses: clean books, working capital control, margin visibility, and reporting built for lender and investor review."),
    ("dallas", "Dallas", "TX",
     "Bookkeeping, fractional CFO support, funding readiness, and tax preparation for Dallas businesses scaling across Texas and beyond."),
    ("miami", "Miami", "FL",
     "Financial systems for Miami businesses: cash flow visibility, margin clarity, funding readiness, and tax preparation for fast-moving companies."),
    ("los-angeles", "Los Angeles", "CA",
     "Bookkeeping, fractional CFO support, funding readiness, and tax preparation for Los Angeles businesses across consumer brands, media, and services."),
    ("washington-dc", "Washington", "DC",
     "Financial systems for Washington, DC businesses: contract-driven cash flow, clean books, documentation discipline, and investor-ready reporting."),
]

for slug, city, state, desc in _LOC:
    label = "%s, %s" % (city, state)
    PAGES.append(dict(
        out="locations/%s.html" % slug, prefix="../", nav="", fragment="loc-%s.html" % slug, priority="0.8",
        title="Bookkeeping & Fractional CFO Services in %s | OCG Financial" % label,
        desc=desc,
        crumbs=[("Markets We Serve", "locations/index.html"), (label, None)],
        schema=[loc_schema(city, state, slug)],
    ))

# ---------------- ARTICLES ----------------
_ARTICLES = [
    ("cash-flow-mistakes", "The Cash Flow Mistakes Most Owners Make",
     "Five cash flow mistakes that quietly strain growing businesses, and the early warning systems that catch each one before it becomes urgent.", "2026-06-12"),
    ("profit-vs-cash", "Why Profitable Businesses Still Run Out of Cash",
     "A healthy profit and loss statement can hide a cash problem. How to see the gap between accounting profit and money in the bank before it hurts.", "2026-06-26"),
    ("bookkeeping-to-cfo", "When Bookkeeping Alone Isn't Enough Anymore",
     "Clean books tell you where the business has been. The signals that you now need help planning where it is going.", "2026-07-10"),
]

for slug, title, desc, date in _ARTICLES:
    PAGES.append(dict(
        out="resources/%s.html" % slug, prefix="../", nav="insights", fragment="art-%s.html" % slug, priority="0.6",
        title="%s | OCG Financial" % title,
        desc=desc,
        crumbs=[("News", "tax-news.html"), (title[:46] + ("…" if len(title) > 46 else ""), None)],
        schema=[article_schema(title, slug, desc, date)],
    ))
