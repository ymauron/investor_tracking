from pydantic import BaseModel


class GraphNode(BaseModel):
    id: str
    name: str
    type: str  # "person" or "firm"
    firm_type: str | None = None
    therapeutic_area: str | None = None
    has_lp_commitment: bool = False
    val: int = 1


class GraphLink(BaseModel):
    source: str
    target: str
    is_current: bool = True
    title: str | None = None


class GraphData(BaseModel):
    nodes: list[GraphNode]
    links: list[GraphLink]


class TimelineEvent(BaseModel):
    id: str
    individual_id: str
    individual_name: str
    date: str
    origin_firm: str | None = None
    destination_firm: str | None = None
    origin_title: str | None = None
    destination_title: str | None = None
    move_type: str
    is_spinout: bool = False
    tags: list[str] = []


class TimelineData(BaseModel):
    events: list[TimelineEvent]
