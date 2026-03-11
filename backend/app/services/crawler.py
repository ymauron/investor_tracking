import logging
import re
from datetime import datetime
from decimal import Decimal
from email.utils import parsedate_to_datetime

import feedparser
import httpx
from sqlalchemy.orm import Session

from app.models.enums import (
    TransactionType,
    TransactionSource,
    TherapeuticArea,
    ClinicalStage,
    Sentiment,
)
from app.models.transaction import Transaction
from app.services.matcher import match_to_management_company, match_to_portfolio_company
from app.services.alert_service import check_alerts

logger = logging.getLogger(__name__)

FEED_URLS: dict[TransactionSource, list[str]] = {
    TransactionSource.biospace: [
        "https://www.biospace.com/deals.rss",
        "https://www.biospace.com/FDA.rss",
        "https://www.biospace.com/drug-development.rss",
    ],
    TransactionSource.fierce_biotech: [
        "https://www.fiercebiotech.com/rss/xml",
    ],
    TransactionSource.fierce_pharma: [
        "https://www.fiercepharma.com/rss/xml",
    ],
}

TYPE_KEYWORDS: dict[TransactionType, list[str]] = {
    TransactionType.ma: [
        "acquir", "merger", "buyout", "takeover", "to buy", "to purchase",
        "acquisition", "acquired by",
    ],
    TransactionType.ipo: [
        "ipo", "initial public offering", "goes public", "stock market debut",
        "public listing",
    ],
    TransactionType.licensing: [
        "licens", "license agreement", "royalt", "sublicens",
    ],
    TransactionType.clinical_trial: [
        "phase 1", "phase 2", "phase 3", "phase i", "phase ii", "phase iii",
        "clinical trial", "pivotal study", "pivotal trial", "endpoint",
        "trial results", "readout", "topline data",
    ],
    TransactionType.fda_approval: [
        "fda approv", "cleared by fda", "nda approv", "bla approv",
        "fda grants", "fda clears", "receives fda",
    ],
    TransactionType.fda_rejection: [
        "complete response letter", "crl", "fda reject", "refus",
        "not approved", "fda decline",
    ],
    TransactionType.funding_round: [
        "series a", "series b", "series c", "series d", "series e",
        "funding round", "raises $", "raised $", "secures $", "secured $",
        "venture funding", "financing round",
    ],
    TransactionType.partnership: [
        "partner", "collaborat", "alliance", "joint venture", "strategic deal",
        "co-develop",
    ],
    TransactionType.bankruptcy: [
        "bankrupt", "chapter 11", "chapter 7", "insolven", "wind down",
    ],
}

STAGE_KEYWORDS: dict[ClinicalStage, list[str]] = {
    ClinicalStage.preclinical: ["preclinical", "pre-clinical", "inc study"],
    ClinicalStage.phase_1: ["phase 1", "phase i ", "phase i/"],
    ClinicalStage.phase_2: ["phase 2", "phase ii ", "phase ii/"],
    ClinicalStage.phase_3: ["phase 3", "phase iii", "pivotal"],
    ClinicalStage.nda_bla_filed: ["nda", "bla", "sNDA", "sBLA", "filed with fda"],
    ClinicalStage.approved: ["fda approv", "approved"],
}

AREA_KEYWORDS: dict[TherapeuticArea, list[str]] = {
    TherapeuticArea.oncology: ["cancer", "tumor", "oncol", "lymphoma", "leukemia", "carcinoma", "melanoma", "glioma"],
    TherapeuticArea.rare_disease: ["rare disease", "orphan drug", "ultra-rare", "rare genetic"],
    TherapeuticArea.neuroscience: ["neuro", "alzheimer", "parkinson", "cns", "brain", "epilep", "seizure"],
    TherapeuticArea.immunology: ["immun", "autoimmune", "inflammat", "arthritis", "lupus", "crohn"],
    TherapeuticArea.cardiovascular: ["cardio", "heart", "cardiovascular", "atrial", "hypertens"],
    TherapeuticArea.gene_therapy: ["gene therapy", "gene editing", "crispr", "aav", "cell therapy", "car-t"],
    TherapeuticArea.medtech: ["medtech", "medical device", "surgical", "implant"],
    TherapeuticArea.digital_health: ["digital health", "telehealth", "wearable", "health tech"],
    TherapeuticArea.diagnostics: ["diagnostic", "biomarker", "assay", "companion diagnostic"],
}

DEAL_VALUE_PATTERN = re.compile(
    r"\$\s*([\d,.]+)\s*(billion|million|B|M)\b", re.IGNORECASE
)

FALSE_POSITIVE_COMPANIES = {
    "fda", "phase", "united states", "the company", "the firm",
    "wall street", "new york", "san francisco", "stock exchange",
    "press release", "clinical trial", "the drug", "the treatment",
}


def fetch_feed(url: str) -> feedparser.FeedParserDict:
    resp = httpx.get(url, timeout=30, follow_redirects=True, headers={
        "User-Agent": "InvestorTracker/1.0 (RSS Reader)"
    })
    resp.raise_for_status()
    return feedparser.parse(resp.text)


def classify_transaction_type(title: str, description: str) -> TransactionType | None:
    text = f"{title} {description}".lower()
    for ttype, keywords in TYPE_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return ttype
    return TransactionType.other


def classify_stage(title: str, description: str) -> ClinicalStage | None:
    text = f"{title} {description}".lower()
    for stage, keywords in STAGE_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return stage
    return None


def classify_therapeutic_area(title: str, description: str) -> TherapeuticArea | None:
    text = f"{title} {description}".lower()
    for area, keywords in AREA_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return area
    return None


def extract_deal_value(text: str) -> Decimal | None:
    match = DEAL_VALUE_PATTERN.search(text)
    if not match:
        return None
    value = Decimal(match.group(1).replace(",", ""))
    unit = match.group(2).lower()
    if unit in ("billion", "b"):
        value *= 1000
    return value


def extract_companies(text: str) -> list[str]:
    pattern = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b")
    matches = pattern.findall(text)
    seen = set()
    results = []
    for name in matches:
        normalized = name.lower()
        if normalized in FALSE_POSITIVE_COMPANIES or len(name) < 4:
            continue
        if normalized not in seen:
            seen.add(normalized)
            results.append(name)
    return results[:10]


def classify_sentiment(title: str, description: str) -> Sentiment:
    text = f"{title} {description}".lower()
    positive = ["approv", "success", "positive", "met primary", "exceeded",
                 "breakthrough", "granted", "cleared", "smash", "strong"]
    negative = ["reject", "fail", "negative", "miss", "disappoint", "halt",
                 "suspend", "withdraw", "bankrupt", "terminat", "discontinu"]
    pos_count = sum(1 for kw in positive if kw in text)
    neg_count = sum(1 for kw in negative if kw in text)
    if pos_count > neg_count:
        return Sentiment.positive
    if neg_count > pos_count:
        return Sentiment.negative
    return Sentiment.neutral


def parse_published_date(entry) -> datetime | None:
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        from time import mktime
        return datetime.utcfromtimestamp(mktime(entry.published_parsed))
    if hasattr(entry, "published") and entry.published:
        try:
            return parsedate_to_datetime(entry.published).replace(tzinfo=None)
        except Exception:
            pass
    return datetime.utcnow()


def crawl_all_feeds(db: Session) -> dict:
    stats = {"new": 0, "skipped": 0, "errors": 0}

    for source, urls in FEED_URLS.items():
        for url in urls:
            try:
                feed = fetch_feed(url)
            except Exception:
                logger.exception(f"Failed to fetch feed: {url}")
                stats["errors"] += 1
                continue

            for entry in feed.entries:
                try:
                    entry_url = getattr(entry, "link", None) or getattr(entry, "id", None)
                    if not entry_url:
                        continue

                    existing = db.query(Transaction.id).filter(
                        Transaction.url == entry_url
                    ).first()
                    if existing:
                        stats["skipped"] += 1
                        continue

                    title = getattr(entry, "title", "").strip()
                    description = getattr(entry, "description", "") or ""
                    description = re.sub(r"<[^>]+>", "", description).strip()
                    full_text = f"{title} {description}"

                    companies = extract_companies(full_text)
                    portco_id = match_to_portfolio_company(db, companies)
                    mgmt_id = match_to_management_company(db, companies)

                    txn = Transaction(
                        title=title[:500],
                        url=entry_url[:1000],
                        source=source,
                        published_at=parse_published_date(entry),
                        raw_description=description[:5000] if description else None,
                        transaction_type=classify_transaction_type(title, description),
                        companies_mentioned=companies if companies else None,
                        deal_value_mm=extract_deal_value(full_text),
                        therapeutic_area=classify_therapeutic_area(title, description),
                        stage=classify_stage(title, description),
                        summary=description[:500] if description else None,
                        sentiment=classify_sentiment(title, description),
                        portfolio_company_id=portco_id,
                        management_company_id=mgmt_id,
                    )
                    db.add(txn)
                    db.flush()

                    check_alerts(db, txn)
                    stats["new"] += 1

                except Exception:
                    logger.exception(f"Error processing entry: {getattr(entry, 'link', 'unknown')}")
                    stats["errors"] += 1
                    continue

    db.commit()
    logger.info(f"Crawl complete: {stats}")
    return stats
