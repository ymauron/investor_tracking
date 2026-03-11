import enum


class FirmType(str, enum.Enum):
    vc = "vc"
    growth_equity = "growth_equity"
    buyout = "buyout"
    crossover = "crossover"
    corporate_vc = "corporate_vc"
    family_office = "family_office"
    other = "other"


class TherapeuticArea(str, enum.Enum):
    oncology = "oncology"
    rare_disease = "rare_disease"
    medtech = "medtech"
    digital_health = "digital_health"
    neuroscience = "neuroscience"
    immunology = "immunology"
    cardiovascular = "cardiovascular"
    gene_therapy = "gene_therapy"
    diagnostics = "diagnostics"
    multi_sector = "multi_sector"
    other = "other"


class ConfidenceLevel(str, enum.Enum):
    confirmed = "confirmed"
    rumor = "rumor"
    press_release = "press_release"
    personal_conversation = "personal_conversation"
    linkedin_update = "linkedin_update"


class DegreeType(str, enum.Enum):
    ba = "ba"
    bs = "bs"
    mba = "mba"
    md = "md"
    phd = "phd"
    md_phd = "md_phd"
    jd = "jd"
    mph = "mph"
    ms = "ms"
    other = "other"


class MoveType(str, enum.Enum):
    internal = "internal"
    external = "external"


class EntityType(str, enum.Enum):
    individual = "individual"
    management_company = "management_company"
    fund_vehicle = "fund_vehicle"
    portfolio_company = "portfolio_company"
    deal = "deal"
    movement_event = "movement_event"


class TransactionType(str, enum.Enum):
    ma = "ma"
    ipo = "ipo"
    licensing = "licensing"
    clinical_trial = "clinical_trial"
    fda_approval = "fda_approval"
    fda_rejection = "fda_rejection"
    funding_round = "funding_round"
    partnership = "partnership"
    bankruptcy = "bankruptcy"
    other = "other"


class TransactionSource(str, enum.Enum):
    biospace = "biospace"
    fierce_biotech = "fierce_biotech"
    fierce_pharma = "fierce_pharma"


class ClinicalStage(str, enum.Enum):
    preclinical = "preclinical"
    phase_1 = "phase_1"
    phase_2 = "phase_2"
    phase_3 = "phase_3"
    nda_bla_filed = "nda_bla_filed"
    approved = "approved"
    post_market = "post_market"
    unknown = "unknown"


class Sentiment(str, enum.Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"
