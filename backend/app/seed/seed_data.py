"""
Seed script to generate realistic healthcare investor mock data.
Run: python -m app.seed.seed_data
"""

import random
from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app.models import *  # noqa: F401,F403
from app.models.individual import Individual, IndividualEducation
from app.models.firm import ManagementCompany, FundVehicle, PortfolioCompany
from app.models.role import Role
from app.models.movement import MovementEvent, MovementEventTag
from app.models.deal import Deal, DealParticipant
from app.models.lp_commitment import LPCommitment
from app.models.note import Note
from app.models.enums import (
    FirmType,
    TherapeuticArea,
    ConfidenceLevel,
    MoveType,
    EntityType,
)

random.seed(42)

FIRMS_DATA = [
    ("OrbiMed Advisors", FirmType.vc, "New York", "NY"),
    ("ARCH Venture Partners", FirmType.vc, "Chicago", "IL"),
    ("Flagship Pioneering", FirmType.vc, "Cambridge", "MA"),
    ("Third Rock Ventures", FirmType.vc, "Boston", "MA"),
    ("RA Capital Management", FirmType.crossover, "Boston", "MA"),
    ("Sofinnova Investments", FirmType.vc, "San Francisco", "CA"),
    ("Venrock Healthcare", FirmType.vc, "Palo Alto", "CA"),
    ("Bain Capital Life Sciences", FirmType.growth_equity, "Boston", "MA"),
    ("Deerfield Management", FirmType.crossover, "New York", "NY"),
    ("Perceptive Advisors", FirmType.crossover, "New York", "NY"),
    ("Foresite Capital", FirmType.vc, "San Francisco", "CA"),
    ("General Atlantic Healthcare", FirmType.growth_equity, "New York", "NY"),
    ("Warburg Pincus Healthcare", FirmType.buyout, "New York", "NY"),
    ("Versant Ventures", FirmType.vc, "San Francisco", "CA"),
    ("5AM Ventures", FirmType.vc, "San Francisco", "CA"),
    ("Atlas Venture", FirmType.vc, "Cambridge", "MA"),
    ("Omega Funds", FirmType.vc, "Boston", "MA"),
    ("Abingworth", FirmType.vc, "London", "UK"),
    ("EQT Life Sciences", FirmType.buyout, "Stockholm", "SE"),
    ("Gurnet Point Capital", FirmType.growth_equity, "Cambridge", "MA"),
]

FIRST_NAMES = [
    "Sarah", "Michael", "Jennifer", "David", "Emily", "Robert", "Lisa", "James",
    "Amanda", "Christopher", "Rebecca", "Daniel", "Nicole", "Matthew", "Rachel",
    "Andrew", "Lauren", "Jonathan", "Katherine", "Thomas", "Megan", "William",
    "Stephanie", "Brian", "Jessica", "Ryan", "Michelle", "Kevin", "Elizabeth",
    "Mark", "Allison", "Stephen", "Samantha", "Jason", "Heather", "Eric",
    "Catherine", "Jeffrey", "Natalie", "Scott", "Christina", "Timothy", "Andrea",
    "Benjamin", "Margaret", "Patrick", "Kristin", "Gregory", "Alexandra", "Anthony",
]

LAST_NAMES = [
    "Chen", "Patel", "Kumar", "Williams", "Johnson", "Anderson", "Thompson",
    "Zhang", "Garcia", "Martinez", "Robinson", "Clark", "Lewis", "Walker",
    "Hall", "Young", "King", "Wright", "Lopez", "Hill", "Scott", "Green",
    "Adams", "Baker", "Gonzalez", "Nelson", "Carter", "Mitchell", "Perez",
    "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards",
    "Collins", "Stewart", "Sanchez", "Morris", "Rogers", "Reed", "Cook",
    "Morgan", "Bell", "Murphy", "Bailey", "Rivera", "Cooper", "Richardson",
]

INSTITUTIONS = [
    "Harvard University", "Stanford University", "MIT", "Wharton School",
    "Johns Hopkins University", "Yale University", "Columbia University",
    "University of Chicago", "Duke University", "UC San Francisco",
    "Cornell University", "Northwestern University", "University of Michigan",
    "University of Pennsylvania", "Boston University",
]

TITLES = {
    "analyst": ["Analyst", "Research Analyst", "Investment Analyst"],
    "associate": ["Associate", "Senior Associate", "Investment Associate"],
    "vp": ["Vice President", "VP Investments"],
    "principal": ["Principal", "Senior Principal", "Director"],
    "partner": ["Partner", "General Partner", "Managing Partner", "Managing Director"],
}

SENIORITY_PROGRESSION = ["analyst", "associate", "vp", "principal", "partner"]

PORTCO_NAMES = [
    "Zenith Therapeutics", "Apex Biosciences", "Nova Oncology", "Meridian Health",
    "Prism Diagnostics", "Vertex Genomics", "Catalyst Biotech", "Lumina Pharma",
    "Aegis Medical Devices", "Synapse Neuroscience", "Helix Gene Therapy",
    "Beacon Digital Health", "Orion Immunology", "Pinnacle Rare Disease",
    "Atlas Cardiovascular", "Keystone Medtech", "Quantum Diagnostics",
    "Horizon Cell Therapy", "Nexus Bioinformatics", "Cipher Therapeutics",
    "Vanguard Oncology", "Paragon Neuro", "Summit Health AI", "Radiant Genomics",
    "Eclipse Biotech", "Frontier Immunotherapeutics", "Solaris Pharma",
    "Acumen Health Tech", "Bridge Bio Solutions", "Genesis Rare Therapeutics",
    "Cortex Neural Systems", "Polaris Digital Medicine", "Ascend Oncology",
    "Elevate Therapeutics", "Spectrum Gene Sciences", "Pacific Bioventures",
    "Cardinal Health AI", "Axis Immunology", "Sterling Cardiovascular",
    "Pioneer Cell Systems", "Trident Diagnostics", "Ember Therapeutics",
    "Crest Neuroscience", "Harbor Medtech", "Infinity Genomics",
    "Matrix BioPharma", "Velocity Health", "Stratos Immunotherapy",
    "Quantum Neural Tech", "Arcadian Therapeutics",
]

DEAL_TYPES = ["seed", "series_a", "series_b", "series_c", "series_d", "growth", "buyout"]

CONFIDENCE_LEVELS = list(ConfidenceLevel)
THERAPEUTIC_AREAS = list(TherapeuticArea)
MOVEMENT_TAGS = ["key_person_event", "fund_launch", "retirement", "spinout", "promotion"]


def random_date(start_year: int, end_year: int) -> date:
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def seed_database():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # Check if data already exists
        if db.query(ManagementCompany).count() > 0:
            print("Database already seeded. Skipping.")
            return

        print("Seeding management companies...")
        mgmt_companies: list[ManagementCompany] = []
        for name, ftype, city, state in FIRMS_DATA:
            mc = ManagementCompany(
                name=name,
                firm_type=ftype,
                hq_city=city,
                hq_state=state,
            )
            db.add(mc)
            mgmt_companies.append(mc)
        db.flush()

        print("Seeding fund vehicles...")
        fund_vehicles: list[FundVehicle] = []
        for mc in mgmt_companies:
            num_funds = random.randint(2, 4)
            for i in range(num_funds):
                vintage = random.randint(2015, 2024)
                target = Decimal(str(random.randint(200, 2000)))
                fv = FundVehicle(
                    management_company_id=mc.id,
                    name=f"{mc.name} Fund {'I' * (i + 1) if i < 3 else f'{i + 1}'}",
                    vintage_year=vintage,
                    target_size_mm=target,
                    final_close_mm=target * Decimal(str(random.uniform(0.8, 1.2))),
                    strategy_focus=random.choice(THERAPEUTIC_AREAS),
                    status=random.choice(["fundraising", "investing", "harvesting", "fully_invested"]),
                )
                db.add(fv)
                fund_vehicles.append(fv)
        db.flush()

        print("Seeding portfolio companies...")
        portcos: list[PortfolioCompany] = []
        for name in PORTCO_NAMES:
            mc = random.choice(mgmt_companies)
            mc_funds = [f for f in fund_vehicles if f.management_company_id == mc.id]
            fv = random.choice(mc_funds) if mc_funds else None
            pc = PortfolioCompany(
                management_company_id=mc.id,
                fund_vehicle_id=fv.id if fv else None,
                name=name,
                therapeutic_area=random.choice(THERAPEUTIC_AREAS),
                stage=random.choice(["seed", "series_a", "series_b", "series_c", "public"]),
            )
            db.add(pc)
            portcos.append(pc)
        db.flush()

        print("Seeding individuals...")
        individuals: list[Individual] = []
        used_names: set[tuple[str, str]] = set()
        for _ in range(90):
            while True:
                fn = random.choice(FIRST_NAMES)
                ln = random.choice(LAST_NAMES)
                if (fn, ln) not in used_names:
                    used_names.add((fn, ln))
                    break
            ind = Individual(
                first_name=fn,
                last_name=ln,
                email=f"{fn.lower()}.{ln.lower()}@email.com",
                primary_therapeutic_area=random.choice(THERAPEUTIC_AREAS),
                relationship_status=random.choice(
                    ["warm intro", "cold", "met at JPM", "LP relationship", "board co-member", None]
                ),
            )
            db.add(ind)
            individuals.append(ind)
        db.flush()

        # Add education
        print("Seeding education...")
        degree_types = ["ba", "bs", "mba", "md", "phd", "md_phd", "ms"]
        fields = [
            "Biology", "Chemistry", "Biomedical Engineering", "Finance",
            "Business Administration", "Molecular Biology", "Neuroscience",
            "Computer Science", "Public Health", "Medicine",
        ]
        for ind in individuals:
            num_degrees = random.randint(1, 3)
            for _ in range(num_degrees):
                edu = IndividualEducation(
                    individual_id=ind.id,
                    institution=random.choice(INSTITUTIONS),
                    degree_type=random.choice(degree_types),
                    field_of_study=random.choice(fields),
                    graduation_year=random.randint(1990, 2020),
                )
                db.add(edu)

        # Assign roles (current)
        print("Seeding roles...")
        all_roles: list[Role] = []
        for ind in individuals:
            seniority = random.choice(SENIORITY_PROGRESSION)
            mc = random.choice(mgmt_companies)
            title = random.choice(TITLES[seniority])
            start = random_date(2018, 2024)
            role = Role(
                individual_id=ind.id,
                management_company_id=mc.id,
                title=title,
                is_current=True,
                start_date=start,
                seniority_level=seniority,
            )
            db.add(role)
            all_roles.append(role)
        db.flush()

        # Add past roles for ~60% of individuals
        past_roles: list[Role] = []
        for ind in random.sample(individuals, int(len(individuals) * 0.6)):
            prev_mc = random.choice(mgmt_companies)
            seniority_idx = max(
                0,
                SENIORITY_PROGRESSION.index(
                    random.choice(SENIORITY_PROGRESSION[:3])
                ),
            )
            seniority = SENIORITY_PROGRESSION[seniority_idx]
            start = random_date(2014, 2018)
            end = random_date(2018, 2022)
            if end < start:
                start, end = end, start
            role = Role(
                individual_id=ind.id,
                management_company_id=prev_mc.id,
                title=random.choice(TITLES[seniority]),
                is_current=False,
                start_date=start,
                end_date=end,
                seniority_level=seniority,
            )
            db.add(role)
            past_roles.append(role)
        db.flush()

        # Create movement events
        print("Seeding movement events...")
        for role in past_roles:
            current_roles = [
                r for r in all_roles
                if r.individual_id == role.individual_id and r.is_current
            ]
            if not current_roles:
                continue
            dest_role = current_roles[0]
            is_same_firm = role.management_company_id == dest_role.management_company_id
            event = MovementEvent(
                individual_id=role.individual_id,
                origin_role_id=role.id,
                destination_role_id=dest_role.id,
                departure_date=role.end_date,
                joining_date=dest_role.start_date,
                move_type=MoveType.internal if is_same_firm else MoveType.external,
                is_spinout=random.random() < 0.1,
                reason=random.choice([
                    "Career advancement", "Better platform", "Fund launch",
                    "Recruited", "Followed GP", None,
                ]),
                confidence=random.choice(CONFIDENCE_LEVELS),
                source_of_intel=random.choice([
                    "LinkedIn", "Press release", "Industry contact",
                    "Conference", "Direct conversation",
                ]),
            )
            db.add(event)
            db.flush()

            # Add tags
            if random.random() < 0.3:
                num_tags = random.randint(1, 2)
                for tag in random.sample(MOVEMENT_TAGS, num_tags):
                    db.add(MovementEventTag(movement_event_id=event.id, tag=tag))

        # Create deals
        print("Seeding deals...")
        deals: list[Deal] = []
        for _ in range(40):
            pc = random.choice(portcos)
            deal = Deal(
                name=f"{pc.name} {random.choice(DEAL_TYPES).replace('_', ' ').title()}",
                portfolio_company_id=pc.id,
                therapeutic_area=pc.therapeutic_area,
                deal_date=random_date(2018, 2025),
                deal_type=random.choice(DEAL_TYPES),
                deal_size_mm=Decimal(str(random.randint(10, 500))),
                confidence=random.choice([ConfidenceLevel.confirmed, ConfidenceLevel.press_release]),
                source=random.choice(["SEC filing", "Press release", "PitchBook", "Crunchbase"]),
            )
            db.add(deal)
            deals.append(deal)
        db.flush()

        # Add deal participants
        print("Seeding deal participants...")
        for deal in deals:
            num_participants = random.randint(1, 3)
            participants = random.sample(individuals, num_participants)
            for i, ind in enumerate(participants):
                ind_roles = [r for r in all_roles if r.individual_id == ind.id]
                dp = DealParticipant(
                    deal_id=deal.id,
                    individual_id=ind.id,
                    role_id=ind_roles[0].id if ind_roles else None,
                    is_lead=(i == 0),
                )
                db.add(dp)

        # Create LP commitments
        print("Seeding LP commitments...")
        lp_funds = random.sample(fund_vehicles, min(8, len(fund_vehicles)))
        for fv in lp_funds:
            lp = LPCommitment(
                fund_vehicle_id=fv.id,
                commitment_amount_mm=Decimal(str(random.randint(5, 50))),
                commitment_date=random_date(2018, 2024),
                status=random.choice(["committed", "considering", "passed"]),
            )
            db.add(lp)

        # Add some notes
        print("Seeding notes...")
        note_contents = [
            "Strong track record in oncology investments.",
            "Met at JPMorgan Healthcare Conference 2024.",
            "Interested in co-investment opportunities.",
            "Key relationship — schedule quarterly check-ins.",
            "Recently raised new fund, actively deploying.",
            "Known for deep scientific diligence process.",
            "Well-connected in rare disease ecosystem.",
            "Considering expansion into digital health.",
            "Former FDA reviewer — strong regulatory insight.",
            "Spoke on gene therapy panel at BIO conference.",
        ]
        for _ in range(20):
            entity = random.choice(individuals)
            note = Note(
                entity_type=EntityType.individual,
                entity_id=entity.id,
                content=random.choice(note_contents),
            )
            db.add(note)
        for _ in range(10):
            entity = random.choice(mgmt_companies)
            note = Note(
                entity_type=EntityType.management_company,
                entity_id=entity.id,
                content=random.choice(note_contents),
            )
            db.add(note)

        db.commit()
        print("Seed complete!")
        print(f"  {len(mgmt_companies)} management companies")
        print(f"  {len(fund_vehicles)} fund vehicles")
        print(f"  {len(portcos)} portfolio companies")
        print(f"  {len(individuals)} individuals")
        print(f"  {len(past_roles)} movement events")
        print(f"  {len(deals)} deals")
        print(f"  {len(lp_funds)} LP commitments")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
