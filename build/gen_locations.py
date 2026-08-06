#!/usr/bin/env python3
"""Generate the eight market-page content fragments.

Copy is market-specific by design: each page speaks to how that economy
actually moves money. No page claims a physical OCG Financial office.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "content")

ALL = [
    ("new-york", "New York City", "NY"),
    ("san-francisco", "San Francisco", "CA"),
    ("boston", "Boston", "MA"),
    ("chicago", "Chicago", "IL"),
    ("dallas", "Dallas", "TX"),
    ("miami", "Miami", "FL"),
    ("los-angeles", "Los Angeles", "CA"),
    ("washington-dc", "Washington", "DC"),
]

# Note: p1 is deliberately not rendered. It restated the hero lead almost
# point for point on every page, so the intro now opens on p2. The copy is
# kept here in case it is ever wanted back.
CITIES = {
    "new-york": dict(
        eyebrow="New York City, NY",
        h1='Financial Clarity for <span class="grad-text">New York City</span> Businesses',
        lead="New York runs on capital, speed, and scrutiny. Businesses here are held to a higher standard of financial rigor, often earlier than they expect. OCG Financial builds the reporting and cash flow systems that let owners operate at that level with confidence.",
        p1="Few markets apply pressure like New York. Rent and payroll are unforgiving, competition for capital is constant, and the people reviewing your numbers, whether a bank, a private equity group, or a landlord, tend to be sophisticated. Financial systems that were adequate in a smaller market get exposed here quickly.",
        p2="What we see repeatedly in New York engagements is a business with real revenue and no forward visibility. Margins compress quietly, cash tightens as the business grows, and the reporting cannot answer the questions that decide whether a deal moves forward.",
        p3="The work is to close that gap: reconciled books, margin clarity by line of business, a rolling view of cash, and reporting built to be read by people who read a lot of it.",
        econ=[
            ("Professional and financial services", "Utilization, realization, and partner-level reporting"),
            ("Consumer brands and ecommerce", "Channel margin and inventory cash cycles"),
            ("Hospitality and food service", "Prime cost discipline in a high-rent market"),
            ("Real estate and construction", "Entity-level books and project returns"),
        ],
        faq=[
            ("Do you have an office in New York City?",
             "OCG Financial supports businesses in and connected to the New York market and works remotely. We are not claiming a Manhattan address, and the engagement is built to be responsive without one."),
            ("What size of New York business do you work with?",
             'Established, founder-led companies where the numbers now drive real decisions on hiring, inventory, expansion, or capital. See the <a href="{{p}}industries.html">industries we serve</a>.'),
            ("Can you prepare us for institutional review?",
             'That is the core of our <a href="{{p}}services/business-funding.html">funding readiness work</a>: financials, documentation, and forecasts organized to survive a serious review. We do not promise outcomes, only genuine preparation.'),
        ],
    ),
    "san-francisco": dict(
        eyebrow="San Francisco, CA",
        h1='Financial Systems for <span class="grad-text">San Francisco</span> Businesses',
        lead="In the Bay Area, financial credibility is currency. Investors and lenders here read financials closely, and a business that cannot explain its own unit economics loses ground fast. OCG Financial builds the clarity that stands up to that examination.",
        p1="San Francisco businesses tend to be measured on metrics rather than narratives: contribution margin, burn, runway, payback. Those numbers are only as trustworthy as the books beneath them, and in fast-moving companies the books are usually the thing that fell behind first.",
        p2="We also see the opposite failure. Businesses with excellent product instincts and no honest read on whether growth is actually funding itself. Revenue climbs, cash does not, and nobody can say precisely why until someone builds the model.",
        p3="Our work is to make the numbers defensible: clean books, unit economics you can explain in a meeting, a forward view of cash, and reporting structured the way capital providers expect to receive it.",
        econ=[
            ("Technology and subscription businesses", "Unit economics, retention math, and burn clarity"),
            ("Consumer brands and ecommerce", "Contribution margin after acquisition cost"),
            ("Professional and creative services", "Utilization and project-level profitability"),
            ("Food, beverage, and hospitality", "Labor and prime cost in a high-cost market"),
        ],
        faq=[
            ("Do you have a San Francisco office?",
             "No. OCG Financial works with businesses in and connected to the Bay Area on a remote-first basis, which is how most companies here prefer to operate anyway."),
            ("Can you produce investor-ready reporting?",
             'Yes. Investor-ready reporting is a standing feature of <a href="{{p}}services/fractional-cfo.html">fractional CFO support</a> rather than a one-off deliverable assembled under deadline.'),
            ("We are pre-profit. Is this still relevant?",
             'Often more so. When you are spending ahead of revenue, knowing exactly what cash is doing matters enormously. Start with <a href="{{p}}services/bookkeeping.html">clean books</a> and add the forward layer as decisions get bigger.'),
        ],
    ),
    "boston": dict(
        eyebrow="Boston, MA",
        h1='Financial Discipline for <span class="grad-text">Boston</span> Businesses',
        lead="Boston is a market built on institutions: established capital, long-standing firms, and a professional culture that expects things to be done properly. OCG Financial brings the same standard to the financial systems inside growing businesses here.",
        p1="Businesses in this market are often held to institutional standards of documentation and reporting earlier than businesses elsewhere. Whether the counterparty is a regional bank, a university, a healthcare system, or an established investor, the expectation is that your numbers arrive organized and reconciled.",
        p2="That expectation catches a lot of good businesses off guard. Revenue is solid, the operation works, but the financial reporting was never built to be examined by an outside party. The scramble to assemble it usually happens at the worst possible moment.",
        p3="We build that capability in advance: monthly close on schedule, margin clarity, forward cash forecasting, and documentation kept in a state where a serious review is an inconvenience rather than a crisis.",
        econ=[
            ("Professional and financial services", "Utilization, realization, and partner reporting"),
            ("Healthcare and life-science services", "Contract revenue and multi-entity clarity"),
            ("Education-adjacent and nonprofit-adjacent", "Grant, contract, and restricted-fund discipline"),
            ("Construction and trades", "Job costing, work in progress, and bonding-ready statements"),
        ],
        faq=[
            ("Do you have a Boston office?",
             "OCG Financial supports businesses in and connected to the Boston market remotely. We do not maintain a local office, and the engagement is structured so that is not a limitation."),
            ("Can you handle multi-entity structures?",
             'Yes. Entity-level books and consolidated reporting are common in this market, and both are handled within <a href="{{p}}services/bookkeeping.html">bookkeeping</a> and <a href="{{p}}services/fractional-cfo.html">CFO support</a>.'),
            ("We work with a regional bank. Can you prepare that package?",
             'Yes. Preparing the financial documentation lenders request is exactly what <a href="{{p}}services/business-funding.html">funding readiness</a> covers. Approval decisions remain entirely with the lender.'),
        ],
    ),
    "chicago": dict(
        eyebrow="Chicago, IL",
        h1='Working Capital Clarity for <span class="grad-text">Chicago</span> Businesses',
        lead="Chicago is an operator's market: manufacturing, distribution, logistics, professional services, and consumer brands built on real physical operations. Those businesses live and die on working capital, which is exactly where OCG Financial focuses.",
        p1="When a business carries inventory, equipment, or crews, cash timing decides almost everything. When receivables land, how long inventory sits, what a large purchase order does to liquidity three weeks out. None of that shows up usefully in an annual profit and loss statement.",
        p2="Chicago businesses also tend to have long-standing banking relationships, which is an advantage right up until the moment financial reporting cannot support a larger facility or a new line of credit.",
        p3="We build the system those decisions need: reconciled books, cost visibility at the level you actually operate, rolling cash forecasting, and statements a lender can underwrite without asking for three rounds of clarification.",
        econ=[
            ("Manufacturing and distribution", "Landed cost, inventory turns, and working capital control"),
            ("Logistics and transportation", "Equipment cost, utilization, and cash timing"),
            ("Professional services", "Utilization and project margin visibility"),
            ("Consumer and retail brands", "Channel profitability and seasonal cash planning"),
        ],
        faq=[
            ("Do you have a Chicago office?",
             "No. OCG Financial works with businesses in and connected to the Chicago market on a remote-first basis, with a reporting cadence that keeps everyone aligned."),
            ("Do you understand inventory-heavy businesses?",
             'Yes. Inventory and landed-cost accuracy is central to how we serve product businesses, including more than thirty ecommerce and consumer brands. See <a href="{{p}}industries.html">industries we serve</a>.'),
            ("Can you help us qualify for a larger credit facility?",
             'We prepare the financials and documentation that support the conversation through <a href="{{p}}services/business-funding.html">funding readiness</a>. The lender decides on approval and terms, not us.'),
        ],
    ),
    "dallas": dict(
        eyebrow="Dallas, TX",
        h1='Built for Growth in <span class="grad-text">Dallas</span>',
        lead="Dallas rewards businesses that scale well. Expansion here is common, capital is available, and the operators who win tend to be the ones whose financial systems kept pace with their ambition. OCG Financial builds those systems.",
        p1="Growth is the defining feature of this market, and growth is precisely what breaks financial infrastructure. New locations, larger contracts, more headcount, and heavier working capital demands all arrive at once, and the reporting that worked at one scale stops answering the questions that matter at the next.",
        p2="The pattern we see in Dallas engagements is a strong operator moving fast with numbers that lag two months behind. Decisions get made on instinct, and the instinct is usually good, but the margin for error narrows as the business gets bigger.",
        p3="We put the forward-looking layer in place: current books, margin clarity by location or line of business, expansion modeling before you commit capital, and reporting ready for the lenders and investors who fund growth here.",
        econ=[
            ("Construction and trades", "Job costing, work in progress, and bonding-ready statements"),
            ("Distribution and logistics", "Working capital and multi-location cost visibility"),
            ("Professional and business services", "Utilization, pricing, and project margins"),
            ("Multi-location retail and hospitality", "Location-level profit and loss and labor discipline"),
        ],
        faq=[
            ("Do you have a Dallas office?",
             "OCG Financial supports businesses in and connected to the Dallas market remotely. There is no local office, and the working rhythm is built to keep that irrelevant."),
            ("Can you model a second location or expansion?",
             'Yes. Expansion modeling is core <a href="{{p}}services/fractional-cfo.html">CFO work</a>: what the new location has to produce, when it turns cash positive, and what it does to liquidity in the meantime.'),
            ("We are adding headcount fast. Can you keep up?",
             'That is a reporting cadence question, and it is what the monthly close plus rolling forecast is designed for. Start with <a href="{{p}}services/bookkeeping.html">bookkeeping</a> if records are behind.'),
        ],
    ),
    "miami": dict(
        eyebrow="Miami, FL",
        h1='Financial Clarity for <span class="grad-text">Miami</span> Businesses',
        lead="Miami moves quickly. International trade, a deep consumer brand scene, active real estate, and a founder culture that raises and deploys capital aggressively. That pace is an advantage until the financial systems fall behind it.",
        p1="This is a market where opportunity arrives faster than infrastructure. Businesses scale on momentum, and reporting becomes the thing nobody had time to fix. Then a funding conversation, a partnership, or a cash squeeze makes it urgent.",
        p2="The recurring pattern in Miami engagements is revenue growing faster than visibility. Inventory and receivables quietly absorb the cash that growth produced, and margin erosion is discovered late because the books were weeks behind.",
        p3="Our job is to close that gap before it costs a decision or a term sheet: clean books, honest margin data, a forward view of cash, and financials that hold up when someone serious reviews them.",
        econ=[
            ("Ecommerce and consumer brands", "Inventory cash cycles and marketplace payouts handled correctly"),
            ("Import, export, and logistics", "Landed cost and multi-entity clarity for trade-driven operators"),
            ("Real estate and hospitality", "Entity-level books and project-level returns"),
            ("Professional services", "Utilization and project margins for fast-growing firms"),
        ],
        faq=[
            ("Is OCG Financial based in Miami?",
             'OCG Financial supports businesses in and connected to the Miami market. Engagements run remote-first, which is how most clients here prefer to work. <a href="{{p}}contact.html">Get in touch</a> to confirm details.'),
            ("What kinds of Miami businesses do you work with?",
             'Established, founder-led companies, particularly ecommerce and consumer brands, trade and logistics operators, real estate groups, and service firms. See <a href="{{p}}industries.html">industries we serve</a>.'),
            ("Can you help a Miami business prepare for capital?",
             'Yes, through <a href="{{p}}services/business-funding.html">funding readiness</a>. The preparation work starts months before any application, and we do not make promises about approvals or terms.'),
        ],
    ),
    "los-angeles": dict(
        eyebrow="Los Angeles, CA",
        h1='Financial Systems for <span class="grad-text">Los Angeles</span> Businesses',
        lead="Los Angeles is a market of brands, projects, and independent operators. Revenue arrives unevenly, costs are front-loaded, and cash timing rules everything. OCG Financial builds the clarity that turns creative momentum into a durable business.",
        p1="Much of the LA economy runs on project and campaign cycles: production schedules, product launches, wholesale orders, seasonal pushes. Money goes out well before it comes in, and a business can be genuinely successful while feeling permanently short of cash.",
        p2="Consumer brands here face the same trap in a different form. Inventory and marketing spend land immediately, revenue follows later, and the faster the brand grows the wider that gap becomes.",
        p3="We build around that reality: reconciled books, contribution margin by product and channel, cash forecasting that respects real timing, and reporting ready for the wholesale partners, lenders, and investors who scrutinize it.",
        econ=[
            ("Consumer brands and ecommerce", "Contribution margin by product and channel"),
            ("Media, production, and creative services", "Project-based cash timing and margin clarity"),
            ("Apparel and wholesale", "Inventory cycles and terms management"),
            ("Hospitality and wellness", "Labor and prime cost discipline"),
        ],
        faq=[
            ("Do you have a Los Angeles office?",
             "No. OCG Financial supports businesses in and connected to the Los Angeles market remotely, with a consistent reporting cadence rather than a local address."),
            ("Our revenue is seasonal and lumpy. Can you forecast that?",
             'Yes, and flat monthly averages are exactly the wrong tool for it. Forecasting built on your real annual curve is part of <a href="{{p}}services/fractional-cfo.html">fractional CFO support</a>.'),
            ("We sell wholesale and direct. Can you handle both?",
             'Yes. Multi-channel accounting, including platform payouts and processor fees, is standard in our <a href="{{p}}services/bookkeeping.html">bookkeeping service</a>.'),
        ],
    ),
    "washington-dc": dict(
        eyebrow="Washington, DC",
        h1='Documentation Discipline for <span class="grad-text">Washington, DC</span> Businesses',
        lead="Business in the capital region often runs on contracts, and contracts run on documentation. Precise records, defensible costs, and reporting that survives review are not optional here. OCG Financial builds financial systems to that standard.",
        p1="Contract-driven businesses face a distinct financial reality. Revenue is committed but paid on someone else's schedule, costs must be tracked and substantiated at a granular level, and the consequences of disorganized records extend well beyond an inconvenient tax season.",
        p2="Professional services firms in this market face a parallel problem: highly skilled teams whose profitability depends on utilization and pricing discipline that nobody is measuring accurately.",
        p3="We build the infrastructure that fits: clean books with cost detail that holds up to scrutiny, cash forecasting built around actual payment timing, and reporting organized for the reviews this market routinely requires.",
        econ=[
            ("Government-adjacent and contract services", "Cost tracking, documentation, and payment-cycle forecasting"),
            ("Professional and consulting firms", "Utilization, pricing, and project profitability"),
            ("Association and nonprofit-adjacent", "Restricted funds and grant-level reporting"),
            ("Hospitality and real estate", "Location and entity-level clarity"),
        ],
        faq=[
            ("Do you have a Washington, DC office?",
             "OCG Financial supports businesses in and connected to the DC market remotely. We do not claim a local office, and engagements are structured to work without one."),
            ("Our revenue is contract-based. Does that change the work?",
             'It changes where we focus: cost substantiation, payment timing, and cash forecasting around committed but slow-paying revenue. Handled within <a href="{{p}}services/fractional-cfo.html">CFO support</a>.'),
            ("Can you support an audit or a formal review?",
             'Clean, reconciled books with organized documentation are the foundation any review requires, and that is what <a href="{{p}}services/bookkeeping.html">bookkeeping</a> maintains year round.'),
        ],
    ),
}

PIN = ('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
       'aria-hidden="true"><path d="M12 21s-7-5.5-7-11a7 7 0 0 1 14 0c0 5.5-7 11-7 11z"/>'
       '<circle cx="12" cy="10" r="2.5"/></svg>')

SERVICE_CARDS = [
    ("bookkeeping", "Foundation", "Bookkeeping",
     "Clean, current, reconciled books with a monthly close you can plan around."),
    ("fractional-cfo", "Strategy", "Fractional CFO Services",
     "Forecasting, margin clarity, and investor-ready reporting without full-time overhead."),
    ("business-funding", "Capital", "Business Funding",
     "Identify funding options and strengthen the financial picture before you apply."),
    ("tax-preparation", "Compliance", "Tax Preparation",
     "Returns prepared from organized, reconciled records and kept filing-ready year round."),
]


def render(slug, c):
    label = c["eyebrow"]
    city = label.split(",")[0]

    ICONS = [
        '<path d="M3 3v18h18M7 15l4-5 3 3 5-7"/>',
        '<path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
        '<rect x="3" y="4" width="18" height="16" rx="1"/><path d="M3 9h18M8 4v16"/>',
        '<path d="M9 12l2 2 4-4M5 3h14v18l-7-4-7 4V3z"/>',
    ]
    focus = "\n".join(
        '''      <div class="lf-card">
        <div class="lf-ico"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">%s</svg></div>
        <h3>%s</h3>
        <p>%s</p>
      </div>''' % (ICONS[i % len(ICONS)], k, v)
        for i, (k, v) in enumerate(c["econ"])
    )

    faqs = "\n".join(
        '''      <details class="faq-item">
        <summary><h3>%s</h3><span class="faq-ico" aria-hidden="true"></span></summary>
        <div class="faq-body"><p>%s</p></div>
      </details>''' % (q, a) for q, a in c["faq"]
    )

    svc_cards = "\n".join(
        '''      <a class="related-card" href="{{p}}services/%s.html">
        <span class="tag">%s</span>
        <h3>%s</h3>
        <p>%s</p>
        <span class="go">Explore →</span>
      </a>''' % (sl, tag, name, desc) for sl, tag, name, desc in SERVICE_CARDS
    )

    others = "\n".join(
        '      <a class="loc-chip" href="{{p}}locations/%s.html">%s %s, %s</a>' % (sl, PIN, n, st)
        for sl, n, st in ALL if sl != slug
    )

    return '''<section class="page-hero loc-hero">
  <div class="orb" style="width:320px;height:320px;top:40px;right:-90px;" aria-hidden="true"></div>
  <div class="container">
    {{crumbs}}
    <h1>%(h1)s</h1>
    <p class="lead">%(lead)s</p>
    <div class="hero-cta">
      <a href="{{book}}" target="_blank" rel="noopener" class="btn btn-gold">Schedule a Consultation</a>
      <a href="#services" class="btn btn-ghost">See the Services</a>
    </div>
    <div class="hero-tags">
      <span>Founder-Led</span><span class="sep">·</span><span>Remote-First</span>
    </div>
  </div>
</section>

<section class="sec first" style="border-top:none;">
  <div class="container">
    <div class="section-head centered reveal">
      <span class="eyebrow">The Local Picture</span>
      <h2>What We See in the %(city)s Market</h2>
    </div>
    <div class="loc-intro reveal">
      <p>%(p2)s</p>
      <p>%(p3)s</p>
    </div>
  </div>
</section>

<section class="sec alt" aria-label="Where we add value in %(city)s">
  <div class="container">
    <div class="section-head centered reveal">
      <span class="eyebrow">Local Focus</span>
      <h2>Where We Add the Most Value in %(city)s</h2>
      <p>Different industries hide cash in different places. These are the areas we most often work on with %(city)s businesses.</p>
    </div>
    <div class="loc-focus reveal">
%(focus)s
    </div>
  </div>
</section>

<section class="sec" aria-label="What changes">
  <div class="container">
    <div class="section-head centered reveal">
      <span class="eyebrow">What Changes</span>
      <h2>Where Owners Feel the Difference</h2>
      <p>If the business generates serious revenue but the financial side feels like guesswork, this is the gap we close.</p>
    </div>
    <div class="benefit-grid cols-2 reveal" style="max-width:1000px;margin:0 auto;">
      <div class="benefit-card">
        <div class="icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div>
        <h3>Cash Stops Surprising You</h3>
        <p>A forward view of cash means pressure shows up in a forecast weeks before it reaches your account, while you still have choices.</p>
      </div>
      <div class="benefit-card">
        <div class="icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M3 3v18h18M7 15l4-5 3 3 5-7"/></svg></div>
        <h3>Overhead Becomes Visible</h3>
        <p>Fixed costs, labor, and margin by line of business get measured rather than estimated, so you can see what is genuinely carrying the company.</p>
      </div>
      <div class="benefit-card">
        <div class="icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M8 12l3 3 5-6"/></svg></div>
        <h3>Reporting Holds Up Outside</h3>
        <p>When a lender, investor, or acquirer asks for numbers, the package already exists and already reconciles.</p>
      </div>
      <div class="benefit-card">
        <div class="icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg></div>
        <h3>You Get Your Time Back</h3>
        <p>The hours spent reconciling spreadsheets return to running the business, with better information behind every decision.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec alt" id="services" aria-label="Services for %(city)s businesses">
  <div class="container">
    <div class="section-head centered reveal">
      <span class="eyebrow">Services</span>
      <h2>How We Work With %(city)s Businesses</h2>
      <p>Available individually or as one connected financial system.</p>
    </div>
    <div class="related-row reveal">
%(svc)s
    </div>
  </div>
</section>

<section class="sec" aria-label="Questions">
  <div class="container">
    <div class="section-head centered reveal">
      <span class="eyebrow">Questions</span>
      <h2>Working With OCG Financial in %(city)s</h2>
    </div>
    <div class="faq-list reveal" style="margin:0 auto;">
%(faqs)s
    </div>
    <p class="reveal" style="margin-top:32px;text-align:center;"><a href="{{p}}faqs.html" style="color:var(--gold);border-bottom:1px solid rgba(201,161,59,.35);">See all FAQs →</a></p>
  </div>
</section>

<section class="sec alt" aria-label="Get started">
  <div class="container">
    <div class="split" style="align-items:start;">
      <div class="body-copy reveal">
        <span class="eyebrow">Get Started</span>
        <h2>Ready to See Where Your Numbers Stand?</h2>
        <p>Every engagement begins with a consultation: an honest look at your current financial infrastructure and a clear view of what to address first. You keep the findings either way.</p>
        <div class="hero-cta" style="margin-top:28px;">
          <a href="{{book}}" target="_blank" rel="noopener" class="btn btn-gold">Schedule a Consultation</a>
          <a href="{{p}}contact.html" class="btn btn-ghost">Contact Us</a>
        </div>
      </div>
      {{ghl_form_short}}
    </div>
    <div class="reveal" style="margin-top:70px;text-align:center;">
      <span class="eyebrow" style="justify-content:center;">Other Markets We Serve</span>
      <div class="loc-chip-row" style="margin-top:22px;justify-content:center;">
%(others)s
      </div>
      <p style="margin-top:28px;"><a href="{{p}}locations/index.html" style="color:var(--gold);border-bottom:1px solid rgba(201,161,59,.35);">View all markets we serve →</a></p>
    </div>
  </div>
</section>
''' % dict(label=label, h1=c["h1"], lead=c["lead"], city=city,
           p1=c["p1"], p2=c["p2"], p3=c["p3"],
           focus=focus, svc=svc_cards, faqs=faqs, others=others)


if __name__ == "__main__":
    # Remove fragments for retired city pages so stale files cannot be built.
    keep = {"loc-%s.html" % s for s, _, _ in ALL}
    for f in os.listdir(OUT):
        if f.startswith("loc-") and f not in keep:
            os.remove(os.path.join(OUT, f))
            print("removed stale fragment", f)

    for slug, c in CITIES.items():
        with open(os.path.join(OUT, "loc-%s.html" % slug), "w", encoding="utf-8") as fh:
            fh.write(render(slug, c))
        print("wrote loc-%s.html" % slug)
