"""
EaseStart — BM25 Search Engine Core
Zero external dependencies. Pure Python implementation.
Based on proven ui-ux-pro-max-skill pattern.

V2 enhancements (2026-03-16):
- Stage-weighted scoring: same query returns stage-relevant results
- Min-score threshold: prevents low-quality recommendations
- Anti-pattern warnings: proactive mistake prevention

V3 enhancements (2026-03-18):
- Hash-based index cache: BM25 index built once per CSV, invalidated on file change
- Inspired by GitNexus staleness management + Repomix incremental processing
"""

import csv
import math
import os
import re
import json
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from typing import Optional


# --- Configuration ---

DATA_DIR = Path(__file__).parent.parent / "data"

# Minimum BM25 score to include in results.
# Below this threshold → agent should say "No confident data for this query"
MIN_SCORE_THRESHOLD = 0.5

# Stage-relevance multiplier: boost results matching the founder's current stage.
# Adjacent stages get a smaller boost. Far stages get no boost.
# Applied as: final_score = bm25_score × stage_weight
STAGE_RELEVANCE_WEIGHTS = {
    0: 1.5,   # exact stage match → 50% boost
    1: 1.2,   # adjacent stage → 20% boost
    2: 1.0,   # 2 stages away → no change
    3: 0.7,   # far away → penalty
}

# Lucius L5 Confidence Protocol — map BM25 scores to action levels.
# HIGH: agent proceeds autonomously. MEDIUM: present binary choice. LOW: ask founder.
CONFIDENCE_THRESHOLDS = {
    "HIGH": 3.0,    # BM25 ≥ 3.0 → strong confidence → proceed
    "MEDIUM": 1.0,  # BM25 1.0-2.99 → moderate → binary choice with recommendation
    # below 1.0 → LOW confidence → ask founder for input
}

EASESTART_CONFIG = {
    "stages":     {"file": "stages/_SCHEMA.csv",     "search_cols": ["Stage", "Keywords", "Exit_Criteria", "Key_Metrics", "Actions", "Frameworks"]},
    "tools":      {"file": "tools/_SCHEMA.csv",       "search_cols": ["Name", "Category", "Subcategory", "Keywords", "Best_For"]},
    "tools_anti_patterns": {"file": "tools/anti-patterns.csv", "search_cols": ["Tool_Name", "When_Not_To_Use", "Warning", "Stage_Anti_Pattern"]},
    "programs":   {"file": "programs/_SCHEMA.csv",    "search_cols": ["Name", "Provider", "Category", "Keywords", "Best_For"]},
    "resources":  {"file": "resources/_SCHEMA.csv",   "search_cols": ["Title", "Author", "Keywords", "Topics", "Key_Takeaways"]},
    "frameworks": {"file": "frameworks/_SCHEMA.csv",  "search_cols": ["Name", "Author", "Keywords", "Key_Concepts", "Steps"]},
    "playbook":   {"file": "playbook.csv",            "search_cols": ["Stage", "Category", "Rule", "Keywords", "Do", "Dont"]},
    "reasoning":  {"file": "reasoning/_SCHEMA.csv",   "search_cols": ["Stage", "Context", "Keywords", "Decision_Rules", "Recommended_Action"]},
    "industries": {"file": "industries/_SCHEMA.csv",  "search_cols": ["Industry", "Keywords", "Typical_Stage_Challenges", "Counter_Position_Examples", "Revenue_Model"]},
    "team_vetting":   {"file": "team/cofounder-vetting.csv", "search_cols": ["Check", "Category", "Question", "Green_Flag", "Red_Flag"]},
    "team_equity":    {"file": "team/equity-splits.csv",     "search_cols": ["Scenario", "Recommended_Split", "Reasoning", "Anti_Pattern"]},
    "legal":          {"file": "legal/checklist.csv",        "search_cols": ["Item", "Category", "Description", "DIY_Tool", "Giantiny_Note"]},
    "pricing":        {"file": "pricing/strategies.csv",     "search_cols": ["Strategy", "Type", "Keywords", "Description", "Best_For", "Example_Companies"]},
    "metrics":        {"file": "metrics/stage-metrics.csv",  "search_cols": ["Stage", "North_Star_Metric", "Key_Metrics", "Vanity_Metrics_To_Ignore", "AI_Methodology"]},
    "metrics_quality": {"file": "metrics/vanity-vs-real.csv", "search_cols": ["Metric", "Real_Or_Vanity", "Why", "What_To_Track_Instead"]},
    "psychology":     {"file": "psychology/burnout-signals.csv", "search_cols": ["Signal", "Category", "Description", "Self_Check_Question", "Intervention"]},
    "casestudies":    {"file": "casestudies/startups.csv",       "search_cols": ["Company", "Industry", "Stage_0_Problem", "Stage_1_Insight", "Key_Lesson", "Giantiny_Alignment"]},
    "templates":      {"file": "templates/templates.csv",        "search_cols": ["Template", "Category", "Keywords", "Purpose", "Sections"]},
    # Marketing domains
    "mkt_channels":   {"file": "marketing/channels.csv",         "search_cols": ["Channel", "Type", "Keywords", "Best_For", "Description", "Anti_Pattern"]},
    "mkt_content":    {"file": "marketing/content-playbook.csv", "search_cols": ["Content_Type", "Keywords", "Platform", "Example", "Anti_Pattern"]},
    "mkt_email":      {"file": "marketing/email-sequences.csv",  "search_cols": ["Sequence", "Keywords", "Subject_Line_Template", "Goal", "Body_Framework"]},
    "mkt_landing":    {"file": "marketing/landing-page.csv",     "search_cols": ["Element", "Keywords", "Description", "Do", "Dont", "Example_Good"]},
    "mkt_community":  {"file": "marketing/community.csv",        "search_cols": ["Pattern", "Keywords", "Description", "Do", "Dont", "Example"]},
    # Finance domains
    "fin_bookkeeping": {"file": "finance/bookkeeping.csv",       "search_cols": ["Task", "Keywords", "Category", "Description", "Do", "Dont"]},
    "fin_economics":   {"file": "finance/unit-economics.csv",    "search_cols": ["Metric", "Keywords", "Formula", "Category", "Why_It_Matters", "How_To_Improve"]},
    # Operations domains
    "ops_support":     {"file": "operations/support.csv",        "search_cols": ["Topic", "Keywords", "Category", "Description", "Do", "Dont"]},
    "ops_automation":  {"file": "operations/automation.csv",     "search_cols": ["Workflow", "Keywords", "Category", "Description", "Implementation", "Anti_Pattern"]},
    # Legal expansion
    "contracts":       {"file": "legal/contracts.csv",           "search_cols": ["Contract_Type", "Keywords", "When_Needed", "Key_Clauses", "Risk_If_Missing"]},
    "security":        {"file": "legal/security.csv",            "search_cols": ["Area", "Keywords", "Description", "Implementation", "Verification", "Risk_If_Ignored"]},
    # Analytics domains
    "analytics_events":  {"file": "analytics/event-taxonomy.csv",  "search_cols": ["Event_Name", "Category", "Stage", "Why_Track", "Anti_Pattern"]},
    "analytics_funnels": {"file": "analytics/funnel-templates.csv", "search_cols": ["Funnel_Name", "Product_Type", "Steps", "Fix_If_Broken", "Giantiny_Note"]},
    "analytics_tools":   {"file": "analytics/analytics-tools.csv",  "search_cols": ["Tool", "Category", "Key_Features", "Best_For", "Anti_Pattern"]},
    # --- Round 1-7 enrichment domains ---
    # Grow
    "mkt_launch":      {"file": "marketing/launch-platforms.csv",   "search_cols": ["Platform", "Type", "Keywords", "Description", "Best_For", "Anti_Pattern"]},
    "mkt_sales":       {"file": "marketing/sales-outreach.csv",    "search_cols": ["Tactic", "Category", "Keywords", "Description", "Do_This", "Avoid_This"]},
    "mkt_growth":      {"file": "marketing/growth-tactics.csv",    "search_cols": ["Tactic", "Category", "Keywords", "Description", "Do_This", "Avoid_This"]},
    "user_research":   {"file": "validation/user-research.csv",    "search_cols": ["Method", "Category", "Keywords", "Description", "How_To_Do", "Anti_Pattern"]},
    "positioning":     {"file": "marketing/positioning.csv",       "search_cols": ["Concept", "Category", "Keywords", "Description", "Do_This", "Avoid_This"]},
    "brand_identity":  {"file": "marketing/brand-identity.csv",    "search_cols": ["Element", "Category", "Keywords", "Description", "Do_This", "Anti_Pattern"]},
    "analytics":       {"file": "ops/analytics-setup.csv",         "search_cols": ["Step", "Category", "Keywords", "Description", "Tool", "Do_This", "Anti_Pattern"]},
    # Protect
    "privacy":         {"file": "legal/data-privacy.csv",          "search_cols": ["Requirement", "Category", "Keywords", "Description", "Implementation", "Risk_If_Ignored"]},
    "legal_resources": {"file": "legal/legal-resources.csv",       "search_cols": ["Resource", "Category", "Keywords", "Description", "Best_For", "Documents_Available"]},
    "insurance_risk":  {"file": "legal/insurance-risk.csv",        "search_cols": ["Risk", "Category", "Keywords", "Description", "Mitigation", "Priority"]},
    # People
    "hiring":          {"file": "team/hiring-playbook.csv",        "search_cols": ["Practice", "Category", "Keywords", "Description", "Do_This", "Avoid_This"]},
    "leadership":      {"file": "team/leadership.csv",             "search_cols": ["Skill", "Category", "Keywords", "Description", "Do_This", "Warning_Signs"]},
    "remote_work":     {"file": "team/remote-work.csv",            "search_cols": ["Practice", "Category", "Keywords", "Description", "Do_This", "Avoid_This"]},
    "founder_psych":   {"file": "psychology/founder-psychology.csv", "search_cols": ["Concept", "Category", "Keywords", "Description", "Impact_On_Founders", "Mitigation"]},
    # Money
    "fundraising":     {"file": "finance/fundraising.csv",         "search_cols": ["Topic", "Category", "Keywords", "Description", "Do_This", "Avoid_This"]},
    "revenue_opt":     {"file": "finance/revenue-optimization.csv", "search_cols": ["Strategy", "Category", "Keywords", "Description", "How_To_Do", "Anti_Pattern"]},
    # Build
    "mvp_patterns":    {"file": "build/mvp-patterns.csv",          "search_cols": ["Pattern", "Category", "Keywords", "Description", "When_To_Use", "Anti_Pattern"]},
    # Operate
    "startup_tools":   {"file": "ops/startup-tools.csv",           "search_cols": ["Tool", "Category", "Keywords", "Description", "Free_Tier", "Best_For"]},
    "customer_success": {"file": "ops/customer-success.csv",       "search_cols": ["Practice", "Category", "Keywords", "Description", "Do_This", "Warning_Signs"]},
    "automation":      {"file": "ops/automation-playbook.csv",     "search_cols": ["Task", "Category", "Keywords", "Description", "Tool", "Automate_When"]},
    # OSINT / Digital Intelligence
    "osint_tools":     {"file": "ops/osint-tools.csv",             "search_cols": ["Tool", "Category", "Keywords", "Description", "Free_Tier", "Best_For", "Anti_Pattern"]},
}

# Domain detection keywords
DOMAIN_KEYWORDS = {
    "stages":     ["what stage", "where am i", "exit criteria", "next step", "progress to", "phase"],
    "tools":      ["tech stack", "no-code", "recommend tool", "recommend a tool", "what software", "build with", "stack for", "platform for"],
    "tools_anti_patterns": ["don't use", "when not to use", "anti-pattern", "wrong tool for", "wrong tool", "avoid using", "should I avoid"],
    "programs":   ["credit", "free credits", "startup program", "discount", "deal", "aws", "gcp", "accelerator"],
    "resources":  ["book", "essay", "paul graham", "course", "article", "read", "learn"],
    "frameworks": ["framework", "lean canvas", "canvas", "method", "jobs-to-be-done", "jtbd", "mom test", "build-measure-learn", "customer discovery", "validate", "approach"],
    "playbook":   ["mistake", "don't", "do not", "advice", "best practice", "common mistake", "avoid", "rule"],
    "reasoning":  ["decide between", "brainstorm", "no idea", "don't have an idea", "start a startup", "pre-idea", "what if", "trade-off", "tradeoff", "help me think"],
    "industries": ["industry", "ecommerce", "marketplace", "fintech", "edtech", "devtools", "sector", "tam", "market size", "market trends", "market opportunity"],
    "team_vetting":   ["co-founder", "cofounder", "partner", "vet", "evaluate", "red flag", "green flag", "stay solo", "hire"],
    "team_equity":    ["equity", "split", "vesting", "shares", "cap table", "ownership"],
    "legal":          ["legal", "incorporate", "lawyer", "compliance", "gdpr", "privacy policy", "trademark", "patent", "llc", "c-corp", "s-corp", "register company", "llc or c-corp"],
    "pricing":        ["pricing", "price", "freemium", "subscription", "revenue model", "charge", "monetize", "how much", "price my", "saas pricing"],
    "metrics":        ["metric", "kpi", "north star", "track", "measure", "analytics"],
    "metrics_quality": ["vanity metric", "real metric", "vanity metrics"],
    "psychology":     ["burnout", "stress", "mental health", "tired", "overwhelmed", "imposter", "anxiety", "resilience", "wellness", "exhausted", "founder burnout", "dealing with burnout", "solo founder face"],
    "casestudies":    ["case study", "how did", "startup story", "learn from", "grew", "bootstrapped", "basecamp", "stripe", "notion", "linear", "figma"],
    "templates":      ["template", "fill out", "interview script", "pitch deck", "document template"],
    # Marketing
    "mkt_channels":   ["marketing channel", "growth channel", "acquisition", "distribution", "traffic", "organic", "paid", "product hunt", "launch strategy"],
    "mkt_content":    ["content", "blog", "seo", "social media", "content marketing", "content strategy"],
    "mkt_email":      ["email", "newsletter", "drip", "sequence", "welcome email", "onboarding email"],
    "mkt_landing":    ["landing page", "homepage", "conversion", "cta", "above the fold", "signup page", "hero section", "hero"],
    "mkt_community":  ["community", "discord", "forum", "members", "user group", "engagement", "community building"],
    # Finance
    "fin_bookkeeping": ["bookkeeping", "accounting", "expense", "invoice", "tax", "filing", "receipt", "p&l", "profit loss", "do bookkeeping"],
    "fin_economics":   ["unit economics", "ltv", "cac", "mrr", "arr", "churn rate", "burn rate", "runway", "margin", "payback"],
    # Operations
    "ops_support":     ["customer support", "help desk", "ticket", "sla", "response time", "support system"],
    "ops_automation":  ["automate", "workflow", "zapier", "cron", "scheduled", "monitoring", "alert"],
    # Legal expansion
    "contracts":       ["contract", "agreement", "nda", "founders agreement", "contractor", "employment", "offer letter"],
    "security":        ["security", "encryption", "https", "vulnerability", "backup", "cors", "data protection", "secure", "security best practices"],
    # Analytics domains
    "analytics_events":  ["event", "track", "tracking", "what to track", "event taxonomy", "capture", "log event"],
    "analytics_funnels": ["funnel", "activation", "retention curve", "drop-off", "conversion", "aarrr", "pirate metrics", "onboarding funnel"],
    "analytics_tools":   ["analytics tool", "amplitude", "google analytics", "session replay", "heatmap"],
    # --- Round 1-7 enrichment domains ---
    "mkt_launch":      ["launch", "product hunt", "producthunt", "hacker news", "beta launch", "launch platform", "launch strategy", "announce"],
    "mkt_sales":       ["sales", "outreach", "cold email", "cold outreach", "b2b sales", "sales process", "icp", "prospecting"],
    "mkt_growth":      ["growth hacking", "first 1000 users", "growth tactics", "viral", "referral", "growth loop", "word of mouth"],
    "user_research":   ["user research", "customer discovery", "mom test", "discovery interview", "user interview", "sean ellis", "pmf survey", "validate idea"],
    "positioning":     ["positioning", "value proposition", "counter-positioning", "category design", "competitive advantage", "differentiation", "icp"],
    "brand_identity":  ["brand", "brand name", "naming", "logo", "visual identity", "brand voice", "brand guide", "brand identity", "typography system", "color palette"],
    "analytics":       ["product analytics", "analytics setup", "tracking plan", "posthog", "mixpanel", "analytics implementation", "a/b test", "experiment"],
    "privacy":         ["data privacy", "gdpr", "ccpa", "cookie consent", "privacy policy", "data protection regulation", "data breach", "personal data"],
    "legal_resources": ["legal template", "legal resource", "startup lawyer", "free legal", "legal service", "legal platform", "clerky", "stripe atlas"],
    "insurance_risk":  ["insurance", "business insurance", "liability", "cyber insurance", "d&o", "intellectual property", "ip assignment", "risk management"],
    "hiring":          ["hire", "hiring", "first hire", "recruit", "job posting", "interview process", "hiring playbook", "talent"],
    "leadership":      ["leadership", "ceo", "management", "1-on-1", "one on one", "delegation", "engineering team", "team culture", "manager"],
    "remote_work":     ["remote", "async", "distributed team", "remote work", "work from home", "virtual team", "remote culture", "timezone"],
    "founder_psych":   ["cognitive bias", "confirmation bias", "sunk cost", "first principles", "mental model", "dunning kruger", "loss aversion", "decision fatigue", "imposter syndrome founder"],
    "fundraising":     ["fundraise", "fundraising", "raise", "pre-seed", "seed round", "series a", "investor", "pitch deck", "vc funding", "bootstrap vs", "angel investor"],
    "revenue_opt":     ["revenue optimization", "net revenue retention", "nrr", "dunning", "involuntary churn", "annual plan", "expansion revenue", "rule of 40"],
    "mvp_patterns":    ["mvp pattern", "concierge mvp", "wizard of oz", "landing page mvp", "mvp type", "prototype", "minimum viable", "api-first mvp"],
    "startup_tools":   ["startup tools", "best tools", "saas tools", "payment processing", "indie hacker tools", "tool stack", "startup software"],
    "customer_success": ["customer success", "health score", "customer health", "churn prevention", "onboarding flow", "nps", "customer retention", "qbr"],
    "automation":      ["automation playbook", "ci/cd", "cicd", "automate billing", "automate email", "what to automate", "monitoring alerting"],
    # OSINT / Digital Intelligence
    "osint_tools":     ["osint", "competitive intelligence", "brand scan", "domain lookup", "shodan", "wayback machine", "metadata", "reconnaissance", "competitor scan", "digital intelligence", "brand availability"],
}

# Cross-domain linking: when searching one domain, suggest related domains
CROSS_DOMAIN_LINKS = {
    "pricing":        ["reasoning", "casestudies", "playbook"],
    "team_vetting":   ["team_equity", "legal", "playbook"],
    "team_equity":    ["team_vetting", "legal", "reasoning"],
    "legal":          ["team_equity", "stages", "tools"],
    "metrics":        ["metrics_quality", "stages", "reasoning"],
    "metrics_quality": ["metrics", "playbook"],
    "psychology":     ["playbook", "reasoning"],
    "tools":          ["tools_anti_patterns", "programs"],
    "frameworks":     ["reasoning", "resources", "casestudies"],
    "stages":         ["metrics", "playbook", "reasoning"],
    "casestudies":    ["frameworks", "industries", "playbook"],
    "templates":      ["frameworks", "playbook"],
    # Marketing cross-links
    "mkt_channels":   ["mkt_content", "mkt_email", "mkt_landing", "playbook"],
    "mkt_content":    ["mkt_channels", "mkt_email", "casestudies"],
    "mkt_email":      ["mkt_content", "mkt_landing", "ops_automation"],
    "mkt_landing":    ["mkt_channels", "mkt_content", "pricing"],
    "mkt_community":  ["mkt_content", "mkt_channels", "ops_support"],
    # Finance cross-links
    "fin_bookkeeping": ["fin_economics", "legal", "pricing"],
    "fin_economics":   ["fin_bookkeeping", "metrics", "pricing"],
    # Operations cross-links
    "ops_support":     ["mkt_community", "ops_automation", "templates"],
    "ops_automation":  ["ops_support", "mkt_email", "tools"],
    # Legal expansion cross-links
    "contracts":       ["legal", "team_equity", "team_vetting"],
    "security":        ["legal", "tools", "ops_automation"],
    # Analytics cross-links
    "analytics_events":  ["analytics_funnels", "analytics_tools", "metrics"],
    "analytics_funnels": ["analytics_events", "metrics_quality", "casestudies"],
    "analytics_tools":   ["analytics_events", "tools", "ops_automation"],
    # --- Round 1-7 enrichment cross-links ---
    "mkt_launch":       ["mkt_channels", "mkt_content", "mkt_landing"],
    "mkt_sales":        ["mkt_channels", "mkt_email", "pricing"],
    "mkt_growth":       ["mkt_channels", "mkt_content", "analytics"],
    "user_research":    ["frameworks", "positioning", "founder_psych"],
    "positioning":      ["user_research", "mkt_content", "pricing"],
    "brand_identity":   ["mkt_content", "mkt_landing", "positioning"],
    "analytics":        ["analytics_events", "metrics", "customer_success"],
    "privacy":          ["legal", "security", "insurance_risk"],
    "legal_resources":  ["legal", "contracts", "privacy"],
    "insurance_risk":   ["legal", "privacy", "contracts"],
    "hiring":           ["team_vetting", "team_equity", "leadership"],
    "leadership":       ["hiring", "psychology", "remote_work"],
    "remote_work":      ["leadership", "hiring", "ops_automation"],
    "founder_psych":    ["psychology", "reasoning", "user_research"],
    "fundraising":      ["pricing", "fin_economics", "team_equity"],
    "revenue_opt":      ["pricing", "fin_economics", "customer_success"],
    "mvp_patterns":     ["frameworks", "tools", "user_research"],
    "startup_tools":    ["tools", "ops_automation", "analytics"],
    "customer_success": ["revenue_opt", "analytics", "mkt_email"],
    "automation":       ["ops_automation", "startup_tools", "analytics"],
    # OSINT / Digital Intelligence
    "osint_tools":      ["security", "positioning", "brand_identity", "mkt_launch"],
}


# --- Tokenizer ---

STOP_WORDS = frozenset([
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "i", "my", "me",
    "we", "our", "you", "your", "it", "its", "this", "that", "these",
    "those", "what", "which", "who", "how", "when", "where", "not", "no"
])


def tokenize(text: str) -> list[str]:
    """Normalize and tokenize text into searchable terms."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    tokens = text.split()
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 1]


# --- BM25 Scoring ---

class BM25:
    """BM25 ranking function. Zero dependencies."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus = []
        self.doc_freqs = Counter()
        self.doc_lens = []
        self.avgdl = 0
        self.n_docs = 0

    def index(self, documents: list[list[str]]):
        """Build index from tokenized documents."""
        self.corpus = documents
        self.n_docs = len(documents)
        self.doc_lens = [len(doc) for doc in documents]
        self.avgdl = sum(self.doc_lens) / max(self.n_docs, 1)

        for doc in documents:
            unique_terms = set(doc)
            for term in unique_terms:
                self.doc_freqs[term] += 1

    def score(self, query_tokens: list[str]) -> list[float]:
        """Score all documents against query tokens."""
        scores = [0.0] * self.n_docs

        for token in query_tokens:
            if token not in self.doc_freqs:
                continue

            df = self.doc_freqs[token]
            idf = math.log((self.n_docs - df + 0.5) / (df + 0.5) + 1)

            for i, doc in enumerate(self.corpus):
                tf = doc.count(token)
                if tf == 0:
                    continue
                dl = self.doc_lens[i]
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
                scores[i] += idf * numerator / denominator

        return scores


# --- CSV Loading ---

def load_csv(domain: str) -> tuple:
    """Load CSV data for a domain. Returns (rows, search_columns)."""
    if domain not in EASESTART_CONFIG:
        return [], []

    config = EASESTART_CONFIG[domain]
    filepath = DATA_DIR / config["file"]

    if not filepath.exists():
        return [], config["search_cols"]

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except (csv.Error, UnicodeDecodeError, IOError) as e:
        print(f"  ⚠️  Error loading {filepath}: {e}")
        return [], config["search_cols"]

    return rows, config["search_cols"]


def rows_to_documents(rows: list[dict], search_cols: list[str]) -> list[list[str]]:
    """Convert CSV rows into tokenized documents for BM25."""
    documents = []
    for row in rows:
        text_parts = []
        for col in search_cols:
            value = row.get(col, "")
            if value:
                text_parts.append(value)
        full_text = " ".join(text_parts)
        documents.append(tokenize(full_text))
    return documents


# --- Index Cache (V3) ---
# Inspired by GitNexus staleness management: fingerprint-based invalidation.
# Each domain's BM25 index is built once and reused until the CSV file changes.

_INDEX_CACHE: dict[str, dict] = {}


def _get_csv_fingerprint(domain: str) -> str:
    """Get a fingerprint (mtime + size) for a domain's CSV file.
    Returns empty string if file doesn't exist."""
    if domain not in EASESTART_CONFIG:
        return ""
    filepath = DATA_DIR / EASESTART_CONFIG[domain]["file"]
    try:
        stat = filepath.stat()
        return f"{stat.st_mtime_ns}:{stat.st_size}"
    except (OSError, FileNotFoundError):
        return ""


def _get_cached_index(domain: str) -> tuple:
    """Get cached (rows, documents, bm25) for a domain.
    Rebuilds if CSV file changed. Returns (rows, documents, bm25) or ([], [], None)."""
    fingerprint = _get_csv_fingerprint(domain)
    cached = _INDEX_CACHE.get(domain)

    if cached and cached["fingerprint"] == fingerprint and fingerprint:
        return cached["rows"], cached["documents"], cached["bm25"]

    # Cache miss or stale — rebuild
    rows, search_cols = load_csv(domain)
    if not rows:
        return [], [], None

    documents = rows_to_documents(rows, search_cols)
    bm25 = BM25()
    bm25.index(documents)

    _INDEX_CACHE[domain] = {
        "fingerprint": fingerprint,
        "rows": rows,
        "documents": documents,
        "bm25": bm25,
    }

    return rows, documents, bm25


def clear_search_cache(domain: str = "") -> None:
    """Clear the search index cache.
    If domain is specified, clear only that domain. Otherwise clear all."""
    if domain:
        _INDEX_CACHE.pop(domain, None)
    else:
        _INDEX_CACHE.clear()


# --- Domain Detection ---

def detect_domain(query: str) -> Optional[str]:
    """Auto-detect the best domain for a query based on keyword matching.
    
    Multi-word phrases score higher (2 points) than single words (1 point)
    to prefer specific domain matches over generic ones.
    """
    query_lower = query.lower()
    scores = {}

    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in query_lower:
                # Multi-word phrases are more specific → score higher
                word_count = len(kw.split())
                score += 2 if word_count >= 2 else 1
        if score > 0:
            scores[domain] = score

    if not scores:
        return None

    return max(scores, key=scores.get)


# --- Stage-Weighted Scoring ---

def _get_stage_weight(row_stage_val: str, target_stage: int) -> float:
    """Calculate stage-relevance weight for a row given the founder's stage."""
    if not row_stage_val or not row_stage_val.strip():
        return 1.0  # no stage info → neutral weight

    stage_str = str(row_stage_val).strip()

    # Determine the "center" of the row's stage range
    range_match = re.match(r"(\d+)-(\d+)", stage_str)
    if range_match:
        low, high = int(range_match.group(1)), int(range_match.group(2))
        row_center = (low + high) / 2
    elif stage_str.isdigit():
        row_center = int(stage_str)
    else:
        return 1.0  # unparseable → neutral

    distance = int(abs(row_center - target_stage))
    # Clamp to max distance key
    distance = min(distance, max(STAGE_RELEVANCE_WEIGHTS.keys()))
    return STAGE_RELEVANCE_WEIGHTS.get(distance, 0.7)


# --- Anti-Pattern Warnings ---

def _find_anti_pattern_warnings(
    query: str, domain: str, stage: Optional[int] = None
) -> Optional[str]:
    """Check playbook + reasoning CSVs for anti-pattern warnings relevant to the query."""
    query_tokens = set(tokenize(query))
    if not query_tokens:
        return None

    warnings = []

    # Check playbook anti-patterns (use cache instead of raw load_csv)
    playbook_rows, _, _ = _get_cached_index("playbook")
    for row in playbook_rows:
        dont = row.get("Dont", "")
        keywords = row.get("Keywords", "")
        rule_tokens = set(tokenize(keywords + " " + dont))
        overlap = query_tokens & rule_tokens
        if len(overlap) >= 2:  # at least 2 keyword matches
            if stage is not None:
                stage_val = row.get("Stage", "")
                if not _stage_matches(stage_val, stage):
                    continue
            severity = row.get("Severity", "")
            if severity in ("HIGH", "CRITICAL"):
                warnings.append(f"⚠️ {row.get('Dont', '')} (Source: {row.get('Source', 'Playbook')})")

    # Check reasoning anti-patterns (use cache instead of raw load_csv)
    reasoning_rows, _, _ = _get_cached_index("reasoning")
    for row in reasoning_rows:
        anti = row.get("Anti_Patterns", "")
        keywords = row.get("Keywords", "")
        rule_tokens = set(tokenize(keywords + " " + anti))
        overlap = query_tokens & rule_tokens
        if len(overlap) >= 2:
            if stage is not None:
                stage_val = row.get("Stage", "")
                if not _stage_matches(stage_val, stage):
                    continue
            for ap in anti.split("|"):
                ap = ap.strip()
                if ap:
                    warnings.append(f"⚠️ {ap}")

    if not warnings:
        return None

    # Deduplicate and limit
    seen = set()
    unique = []
    for w in warnings:
        if w not in seen:
            seen.add(w)
            unique.append(w)
    return " | ".join(unique[:3])  # max 3 warnings


# --- Context Decay ---

VALIDITY_PERIODS = {
    "90_days": 90,
    "180_days": 180,
    "365_days": 365,
}


def _check_context_decay(row: dict) -> Optional[str]:
    """Check if a knowledge row has expired based on Validity_Period + Last_Verified.
    Returns a warning string if stale, None if fresh or evergreen."""
    validity = row.get("Validity_Period", "").strip()
    last_verified = row.get("Last_Verified", "").strip()

    if not validity or validity == "evergreen" or not last_verified:
        return None

    days_valid = VALIDITY_PERIODS.get(validity)
    if days_valid is None:
        return None

    try:
        verified_date = date.fromisoformat(last_verified)
    except (ValueError, TypeError):
        return None

    expiry_date = verified_date + timedelta(days=days_valid)
    today = date.today()

    if today > expiry_date:
        days_overdue = (today - expiry_date).days
        decay_note = row.get("Decay_Note", "")
        note_str = f" — {decay_note}" if decay_note else ""
        return (
            f"⚠️ STALE ({days_overdue}d overdue): "
            f"Last verified {last_verified}, "
            f"validity {validity}{note_str}. Re-evaluate before acting."
        )

    return None


# --- Search ---

def search(
    query: str,
    domain: Optional[str] = None,
    top_k: int = 5,
    stage: Optional[int] = None,
    min_score: Optional[float] = None,
) -> list:
    """
    Search the EaseStart knowledge graph.

    Args:
        query: Natural language query
        domain: Specific domain to search (auto-detected if None)
        top_k: Number of results to return
        stage: Founder's current startup stage (0-6) — enables stage-weighted scoring
        min_score: Minimum BM25 score threshold (defaults to MIN_SCORE_THRESHOLD)

    Returns:
        List of dicts with score, row data, and optional _anti_pattern_warning
    """
    if min_score is None:
        min_score = MIN_SCORE_THRESHOLD

    # Guard: empty query
    if not query or not query.strip():
        return []

    if domain is None:
        domain = detect_domain(query)

    if domain is None:
        # Search all domains and merge
        all_results = []
        for d in EASESTART_CONFIG:
            results = search(query, domain=d, top_k=3, stage=stage, min_score=min_score)
            for r in results:
                r["_domain"] = d
            all_results.extend(results)
        all_results.sort(key=lambda x: x["_score"], reverse=True)
        return all_results[:top_k]

    # V3: Use cached index when available
    rows, documents, bm25 = _get_cached_index(domain)
    if not rows:
        return []

    # Small-corpus override: domains with ≤10 rows (e.g. stages=7) have very low
    # BM25 IDF because common terms appear in every doc. Lower threshold to avoid
    # silently returning 0 results for valid queries.
    if len(rows) <= 10 and min_score > 0.1:
        min_score = 0.1

    # Stage filter: keep matching rows but DON'T discard non-matching
    # When stage filtering is active, we need a fresh BM25 on the subset
    if stage is not None:
        filtered_indices = []
        for i, row in enumerate(rows):
            stage_val = row.get("Stage", row.get("Applicable_Stages", ""))
            # Fallback: if Stage column is non-numeric text (e.g. "Pre-Idea"),
            # use the "No" column which has the numeric stage index
            if stage_val and not stage_val.strip().replace("-", "").isdigit():
                stage_val = row.get("No", stage_val)
            if _stage_matches(stage_val, stage):
                filtered_indices.append(i)
        if filtered_indices and len(filtered_indices) < len(rows):
            rows = [rows[i] for i in filtered_indices]
            documents = [documents[i] for i in filtered_indices]
            # Rebuild BM25 for the stage-filtered subset
            bm25 = BM25()
            bm25.index(documents)

    query_tokens = tokenize(query)
    scores = bm25.score(query_tokens)

    results = []
    for i, score in enumerate(scores):
        if score <= 0:
            continue

        # Apply stage-weighted scoring
        if stage is not None:
            stage_val = rows[i].get("Stage", rows[i].get("Applicable_Stages", ""))
            # Fallback: use "No" column for non-numeric Stage values
            if stage_val and not stage_val.strip().replace("-", "").isdigit():
                stage_val = rows[i].get("No", stage_val)
            weight = _get_stage_weight(stage_val, stage)
            score *= weight

        # Apply min-score threshold
        if score < min_score:
            continue

        result = dict(rows[i])
        result["_score"] = round(score, 3)
        result["_domain"] = domain
        # Lucius L5: attach confidence level per result
        result["_confidence"] = _score_to_confidence(score)
        results.append(result)

    results.sort(key=lambda x: x["_score"], reverse=True)
    results = results[:top_k]

    # Attach anti-pattern warnings to the result set (not per-row)
    if results:
        warning = _find_anti_pattern_warnings(query, domain, stage)
        if warning:
            for r in results:
                r["_anti_pattern_warning"] = warning

    # Context Decay: flag results with expired Validity_Period
    for r in results:
        decay = _check_context_decay(r)
        if decay:
            r["_decay_warning"] = decay

    return results


def _score_to_confidence(score: float) -> str:
    """Map BM25 score to Lucius L5 confidence level."""
    if score >= CONFIDENCE_THRESHOLDS["HIGH"]:
        return "HIGH"
    elif score >= CONFIDENCE_THRESHOLDS["MEDIUM"]:
        return "MEDIUM"
    return "LOW"


def _stage_matches(stage_value: str, target_stage: int) -> bool:
    """Check if a stage value matches a target stage number."""
    if not stage_value:
        return True

    stage_str = str(stage_value).strip()

    # Exact match: "3"
    if stage_str.isdigit():
        return int(stage_str) == target_stage

    # Range match: "2-5" or "0-6"
    range_match = re.match(r"(\d+)-(\d+)", stage_str)
    if range_match:
        low, high = int(range_match.group(1)), int(range_match.group(2))
        return low <= target_stage <= high

    # Contains the number
    return str(target_stage) in stage_str


# --- Stats ---

def get_stats() -> dict:
    """Get statistics about the knowledge graph."""
    stats = {}
    for domain in EASESTART_CONFIG:
        rows, _ = load_csv(domain)
        stats[domain] = len(rows)
    stats["total"] = sum(stats.values())
    return stats


# --- Knowledge Relationships ---

RELATIONSHIPS_FILE = DATA_DIR / "relationships.csv"


def _load_relationships() -> list[dict]:
    """Load the knowledge relationship graph."""
    if not RELATIONSHIPS_FILE.exists():
        return []
    try:
        with open(RELATIONSHIPS_FILE, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except (csv.Error, UnicodeDecodeError, IOError):
        return []


def get_related(
    domain: str,
    key: str = "",
    relation_type: Optional[str] = None,
) -> list[dict]:
    """
    Get related knowledge from the relationship graph.

    Args:
        domain: Source domain (e.g. "pricing")
        key: Optional source key to match (e.g. "freemium")
        relation_type: Filter by relation type (REQUIRES, WARNS_AGAINST, etc.)

    Returns:
        List of relationship dicts with source, target, relation, weight, context.
    """
    relationships = _load_relationships()
    results = []

    key_lower = key.lower() if key else ""

    for rel in relationships:
        source_domain = rel.get("Source_Domain", "").strip()
        target_domain = rel.get("Target_Domain", "").strip()
        source_key = rel.get("Source_Key", "").strip().lower()
        rel_type = rel.get("Relation_Type", "").strip()

        # Match source or target domain
        is_source = source_domain == domain
        is_target = target_domain == domain
        if not is_source and not is_target:
            continue

        # Filter by key if provided
        if key_lower:
            if is_source and key_lower not in source_key:
                # Also check if key appears in target
                target_key = rel.get("Target_Key", "").strip().lower()
                if not is_target or key_lower not in target_key:
                    continue
            elif is_target:
                target_key = rel.get("Target_Key", "").strip().lower()
                if key_lower not in target_key and key_lower not in source_key:
                    continue

        # Filter by relation type if provided
        if relation_type and rel_type != relation_type:
            continue

        weight = 0.5
        try:
            weight = float(rel.get("Weight", "0.5"))
        except ValueError:
            pass

        results.append({
            "source_domain": source_domain,
            "source_key": rel.get("Source_Key", ""),
            "relation": rel_type,
            "target_domain": target_domain,
            "target_key": rel.get("Target_Key", ""),
            "weight": weight,
            "context": rel.get("Context", ""),
        })

    # Sort by weight descending
    results.sort(key=lambda x: x["weight"], reverse=True)
    return results


def search_with_relations(
    query: str,
    domain: Optional[str] = None,
    top_k: int = 5,
    stage: Optional[int] = None,
) -> dict:
    """
    Search + automatically attach related knowledge and warnings.

    Returns:
        Dict with "results", "related", and "warnings" keys.
    """
    results = search(query, domain=domain, top_k=top_k, stage=stage)

    # Collect related knowledge from relationship graph
    related = []
    warnings = []
    seen_contexts = set()

    # Detect domain for relationship lookup
    search_domain = domain or detect_domain(query)

    if search_domain:
        # Get all relationships for this domain
        domain_rels = get_related(search_domain)
        for rel in domain_rels[:10]:
            ctx = rel.get("context", "")
            if ctx in seen_contexts:
                continue
            seen_contexts.add(ctx)

            if rel["relation"] == "WARNS_AGAINST":
                warnings.append({
                    "warning": ctx,
                    "source": f"{rel['source_domain']}/{rel['source_key']}",
                    "weight": rel["weight"],
                })
            else:
                related.append({
                    "relation": rel["relation"],
                    "from": f"{rel['source_domain']}/{rel['source_key']}",
                    "to": f"{rel['target_domain']}/{rel['target_key']}",
                    "context": ctx,
                    "weight": rel["weight"],
                })

    return {
        "results": results,
        "related": related[:5],
        "warnings": warnings[:3],
    }


# --- Hybrid Search (optional, zero-dep fallback) ---

def search_hybrid(
    query: str,
    domain: Optional[str] = None,
    top_k: int = 5,
    stage: Optional[int] = None,
) -> list:
    """
    Hybrid search: embeddings + BM25 when ChromaDB is available.
    Falls back to pure BM25 when ChromaDB is not installed.

    This preserves core.py's zero-dependency guarantee — chromadb
    is only imported if available.
    """
    try:
        from embed import _check_deps, _get_collection, _get_model, _merge_hybrid
        if not _check_deps():
            raise ImportError("ChromaDB not available")

        _, collection = _get_collection()
        if collection.count() == 0:
            raise ImportError("Index empty")

        model = _get_model()
        query_embedding = model.encode([query]).tolist()

        # Semantic search
        results_raw = collection.query(
            query_embeddings=query_embedding,
            n_results=top_k * 2,
            include=["documents", "metadatas", "distances"],
        )

        semantic_results = []
        for doc, meta, distance in zip(
            results_raw["documents"][0],
            results_raw["metadatas"][0],
            results_raw["distances"][0],
        ):
            similarity = 1 - (distance / 2)
            semantic_results.append({
                "text": doc[:200],
                "domain": meta["domain"],
                "stage": meta["stage"],
                "similarity": round(similarity, 3),
            })

        # BM25 results
        bm25_results = search(query, domain=domain, top_k=top_k, stage=stage)

        # Merge
        return _merge_hybrid(bm25_results, semantic_results, top_k)

    except (ImportError, Exception):
        # Graceful fallback to BM25
        return search(query, domain=domain, top_k=top_k, stage=stage)

