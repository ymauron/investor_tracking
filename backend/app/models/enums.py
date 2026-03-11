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
