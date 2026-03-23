#!/usr/bin/env python3
"""
Generate HVS-style Validation Report.

Creates a single-page HTML report after idea validation succeeds.
Hybrid approach: auto-generates skeleton from KB data + accepts
optional enrichment JSON for AI-synthesized sections.

Usage:
    python3 scripts/generate_validation_report.py "Your idea"
    python3 scripts/generate_validation_report.py "Your idea" --industry saas --open
    python3 scripts/generate_validation_report.py "Your idea" --data enrichment.json --open
"""
import sys, os, argparse, json, shutil, textwrap, unicodedata, re
import html as html_module
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.core import search
from scripts.validate_idea import (
    detect_industry, detect_stage_from_idea, calculate_scores,
    score_label, STAGE_NAMES,
)

e = html_module.escape
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "output")


# ─── Auto-Research ───────────────────────────────────────────────────

def _auto_research(idea: str, industry: str, stage: int) -> dict:
    """Deep multi-domain KB search to fill report sections.
    Returns enrichment-style dict with researched data."""
    print("  🔬 Auto-researching report sections...")
    data = {}

    # ── Reframe research ──
    print("    → Reframe: benchmarks, frameworks, cross-domain...")
    benchmarks = []
    for query in [f"case study {industry} bootstrapped grew",
                  f"case study startup success lesson",
                  f"benchmark best in class {industry}"]:
        for c in search(query, top_k=5, stage=stage):
            company = c.get("Company", "")
            lesson = (c.get("Lesson", "") or c.get("Key_Lesson", "") or
                      c.get("Stage_1_Insight", "") or c.get("Description", "") or
                      c.get("Giantiny_Alignment", ""))
            if company and lesson and not any(b["name"] == company for b in benchmarks):
                benchmarks.append({"name": company, "location": "", "what": str(lesson)[:140]})
            if len(benchmarks) >= 5:
                break

    frameworks = []
    for query in ["lean canvas customer discovery framework",
                  "jobs-to-be-done jtbd framework",
                  f"validate {industry} framework methodology"]:
        for fw in search(query, top_k=3, stage=stage):
            name = fw.get("Name", fw.get("Framework", ""))
            desc = (fw.get("Description", "") or fw.get("Steps", "") or
                    fw.get("Key_Concepts", ""))
            if name and desc and not any(f["name"] == name for f in frameworks):
                frameworks.append({"name": name, "applied": str(desc)[:140]})
            if len(frameworks) >= 4:
                break

    cross_domain = []
    for query in [f"counter-positioning {industry}",
                  f"analogy cross industry insight",
                  f"what can {industry} learn from"]:
        for cd in search(query, top_k=3, stage=stage):
            src = cd.get("Name", cd.get("Industry", cd.get("Concept", "")))
            insight = (cd.get("Description", "") or cd.get("Context", "") or
                       cd.get("Counter_Position_Examples", ""))
            if src and insight and not any(c["from"] == str(src)[:30] for c in cross_domain):
                cross_domain.append({"from": str(src)[:30], "insight": str(insight)[:140]})
            if len(cross_domain) >= 3:
                break

    data["reframe"] = {
        "benchmarks": benchmarks if benchmarks else None,
        "frameworks": frameworks if frameworks else None,
        "cross_domain": cross_domain if cross_domain else None,
    }

    # ── DOV research ──
    print("    → DOV: problem anatomy, anti-patterns...")
    anti_patterns = []
    for query in [f"common mistake {industry} founders",
                  "common mistake don't avoid startup",
                  f"anti-pattern {industry} stage {stage}"]:
        for ap in search(query, top_k=3, stage=stage):
            rule = ap.get("Rule", ap.get("Dont", ap.get("Anti_Pattern", "")))
            if rule and rule not in [a.get("rule") for a in anti_patterns]:
                anti_patterns.append({"rule": str(rule)[:100]})
            if len(anti_patterns) >= 5:
                break
    data["dov"] = {"anti_patterns": anti_patterns}

    # ── Market research ──
    print("    → Market: TAM, competitors, timing...")
    tam = []
    for query in [f"{industry} market size tam",
                  f"{industry} industry growth rate"]:
        for ind in search(query, top_k=3, stage=stage):
            ind_name = ind.get("Industry", industry)
            tam_val = ind.get("TAM", "")
            growth = ind.get("GrowthRate", ind.get("Revenue_Model", ""))
            if tam_val or growth:
                entry = {"level": "TAM", "market": str(ind_name), "size": str(tam_val or "Research needed")}
                if growth:
                    entry["growth"] = str(growth)[:60]
                if not any(t["market"] == entry["market"] for t in tam):
                    tam.append(entry)
            if len(tam) >= 3:
                break

    timing = []
    for query in [f"{industry} market trends why now",
                  f"technology enabler {industry}",
                  f"behavior shift {industry} consumer"]:
        for t in search(query, top_k=3, stage=stage):
            signal = (t.get("Signal", "") or t.get("Name", "") or
                      t.get("Concept", "") or t.get("Tactic", ""))
            evidence = (t.get("Description", "") or t.get("Context", "") or
                        t.get("Details", ""))
            if signal and evidence and not any(x["driver"] == str(signal)[:30] for x in timing):
                timing.append({"driver": str(signal)[:30], "evidence": str(evidence)[:120]})
            if len(timing) >= 4:
                break

    data["market"] = {
        "tam": tam if tam else None,
        "timing": timing if timing else None,
    }

    # ── Offer research ──
    print("    → Offer: pricing strategies...")
    pricing = []
    for query in [f"pricing {industry} strategy",
                  f"freemium subscription {industry}",
                  "pricing model saas b2c"]:
        for p in search(query, top_k=3, stage=stage):
            strat = p.get("Strategy", p.get("Name", ""))
            desc = (p.get("Description", "") or p.get("Best_For", "") or
                    p.get("Type", ""))
            if strat and desc:
                pricing.append({
                    "tier": str(strat)[:30],
                    "target": str(p.get("Best_For", "General"))[:40],
                    "includes": str(desc)[:80],
                    "price": "Research needed",
                })
            if len(pricing) >= 3:
                break
    data["offer"] = {"pricing": pricing if pricing else None}

    # ── Digital validation (optional — try, don't fail) ──
    try:
        from scripts.digital_validate import search_reddit, search_hn, analyze_pain, score_validation, DEFAULT_SUBREDDITS
        print("    → Digital validation: Reddit + HN...")
        keywords = idea.lower().split()[:4]
        query_str = " ".join(keywords)

        all_posts = []
        reddit = search_reddit(query_str, DEFAULT_SUBREDDITS[:3], limit=15)
        all_posts.extend(reddit)
        hn = search_hn(query_str, limit=15)
        all_posts.extend(hn)

        if all_posts:
            analysis = analyze_pain(all_posts)
            validation = score_validation(analysis)
            data["digital"] = {
                "total_posts": analysis["total_posts"],
                "pain_count": analysis["pain_count"],
                "pain_pct": round(analysis["pain_count"] / max(analysis["total_posts"], 1) * 100),
                "avg_engagement": round(analysis["avg_engagement"], 1),
                "validation_score": validation["score"],
                "validation_level": validation["level"],
                "top_pain_signals": list(analysis["top_pain_signals"].keys())[:5],
                "top_quotes": [p["title"][:80] for p in analysis["pain_posts"][:3]],
            }
            print(f"      ✓ {analysis['total_posts']} posts, {analysis['pain_count']} pain signals")
    except (ImportError, Exception) as ex:
        print(f"    → Digital validation skipped ({ex})")

    # Remove None values (sections with no data found)
    for section in list(data.keys()):
        if isinstance(data[section], dict):
            data[section] = {k: v for k, v in data[section].items() if v is not None}

    print("  ✅ Auto-research complete\n")
    return data


def _merge_enrichment(base: dict, research: dict, user: dict) -> dict:
    """Merge: user enrichment > auto-research > empty. User data always wins."""
    merged = {}
    for key in set(list(research.keys()) + list(user.keys())):
        r_val = research.get(key, {})
        u_val = user.get(key, {})
        if isinstance(r_val, dict) and isinstance(u_val, dict):
            section = dict(r_val)
            section.update({k: v for k, v in u_val.items() if v})
            merged[key] = section
        else:
            merged[key] = u_val if u_val else r_val
    return merged


# ─── Data Collection ─────────────────────────────────────────────────

def collect_report_data(idea: str, industry: str = None,
                        enrichment: dict = None,
                        skip_research: bool = False) -> dict:
    """Collect all data for the validation report."""
    if not industry:
        industry = detect_industry(idea)
    stage = detect_stage_from_idea(idea)
    user_enr = enrichment or {}

    # Auto-research: deep KB search to fill gaps
    if skip_research:
        print("  ⏩ Skipping auto-research (--skip-research)")
        enr = user_enr
    else:
        research = _auto_research(idea, industry, stage)
        enr = _merge_enrichment({}, research, user_enr)

    # Scores from validate_idea
    scores = calculate_scores(idea, industry, stage)
    total = sum(scores.values())

    if total >= 80:
        cls_label, cls_color = "VALIDATED TO START", "#22c55e"
    elif total >= 60:
        cls_label, cls_color = "READY WITH CAUTION", "#eab308"
    elif total >= 40:
        cls_label, cls_color = "NEEDS ITERATION", "#f97316"
    else:
        cls_label, cls_color = "RED FLAG", "#ef4444"

    short = idea.split(" for ")[0] if " for " in idea else idea[:50]
    target = idea.split(" for ")[1].strip() if " for " in idea else "target users"
    ind = industry.replace("_", " ").title()

    data = {
        "idea": idea,
        "industry": industry,
        "industry_display": ind,
        "stage": stage,
        "stage_name": STAGE_NAMES.get(stage, "?"),
        "scores": scores,
        "total": total,
        "cls_label": cls_label,
        "cls_color": cls_color,
        "short": short,
        "target": target,
        "now": datetime.now().strftime("%Y-%m-%d"),
        "verdict_label": score_label(total),
        "title": enr.get("title", short),
        "subtitle": enr.get("subtitle", idea),
    }

    # ── Reframe ──
    data["reframe"] = _collect_reframe(idea, industry, stage, enr)

    # ── DOV ──
    data["dov"] = _collect_dov(idea, industry, stage, scores, total, enr)

    # ── Market ──
    data["market"] = _collect_market(idea, industry, stage, enr)

    # ── Offer ──
    data["offer"] = _collect_offer(idea, industry, stage, enr)

    # ── Roadmap ──
    data["roadmap"] = _collect_roadmap(idea, industry, stage, enr)

    # ── Digital validation (from auto-research) ──
    if enr.get("digital"):
        data["digital"] = enr["digital"]

    return data


def _collect_reframe(idea, industry, stage, enr):
    """Collect Reframe section data."""
    rf = enr.get("reframe", {})
    short = idea.split(" for ")[0] if " for " in idea else idea[:50]

    # Auto-generate from KB if not enriched
    benchmarks = rf.get("benchmarks", [])
    if not benchmarks:
        cases = search(f"case study {industry} bootstrapped grew", stage=stage)
        for c in cases[:3]:
            company = c.get("Company", "")
            lesson = c.get("Lesson", "") or c.get("Description", "") or c.get("Context", "") or c.get("Details", "")
            if company and lesson:
                benchmarks.append({"name": company, "location": "", "what": str(lesson)[:120]})

    frameworks = rf.get("frameworks", [])
    if not frameworks:
        fw_results = search("lean canvas customer discovery framework", stage=stage)
        for fw in fw_results[:3]:
            name = fw.get("Name", fw.get("Framework", ""))
            desc = fw.get("Description", fw.get("Steps", ""))
            if name:
                frameworks.append({"name": name, "applied": str(desc)[:120]})

    cross_domain = rf.get("cross_domain", [])
    if not cross_domain:
        cd_results = search(f"cross domain insight analogy {industry}", stage=stage)
        for cd in cd_results[:3]:
            src = cd.get("Name", cd.get("Industry", ""))
            insight = cd.get("Description", cd.get("Context", ""))
            if src and insight:
                cross_domain.append({"from": str(src)[:30], "insight": str(insight)[:120]})

    tradeoffs = rf.get("tradeoffs", [])
    approaches = rf.get("approaches", [])
    if not approaches:
        approaches = [
            {"label": "Recommend", "name": "Narrowest Wedge",
             "desc": f"Manual MVP for {short}. Minimum scope, maximum learning. Effort: Low. Risk: Low."},
            {"label": "Ambitious", "name": "Full Product",
             "desc": f"Web app + subscription tiers + automation. Effort: Medium. Risk: Medium."},
            {"label": "10-Star", "name": "Platform",
             "desc": f"Full platform with AI, marketplace, multi-market. Effort: High. Risk: High."},
        ]

    return {
        "founder_says": rf.get("founder_says", f"Tôi muốn xây dựng {short}"),
        "agent_hears": rf.get("agent_hears", f"Target users đang gặp vấn đề mà chưa có ai giải quyết đúng cách"),
        "root_problem": rf.get("root_problem", ""),
        "benchmarks": benchmarks,
        "frameworks": frameworks,
        "cross_domain": cross_domain,
        "tradeoffs": tradeoffs,
        "approaches": approaches,
    }


def _collect_dov(idea, industry, stage, scores, total, enr):
    """Collect DOV Validation section data."""
    dov = enr.get("dov", {})

    # DOV-specific scores (use enrichment or derive from KB scores)
    dov_scores = dov.get("scores", {
        "Founder-Problem Fit": scores.get("Problem Clarity", 15),
        "Core Difficulty": scores.get("Competitive Edge", 14),
        "Market Friction": scores.get("Market Opportunity", 14),
        "Urgency & Reality": scores.get("Validation Evidence", 16),
        "Value Potential": scores.get("Execution Readiness", 14),
    })

    # Problem anatomy
    monkey = dov.get("monkey", {})
    weakchain = dov.get("weakchain", {})
    do_nothing = dov.get("do_nothing", {})

    return {
        "jtbd": dov.get("jtbd", ""),
        "founder_fit": {
            "specific_knowledge": dov.get("founder_fit", {}).get("specific_knowledge", 7),
            "domain_expertise": dov.get("founder_fit", {}).get("domain_expertise", 6),
            "network": dov.get("founder_fit", {}).get("network", 5),
        },
        "monkey": monkey,
        "weakchain": weakchain,
        "do_nothing": do_nothing,
        "impact": dov.get("impact", {}),
        "scores": dov_scores,
        "total": sum(dov_scores.values()) if dov_scores else total,
    }


def _collect_market(idea, industry, stage, enr):
    """Collect Market Intel section data."""
    mkt = enr.get("market", {})

    # TAM data
    tam = mkt.get("tam", [])
    if not tam:
        ind_results = search(f"{industry} market size", stage=stage)
        if ind_results:
            top = ind_results[0]
            tam.append({
                "level": "TAM",
                "market": top.get("Industry", industry),
                "size": top.get("TAM", "?"),
            })

    # Competitors
    competitors = mkt.get("competitors", [])

    # Timing
    timing = mkt.get("timing", [])
    if not timing:
        timing_results = search(f"{industry} market trends why now", stage=stage)
        for t in timing_results[:3]:
            signal = t.get("Signal", t.get("Name", ""))
            evidence = t.get("Description", t.get("Context", ""))
            if signal:
                timing.append({"driver": str(signal)[:30], "evidence": str(evidence)[:100]})

    return {
        "tam": tam,
        "competitors": competitors,
        "timing": timing,
    }


def _collect_offer(idea, industry, stage, enr):
    """Collect Grand Slam Offer section data."""
    offer = enr.get("offer", {})

    # Pricing from KB
    pricing_tiers = offer.get("pricing", [])
    if not pricing_tiers:
        pricing_results = search(f"pricing {industry} strategy", stage=stage)
        if pricing_results:
            strat = pricing_results[0].get("Strategy", "")
            if strat:
                pricing_tiers.append({
                    "tier": "Suggested",
                    "target": "Primary audience",
                    "includes": str(strat)[:80],
                    "price": "TBD",
                })

    return {
        "value_equation": offer.get("value_equation", ""),
        "problems_solutions": offer.get("problems_solutions", []),
        "offer_name": offer.get("offer_name", ""),
        "offer_tagline": offer.get("offer_tagline", ""),
        "pricing": pricing_tiers,
        "guarantee": offer.get("guarantee", ""),
    }


def _collect_roadmap(idea, industry, stage, enr):
    """Collect Roadmap section data."""
    rm = enr.get("roadmap", {})
    phases = rm.get("phases", [])
    if not phases:
        phases = [{
            "name": "Phase 1: Validate & Launch",
            "items": [
                {"time": "Week 1-2", "action": "Customer interviews (5-10 Mom Test conversations)"},
                {"time": "Week 2-3", "action": "Build MVP — core feature only"},
                {"time": "Week 3-4", "action": "Ship to first 10 users, collect feedback"},
                {"time": "Month 2", "action": "Iterate based on data, set pricing"},
                {"time": "Month 3", "action": "Launch to wider audience, measure retention"},
            ],
        }]
    return {"phases": phases}


# ─── HTML Builders ───────────────────────────────────────────────────

def _build_sidebar(data: dict) -> str:
    """Build sidebar navigation."""
    sections = [
        ("reframe", "0", "Reframe"),
        ("dov", "1", "DOV Validation"),
        ("market", "2", "Market Intel"),
        ("offer", "3", "Grand Slam Offer"),
        ("roadmap", "4", "Roadmap"),
    ]
    links = ""
    for href, num, label in sections:
        links += f'    <a href="#{href}" class="nav-link"><span class="nav-stage-num">{num}</span> {label}</a>\n'

    title = e(data.get("title", data["short"]))
    return f'''<nav class="sidebar">
    <div class="sidebar-brand">
      <h2>{title}</h2>
      <p>Founder's Intel Memo</p>
    </div>
    <div class="nav-group">
      <div class="nav-label">Báo cáo</div>
{links}    </div>
    <div class="nav-group">
      <div class="nav-label">Tham khảo</div>
      <a href="#scorecard" class="nav-link">Scorecard</a>
      <a href="#sources" class="nav-link">Nguồn dữ liệu</a>
    </div>
  </nav>'''


def _build_hero(data: dict) -> str:
    """Build hero section with stats."""
    title = e(data.get("title", data["short"]))
    subtitle = e(data.get("subtitle", data["idea"]))
    total = data["total"]
    cls_label = data["cls_label"]
    industry_display = e(data["industry_display"])
    stage = data["stage"]
    stage_name = e(data["stage_name"])

    # Dynamic stats from enrichment or defaults
    stats = [
        (str(total), "DOV Score"),
        (industry_display, "Industry"),
        (str(stage), "Stage"),
        (stage_name, "Phase"),
        (data["now"], "Date"),
    ]
    stats_html = ""
    for val, label in stats:
        stats_html += f'<div class="stat"><div class="stat-val">{val}</div><div class="stat-label">{label}</div></div>\n'

    verdict_text = data.get("verdict_text", "")
    if not verdict_text:
        if total >= 70:
            verdict_text = f"Idea scores {total}/100 — strong signal. Problem is real, market exists. Focus on execution and customer validation."
        elif total >= 50:
            verdict_text = f"Idea scores {total}/100 — promising but needs more validation. Key areas need strengthening before committing resources."
        else:
            verdict_text = f"Idea scores {total}/100 — significant gaps identified. Consider pivoting the positioning or finding a sharper pain point."

    return f'''<span class="tag tag-stage">EASESTART VALIDATION</span>
    <h1>{title}</h1>
    <p class="subtitle">{subtitle}</p>

    <div class="stats">
      {stats_html}
    </div>

    <div class="classification"><span class="cls-dot"></span> {e(cls_label)}</div>

    <div class="verdict">
      <strong>Kết luận:</strong> {e(verdict_text)}
    </div>'''


def _build_reframe(data: dict) -> str:
    """Build Reframe section."""
    rf = data["reframe"]
    parts = []

    # Pain vs Feature compare
    founder_says = e(rf["founder_says"])
    agent_hears = e(rf["agent_hears"])
    parts.append(f'''<h3>Pain, không phải Feature</h3>
    <div class="compare-grid">
      <div class="compare-col">
        <h4 style="color:var(--slate)">FOUNDER NÓI</h4>
        <p style="font-size:17px">"{founder_says}"</p>
      </div>
      <div class="compare-col">
        <h4>AGENT NGHE</h4>
        <p style="font-size:17px">"{agent_hears}"</p>
      </div>
    </div>''')

    # Root Problem
    root = rf.get("root_problem", "")
    if root:
        parts.append(f'''<div class="why">
      <div class="why-label">Root Problem (First Principles)</div>
      <p style="font-size:17px;margin:0">{e(root)}</p>
    </div>''')

    # Benchmarks
    if rf["benchmarks"]:
        rows = ""
        for b in rf["benchmarks"]:
            name = e(b.get("name", ""))
            loc = b.get("location", "")
            loc_str = f" ({e(loc)})" if loc else ""
            what = e(b.get("what", ""))
            rows += f'<tr><td><strong>{name}</strong>{loc_str}</td><td>{what}</td></tr>\n'
        parts.append(f'''<h3><i class="ph ph-trophy"></i> Benchmark Đỉnh</h3>
    <table>
      <tr><th>Best-in-class</th><th>Điều gì làm họ xuất sắc</th></tr>
      {rows}
    </table>''')

    # Frameworks
    if rf["frameworks"]:
        rows = ""
        for fw in rf["frameworks"]:
            rows += f'<tr><td><strong>{e(fw.get("name", ""))}</strong></td><td>{e(fw.get("applied", ""))}</td></tr>\n'
        parts.append(f'''<h3><i class="ph ph-tree-structure"></i> Framework áp dụng</h3>
    <table>
      <tr><th>Framework</th><th>Áp dụng</th></tr>
      {rows}
    </table>''')

    # Cross-domain
    if rf["cross_domain"]:
        rows = ""
        for cd in rf["cross_domain"]:
            rows += f'<tr><td><strong>{e(cd.get("from", ""))}</strong></td><td>{e(cd.get("insight", ""))}</td></tr>\n'
        parts.append(f'''<h3><i class="ph ph-planet"></i> Cross-Domain Insight</h3>
    <table>
      <tr><th>Ngành gốc</th><th>Insight chuyển sang</th></tr>
      {rows}
    </table>''')

    # Trade-offs
    if rf["tradeoffs"]:
        rows = ""
        for t in rf["tradeoffs"]:
            rows += f'<tr><td>{e(t.get("choose", ""))}</td><td>{e(t.get("sacrifice", ""))}</td><td>{e(t.get("why", ""))}</td></tr>\n'
        parts.append(f'''<h3><i class="ph ph-scales"></i> Trade-offs</h3>
    <table>
      <tr><th>Chọn</th><th>Hy sinh</th><th>Vì sao</th></tr>
      {rows}
    </table>''')

    # 3 Approaches
    if rf["approaches"]:
        cards = ""
        for i, app in enumerate(rf["approaches"]):
            style = ' style="grid-column:span 2;border:3px solid var(--black)"' if i == 0 else ""
            label = e(app.get("label", ""))
            name = e(app.get("name", ""))
            desc = e(app.get("desc", ""))
            cards += f'''<a class="card"{style}>
        <div class="card-tag">{label}</div>
        <h3>{name}</h3>
        <p>{desc}</p>
      </a>\n'''
        parts.append(f'''<h3><i class="ph ph-path"></i> 3 Approaches</h3>
    <div class="grid">
      {cards}
    </div>''')

    return "\n\n".join(parts)


def _build_dov(data: dict) -> str:
    """Build DOV Validation section."""
    dov = data["dov"]
    parts = []

    # Founder-Opportunity Fit bars
    ff = dov["founder_fit"]
    bars = ""
    for label, key in [("Specific Knowledge", "specific_knowledge"),
                        ("Domain Expertise", "domain_expertise"),
                        ("Network", "network")]:
        val = ff.get(key, 5)
        pct = val * 10
        bars += f'<div class="metric-bar"><span class="metric-label">{label}</span><div class="metric-track"><div class="metric-fill" style="width:{pct}%"></div></div><span class="metric-val">{val}/10</span></div>\n'
    parts.append(f'<h3>Founder-Opportunity Fit</h3>\n{bars}')

    # JTBD
    jtbd = dov.get("jtbd", "")
    if jtbd:
        parts.append(f'''<div class="why" style="margin-top:20px">
      <div class="why-label">JTBD sơ khởi</div>
      <p style="font-size:17px;margin:0">{e(jtbd)}</p>
    </div>''')

    # Problem Anatomy
    parts.append('<h3>Problem Anatomy</h3>')
    for key, icon, default_title in [
        ("monkey", "ph-warning", "MONKEY PROBLEM — Biến số quyết định"),
        ("weakchain", "ph-link-break", "WEAKCHAIN — Điểm gãy quy trình"),
        ("do_nothing", "ph-prohibit", "DO-NOTHING — Kịch bản trì trệ"),
    ]:
        item = dov.get(key, {})
        title = item.get("title", default_title)
        desc = item.get("desc", "")
        if desc:
            parts.append(f'''<div class="pain-card">
      <div class="pain-title"><i class="ph {icon}"></i> {e(title)}</div>
      <div class="pain-desc">{e(desc)}</div>
    </div>''')

    # Impact 4D
    impact = dov.get("impact", {})
    if impact:
        dims = ""
        for label in ["Functional", "Emotional", "Breakthrough UX", "Billion+ Market"]:
            val = impact.get(label, impact.get(label.lower(), 7))
            pct = val * 10
            dims += f'<div class="metric-bar"><span class="metric-label">{label}</span><div class="metric-track"><div class="metric-fill" style="width:{pct}%"></div></div><span class="metric-val">{val}/10</span></div>\n'
        parts.append(f'<h3>Impact 4 chiều</h3>\n{dims}')

    # DOV Scorecard
    dov_scores = dov.get("scores", {})
    if dov_scores:
        dov_total = dov.get("total", sum(dov_scores.values()))
        rows = ""
        for dim, score in dov_scores.items():
            pct = score / 20 * 100
            rows += f'''<div class="score-row"><span class="score-label">{e(dim)}</span><div class="score-track"><div class="score-fill" style="width:{pct}%"></div></div><span class="score-val">{score}/20</span></div>\n'''

        total_pct = dov_total
        verdict = "Idea đủ mạnh để bắt đầu." if dov_total >= 70 else "Cần cải thiện trước khi tiến hành."
        parts.append(f'''<div class="scorecard" id="scorecard">
      <div class="scorecard-title">DOV Scorecard</div>
      {rows}
      <div class="score-total"><span class="score-label">Total</span><div class="score-track"><div class="score-fill" style="width:{total_pct}%"></div></div><span class="score-val">{dov_total}/100</span></div>
      <div class="score-verdict">{verdict}</div>
    </div>''')

    # Digital validation (if available)
    digital = data.get("digital", {})
    if digital:
        dv_score = digital.get("validation_score", 0)
        dv_level = digital.get("validation_level", "?")
        dv_posts = digital.get("total_posts", 0)
        dv_pain = digital.get("pain_count", 0)
        parts.append(f'''<h3><i class="ph ph-magnifying-glass"></i> Digital Validation</h3>
    <p class="section-source">Reddit + Hacker News — real founder pain signals</p>
    <div class="stats" style="margin:12px 0">
      <div class="stat"><div class="stat-val">{dv_score}/100</div><div class="stat-label">Pain Score</div></div>
      <div class="stat"><div class="stat-val">{dv_posts}</div><div class="stat-label">Posts</div></div>
      <div class="stat"><div class="stat-val">{dv_pain}</div><div class="stat-label">Pain Signals</div></div>
      <div class="stat"><div class="stat-val">{e(dv_level)}</div><div class="stat-label">Level</div></div>
    </div>''')
        top_signals = digital.get("top_pain_signals", [])
        if top_signals:
            signal_html = ", ".join(f'<code>{e(s)}</code>' for s in top_signals[:5])
            parts.append(f'<p><strong>Top pain keywords:</strong> {signal_html}</p>')
        quotes = digital.get("top_quotes", [])
        if quotes:
            for q in quotes[:3]:
                parts.append(f'<div class="pain-card"><div class="pain-desc">"{e(q)}"</div></div>')

    return "\n\n".join(parts)


def _build_market(data: dict) -> str:
    """Build Market Intel section."""
    mkt = data["market"]
    parts = []

    # TAM/SAM/SOM
    if mkt["tam"]:
        rows = ""
        for t in mkt["tam"]:
            rows += f'<tr><td><strong>{e(t.get("level", ""))}</strong></td><td>{e(t.get("market", ""))}</td><td><strong>{e(t.get("size", ""))}</strong></td></tr>\n'
        parts.append(f'''<h3>Quy mô thị trường</h3>
    <table>
      <tr><th>Level</th><th>Thị trường</th><th>Quy mô</th></tr>
      {rows}
    </table>''')

    # Counter-positioning / Competitors
    if mkt["competitors"]:
        rows = ""
        for c in mkt["competitors"]:
            rows += f'<tr><td><strong>{e(c.get("name", ""))}</strong></td><td>{e(c.get("weakness", ""))}</td><td>{e(c.get("exploit", ""))}</td></tr>\n'
        parts.append(f'''<h3><i class="ph ph-shield-warning"></i> Counter-positioning</h3>
    <table>
      <tr><th>Đối thủ</th><th>Sơ hở cấu trúc</th><th>Exploit</th></tr>
      {rows}
    </table>''')

    # Market Timing
    if mkt["timing"]:
        rows = ""
        for t in mkt["timing"]:
            rows += f'<tr><td><strong>{e(t.get("driver", ""))}</strong></td><td>{e(t.get("evidence", ""))}</td></tr>\n'
        parts.append(f'''<h3><i class="ph ph-clock-countdown"></i> Market Timing — Tại sao BÂY GIỜ?</h3>
    <table>
      <tr><th>Cú hích</th><th>Bằng chứng</th></tr>
      {rows}
    </table>''')

    if not parts:
        parts.append('<div class="insight">Cần research thêm market data. Chạy /deep-research để thu thập thông tin thị trường.</div>')

    return "\n\n".join(parts)


def _build_offer(data: dict) -> str:
    """Build Grand Slam Offer section."""
    offer = data["offer"]
    parts = []

    # Value equation
    veq = offer.get("value_equation", "")
    if veq:
        parts.append(f'''<div class="why">
      <div class="why-label">Phương trình giá trị</div>
      <p style="font-size:17px;margin:0">{e(veq)}</p>
    </div>''')

    # Problem → Solution table
    ps = offer.get("problems_solutions", [])
    if ps:
        rows = ""
        for item in ps:
            rows += f'<tr><td>"{e(item.get("problem", ""))}"</td><td>{e(item.get("solution", ""))}</td></tr>\n'
        parts.append(f'''<h3>Problem → Solution</h3>
    <table>
      <tr><th>Vấn đề khách hàng</th><th>Giải pháp</th></tr>
      {rows}
    </table>''')

    # Offer name
    offer_name = offer.get("offer_name", "")
    offer_tagline = offer.get("offer_tagline", "")
    if offer_name:
        parts.append(f'''<h3><i class="ph ph-tag"></i> Offer Name</h3>
    <div class="why">
      <div class="why-label">Recommend</div>
      <p style="font-size:22px;margin:0;font-weight:700">{e(offer_name)}</p>
      {f'<p style="font-size:17px;margin:4px 0 0;color:var(--slate)">{e(offer_tagline)}</p>' if offer_tagline else ''}
    </div>''')

    # Pricing tiers
    if offer["pricing"]:
        rows = ""
        for p in offer["pricing"]:
            rows += f'<tr><td><strong>{e(p.get("tier", ""))}</strong></td><td>{e(p.get("target", ""))}</td><td>{e(p.get("includes", ""))}</td><td>{e(p.get("price", ""))}</td></tr>\n'
        parts.append(f'''<h3><i class="ph ph-currency-circle-dollar"></i> Pricing</h3>
    <table>
      <tr><th>Gói</th><th>Đối tượng</th><th>Bao gồm</th><th>Giá</th></tr>
      {rows}
    </table>''')

    # Guarantee
    guarantee = offer.get("guarantee", "")
    if guarantee:
        parts.append(f'''<h3><i class="ph ph-shield-check"></i> Guarantee</h3>
    <div class="why">
      <div class="why-label">Cam kết</div>
      <p style="font-size:17px;margin:0">{e(guarantee)}</p>
    </div>''')

    if not parts:
        parts.append('<div class="insight">Grand Slam Offer chưa được thiết kế. AI agent sẽ giúp xây dựng trong quá trình brainstorm.</div>')

    return "\n\n".join(parts)


def _build_roadmap(data: dict) -> str:
    """Build Roadmap section."""
    rm = data["roadmap"]
    parts = []

    for phase in rm.get("phases", []):
        name = e(phase.get("name", "Phase"))
        items = ""
        for item in phase.get("items", []):
            time_label = e(item.get("time", ""))
            action = e(item.get("action", ""))
            items += f'''<div class="tl-item">
        <div class="tl-label">{time_label}</div>
        <div class="tl-text">{action}</div>
      </div>\n'''
        parts.append(f'''<h3>{name}</h3>
    <div class="timeline">
      {items}
    </div>''')

    return "\n\n".join(parts) if parts else '<div class="insight">Roadmap sẽ được xây dựng sau khi validation hoàn tất.</div>'


def _build_sources(data: dict) -> str:
    """Build Sources section."""
    sources = data.get("sources", [])
    if not sources:
        sources = [
            {"domain": "EaseStart Knowledge Base", "detail": f"594-row knowledge graph, {data['industry_display']} domain"},
            {"domain": "Validate Idea Engine", "detail": f"5-dimension scoring, stage-gated methodology"},
            {"domain": "Auto-Research", "detail": "Deep multi-domain KB search (30+ domains, industry-targeted)"},
        ]
        if data.get("digital"):
            sources.append({"domain": "Digital Validation", "detail": f"Reddit + Hacker News pain signal analysis ({data['digital'].get('total_posts', 0)} posts)"})

    items = ""
    for i, s in enumerate(sources, 1):
        items += f'''<div class="source-item">
        <span class="source-num">{i}</span>
        <span class="source-text"><span class="source-domain">{e(s.get("domain", ""))}</span> — {e(s.get("detail", ""))}</span>
      </div>\n'''

    return f'''<div class="sources" id="sources">
      <div class="sources-title">Nguồn dữ liệu</div>
      {items}
    </div>'''


# ─── Main Generator ──────────────────────────────────────────────────

def generate_report(idea: str, industry: str = None,
                    enrichment: dict = None,
                    skip_research: bool = False) -> str:
    """Generate the complete single-page HTML report. Returns output dir path."""
    data = collect_report_data(idea, industry, enrichment, skip_research)

    # Create output directory — ASCII-only slug
    ascii_idea = unicodedata.normalize('NFKD', idea).encode('ascii', 'ignore').decode('ascii')
    slug = ascii_idea.lower().replace(' ', '-')[:40]
    slug = re.sub(r'[^a-z0-9-]', '', slug).strip('-')
    slug = re.sub(r'-+', '-', slug)
    if not slug:
        slug = f"report-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    report_dir = os.path.join(OUT, slug)
    os.makedirs(report_dir, exist_ok=True)

    # Copy shared.css
    css_src = os.path.join(OUT, "shared.css")
    css_dst = os.path.join(report_dir, "shared.css")
    if os.path.exists(css_src):
        shutil.copy2(css_src, css_dst)
    else:
        # Fallback: copy from hvs if exists
        hvs_css = os.path.join(OUT, "hvs", "shared.css")
        if os.path.exists(hvs_css):
            shutil.copy2(hvs_css, css_dst)

    # Add extra inline styles for HVS components
    extra_css = '''
.compare-grid{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid var(--border);margin:16px 0}
.compare-col{padding:16px 20px}
.compare-col:first-child{border-right:1px solid var(--border)}
.compare-col h4{margin-top:0}
.metric-bar{display:flex;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid var(--border)}
.metric-bar:last-child{border-bottom:none}
.metric-label{width:160px;font-size:14px;font-weight:600;flex-shrink:0}
.metric-track{flex:1;height:10px;background:var(--bg-code);border:1px solid var(--border)}
.metric-fill{height:100%;background:var(--black)}
.metric-val{width:50px;text-align:right;font-family:var(--mono);font-size:14px;font-weight:700}
.timeline{position:relative;padding-left:28px;margin:16px 0}
.timeline::before{content:'';position:absolute;left:8px;top:0;bottom:0;width:2px;background:var(--border)}
.tl-item{position:relative;padding:12px 0}
.tl-item::before{content:'';position:absolute;left:-24px;top:16px;width:12px;height:12px;border:2px solid var(--black);background:var(--white)}
.pain-card{border:1px solid var(--border);padding:16px 20px;margin:8px 0}
.pain-title{font-size:16px;font-weight:700;margin-bottom:4px}
.pain-desc{font-size:14px;color:var(--slate);line-height:1.5}
'''

    # Build HTML sections
    sidebar = _build_sidebar(data)
    hero = _build_hero(data)
    reframe = _build_reframe(data)
    dov = _build_dov(data)
    market = _build_market(data)
    offer = _build_offer(data)
    roadmap = _build_roadmap(data)
    sources = _build_sources(data)

    title = e(data.get("title", data["short"]))
    cls_color = data["cls_color"]
    now = data["now"]

    html = f'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Founder's Intel Memo</title>
<link rel="stylesheet" href="shared.css">
<script src="https://unpkg.com/@phosphor-icons/web"></script>
<style>
:root {{ --accent: {cls_color}; }}
{extra_css}
</style>
</head>
<body>
<div class="layout">

{sidebar}

<main class="main">

{hero}

<!-- PHASE 0: REFRAME -->
<h2 id="reframe"><i class="ph ph-lightbulb"></i> Phase 0 — Reframe</h2>
<p class="section-source">EaseStart Ideation Agent — Hướng Loang Protocol</p>

{reframe}

<!-- STAGE 1: DOV -->
<h2 id="dov"><i class="ph ph-exam"></i> Stage 1 — DOV Validation</h2>
<p class="section-source">Deep Origin Validation — IdeaValidator Framework</p>

{dov}

<!-- STAGE 2: MARKET INTEL -->
<h2 id="market"><i class="ph ph-chart-line-up"></i> Stage 2 — Market Intelligence</h2>
<p class="section-source">Research Report + Market Data</p>

{market}

<!-- STAGE 3: GRAND SLAM OFFER -->
<h2 id="offer"><i class="ph ph-target"></i> Stage 3 — Grand Slam Offer</h2>
<p class="section-source">Alex Hormozi Value Equation</p>

{offer}

<!-- ROADMAP -->
<h2 id="roadmap"><i class="ph ph-rocket-launch"></i> Roadmap</h2>
<p class="section-source">Kế hoạch thực thi</p>

{roadmap}

<!-- SOURCES -->
{sources}

<!-- FOOTER -->
<div class="footer">
  <div class="footer-brand">EaseStart</div>
  <p>Generated by EaseStart Validation Report — {now}</p>
  <p>Format: HVS-style · DOV Framework · Grand Slam Offer · KB-enriched</p>
</div>

</main>
</div>

<script>
document.querySelectorAll('.nav-link[href^="#"]').forEach(a=>{{
  a.addEventListener('click',e=>{{e.preventDefault();const t=document.querySelector(a.getAttribute('href'));if(t)t.scrollIntoView({{behavior:'smooth',block:'start'}});
  document.querySelectorAll('.nav-link').forEach(l=>l.classList.remove('active'));a.classList.add('active')}})
}});
const obs=new IntersectionObserver(entries=>{{entries.forEach(e=>{{if(e.isIntersecting){{const id=e.target.id;document.querySelectorAll('.nav-link').forEach(l=>{{l.classList.toggle('active',l.getAttribute('href')==='#'+id)}})}}}})}},{{threshold:0.2}});
document.querySelectorAll('h2[id]').forEach(h=>obs.observe(h));
</script>
</body>
</html>'''

    # Write HTML
    html_path = os.path.join(report_dir, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n  📁 output/{slug}/")
    print(f"  ✅ index.html")
    print(f"  ✅ shared.css")
    print(f"\n  📄 Report: output/{slug}/index.html")

    return report_dir


# ─── CLI ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate HVS-style Validation Report",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python3 scripts/generate_validation_report.py "AI advisor for solo founders"
              python3 scripts/generate_validation_report.py "My idea" --industry fintech --open
              python3 scripts/generate_validation_report.py "My idea" --data enrichment.json --open
        """),
    )
    parser.add_argument("idea", help="Your startup idea in one sentence")
    parser.add_argument("--industry", "-i", help="Industry (auto-detected if omitted)")
    parser.add_argument("--data", "-d", help="Path to enrichment JSON file")
    parser.add_argument("--open", "-o", action="store_true",
                        help="Open report in browser after generation")
    parser.add_argument("--skip-research", action="store_true",
                        help="Skip auto-research (faster, less data)")

    args = parser.parse_args()

    enrichment = None
    if args.data:
        with open(args.data, "r", encoding="utf-8") as f:
            enrichment = json.load(f)

    print(f"\n  🔍 Generating Validation Report...")
    print(f"  Idea: {args.idea}")
    print(f"  Industry: {args.industry or 'auto-detect'}")
    if args.data:
        print(f"  Enrichment: {args.data}")
    print()

    report_dir = generate_report(args.idea, industry=args.industry,
                                  enrichment=enrichment,
                                  skip_research=args.skip_research)

    if args.open:
        import subprocess
        subprocess.run(["open", os.path.join(report_dir, "index.html")],
                       check=False)


if __name__ == "__main__":
    main()
