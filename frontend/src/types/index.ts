export interface Individual {
  id: string
  first_name: string
  last_name: string
  linkedin_url: string | null
  email: string | null
  phone: string | null
  primary_therapeutic_area: string | null
  relationship_status: string | null
  personal_notes: string | null
  created_at: string
  updated_at: string
  education: Education[]
}

export interface IndividualListItem {
  id: string
  first_name: string
  last_name: string
  primary_therapeutic_area: string | null
  relationship_status: string | null
  created_at: string
}

export interface Education {
  id: string
  individual_id: string
  institution: string
  degree_type: string
  field_of_study: string | null
  graduation_year: number | null
}

export interface ManagementCompany {
  id: string
  name: string
  firm_type: string
  website: string | null
  hq_city: string | null
  hq_state: string | null
  description: string | null
  created_at: string
  updated_at: string
}

export interface FundVehicle {
  id: string
  management_company_id: string
  name: string
  vintage_year: number | null
  target_size_mm: number | null
  final_close_mm: number | null
  strategy_focus: string | null
  status: string | null
  created_at: string
  updated_at: string
}

export interface PortfolioCompany {
  id: string
  management_company_id: string
  fund_vehicle_id: string | null
  name: string
  therapeutic_area: string | null
  stage: string | null
  website: string | null
  description: string | null
  created_at: string
  updated_at: string
}

export interface Role {
  id: string
  individual_id: string
  management_company_id: string | null
  fund_vehicle_id: string | null
  portfolio_company_id: string | null
  title: string
  is_current: boolean
  start_date: string | null
  end_date: string | null
  seniority_level: string | null
  created_at: string
  updated_at: string
}

export interface MovementEvent {
  id: string
  individual_id: string
  origin_role_id: string | null
  destination_role_id: string | null
  departure_date: string | null
  joining_date: string | null
  move_type: string
  is_spinout: boolean
  reason: string | null
  carry_economics_notes: string | null
  confidence: string
  source_of_intel: string | null
  tags: string[]
  created_at: string
  updated_at: string
}

export interface Deal {
  id: string
  name: string
  portfolio_company_id: string | null
  therapeutic_area: string | null
  deal_date: string | null
  deal_type: string | null
  deal_size_mm: number | null
  description: string | null
  confidence: string
  source: string | null
  created_at: string
  updated_at: string
  participants: DealParticipant[]
}

export interface DealParticipant {
  id: string
  deal_id: string
  individual_id: string
  role_id: string | null
  is_lead: boolean
}

export interface LPCommitment {
  id: string
  fund_vehicle_id: string
  commitment_amount_mm: number | null
  commitment_date: string | null
  status: string | null
  notes: string | null
  created_at: string
  updated_at: string
}

export interface Note {
  id: string
  entity_type: string
  entity_id: string
  content: string
  created_at: string
  updated_at: string
}

export interface GraphNode {
  id: string
  name: string
  type: string
  firm_type?: string | null
  therapeutic_area?: string | null
  has_lp_commitment?: boolean
  val: number
}

export interface GraphLink {
  source: string
  target: string
  is_current: boolean
  title: string | null
}

export interface GraphData {
  nodes: GraphNode[]
  links: GraphLink[]
}

export interface TimelineEvent {
  id: string
  individual_id: string
  individual_name: string
  date: string
  origin_firm: string | null
  destination_firm: string | null
  origin_title: string | null
  destination_title: string | null
  move_type: string
  is_spinout: boolean
  tags: string[]
}

export interface SearchResult {
  id: string
  type: string
  name: string
  detail: string | null
}

export interface SearchResults {
  individuals: SearchResult[]
  firms: SearchResult[]
  deals: SearchResult[]
}
