# hospitality_firm.py
# NAICS 71, 72: Arts, Entertainment, Recreation & Accommodation and Food Services

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import date, datetime, timedelta
from enum import Enum

from .firm import BaseFirm, Money, Transaction
from .org_chart import Role, RoleType, VotingRights

class HospitalityType(Enum):
    HOTEL = "hotel"
    RESORT = "resort"
    RESTAURANT = "restaurant"
    CASINO = "casino"
    THEME_PARK = "theme_park"
    CRUISE_LINE = "cruise_line"
    SPORTS_VENUE = "sports_venue"
    CONFERENCE_CENTER = "conference_center"
    ENTERTAINMENT_VENUE = "entertainment_venue"
    RECREATIONAL_FACILITY = "recreational_facility"

class AccommodationType(Enum):
    STANDARD_ROOM = "standard_room"
    DELUXE_ROOM = "deluxe_room"
    SUITE = "suite"
    PRESIDENTIAL_SUITE = "presidential_suite"
    VILLA = "villa"
    CABIN = "cabin"

class ReservationStatus(Enum):
    CONFIRMED = "confirmed"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"
    WAITLIST = "waitlist"

class ServiceType(Enum):
    ACCOMMODATION = "accommodation"
    FOOD_BEVERAGE = "food_beverage"
    SPA = "spa"
    RECREATION = "recreation"
    ENTERTAINMENT = "entertainment"
    BUSINESS_SERVICES = "business_services"
    TRANSPORTATION = "transportation"

@dataclass
class Guest:
    guest_id: str
    name: str
    check_in_date: date
    check_out_date: date
    accommodation_type: AccommodationType
    reservation_status: ReservationStatus
    total_charges: float = 0.0
    loyalty_level: str = "standard"  # standard, silver, gold, platinum
    group_size: int = 1
    preferences: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Reservation:
    reservation_id: str
    guest_id: str
    booking_date: date
    check_in_date: date
    check_out_date: date
    accommodation_type: AccommodationType
    room_rate: float
    status: ReservationStatus
    nights: int = 1
    total_revenue: float = 0.0
    booking_channel: str = "direct"  # direct, ota, travel_agent

@dataclass
class Event:
    event_id: str
    event_name: str
    event_type: str  # wedding, conference, concert, sports
    event_date: date
    capacity: int
    expected_attendance: int
    ticket_price: float = 0.0
    total_revenue: float = 0.0
    catering_required: bool = False

@dataclass
class Facility:
    facility_id: str
    facility_type: str  # restaurant, spa, gym, pool, theater
    capacity: int
    operating_hours: Dict[str, str]  # day -> hours
    revenue_per_guest: float = 50.0
    utilization_rate: float = 0.70

@dataclass
class MenuItem:
    item_id: str
    item_name: str
    category: str  # appetizer, entree, dessert, beverage
    cost_to_make: float
    selling_price: float
    popularity_score: float = 0.7  # 0-1 scale

@dataclass
class HospitalityFirm(BaseFirm):
    # Facility characteristics
    hospitality_type: HospitalityType = HospitalityType.HOTEL
    property_size_sqft: float = 50000.0
    location_type: str = "urban"  # urban, suburban, resort, airport
    star_rating: int = 3  # 1-5 star rating
    
    # Accommodation capacity
    total_rooms: int = 100
    rooms_by_type: Dict[AccommodationType, int] = field(default_factory=dict)
    available_rooms: int = 100
    occupancy_rate: float = 0.75
    average_daily_rate: float = 150.0  # ADR
    
    # Guest management
    current_guests: List[Guest] = field(default_factory=list)
    reservations: List[Reservation] = field(default_factory=list)
    total_checkins: int = 0
    total_checkouts: int = 0
    average_length_stay: float = 2.5  # nights
    
    # Revenue streams
    room_revenue: float = 0.0
    food_beverage_revenue: float = 0.0
    other_revenue: float = 0.0  # spa, retail, etc.
    total_revenue_per_available_room: float = 0.0  # RevPAR
    
    # Food and beverage operations
    restaurants: List[str] = field(default_factory=list)
    bars: List[str] = field(default_factory=list)
    menu_items: List[MenuItem] = field(default_factory=list)
    food_cost_percentage: float = 0.30  # 30% food cost
    beverage_cost_percentage: float = 0.25  # 25% beverage cost
    
    # Event and meeting facilities
    meeting_rooms: int = 5
    ballroom_capacity: int = 500
    events_scheduled: List[Event] = field(default_factory=list)
    event_revenue: float = 0.0
    catering_revenue: float = 0.0
    
    # Entertainment and amenities
    facilities: List[Facility] = field(default_factory=list)
    amenities: List[str] = field(default_factory=list)
    entertainment_schedule: Dict[date, List[str]] = field(default_factory=dict)
    recreational_activities: List[str] = field(default_factory=list)
    
    # Staffing and service
    front_desk_staff: int = 8
    housekeeping_staff: int = 15
    food_service_staff: int = 20
    management_staff: int = 5
    guest_service_score: float = 4.2  # out of 5
    
    # Pricing and revenue management
    dynamic_pricing_enabled: bool = True
    seasonal_rate_adjustments: Dict[str, float] = field(default_factory=dict)
    demand_forecasting: Dict[date, float] = field(default_factory=dict)
    competitor_rate_data: Dict[str, float] = field(default_factory=dict)
    
    # Guest loyalty and marketing
    loyalty_program: bool = True
    loyalty_members: Dict[str, int] = field(default_factory=dict)  # level -> count
    marketing_channels: List[str] = field(default_factory=list)
    online_review_score: float = 4.1  # aggregated review score
    
    # Quality and compliance
    service_quality_scores: Dict[str, float] = field(default_factory=dict)
    health_safety_compliance: float = 0.95
    environmental_certifications: List[str] = field(default_factory=list)
    accessibility_compliance: bool = True
    
    # Seasonal operations
    peak_season: List[str] = field(default_factory=list)  # months
    seasonal_closures: List[str] = field(default_factory=list)
    weather_dependent_operations: bool = False
    seasonal_staffing_adjustments: Dict[str, float] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()
        if not self.naics:
            if self.hospitality_type in [HospitalityType.THEME_PARK, HospitalityType.CASINO, 
                                       HospitalityType.SPORTS_VENUE, HospitalityType.ENTERTAINMENT_VENUE]:
                self.naics = "71"  # Arts, Entertainment, and Recreation
            else:
                self.naics = "72"  # Accommodation and Food Services
        
        # Initialize default room distribution
        if not self.rooms_by_type:
            self.rooms_by_type = {
                AccommodationType.STANDARD_ROOM: int(self.total_rooms * 0.60),
                AccommodationType.DELUXE_ROOM: int(self.total_rooms * 0.25),
                AccommodationType.SUITE: int(self.total_rooms * 0.15)
            }
    
    # Reservation and guest management
    def make_reservation(self, reservation: Reservation) -> str:
        """Process new reservation"""
        # Check availability
        if not self._check_availability(reservation.check_in_date, 
                                      reservation.check_out_date, 
                                      reservation.accommodation_type):
            reservation.status = ReservationStatus.WAITLIST
            self.reservations.append(reservation)
            return reservation.reservation_id
        
        # Calculate revenue
        nights = (reservation.check_out_date - reservation.check_in_date).days
        reservation.nights = nights
        reservation.total_revenue = reservation.room_rate * nights
        
        # Apply dynamic pricing
        if self.dynamic_pricing_enabled:
            rate_adjustment = self._calculate_dynamic_rate(reservation.check_in_date)
            reservation.room_rate *= rate_adjustment
            reservation.total_revenue *= rate_adjustment
        
        reservation.status = ReservationStatus.CONFIRMED
        self.reservations.append(reservation)
        
        # Record revenue
        self.room_revenue += reservation.total_revenue
        self.post("reservation_receivable", "room_revenue", reservation.total_revenue,
                 f"Reservation: {reservation.reservation_id}")
        
        return reservation.reservation_id
    
    def check_in_guest(self, reservation_id: str) -> bool:
        """Check in guest"""
        reservation = next((r for r in self.reservations if r.reservation_id == reservation_id), None)
        if not reservation or reservation.status != ReservationStatus.CONFIRMED:
            return False
        
        # Create guest record
        guest = Guest(
            guest_id=f"guest_{reservation.guest_id}",
            name=f"Guest {reservation.guest_id}",
            check_in_date=reservation.check_in_date,
            check_out_date=reservation.check_out_date,
            accommodation_type=reservation.accommodation_type,
            reservation_status=ReservationStatus.CHECKED_IN
        )
        
        self.current_guests.append(guest)
        reservation.status = ReservationStatus.CHECKED_IN
        self.total_checkins += 1
        
        # Update room availability
        self.available_rooms -= 1
        self.occupancy_rate = (self.total_rooms - self.available_rooms) / self.total_rooms
        
        # Record check-in revenue
        self.post("cash", "room_revenue", reservation.total_revenue,
                 f"Check-in: {reservation.reservation_id}")
        self.income_statement["revenue"] += reservation.total_revenue
        
        return True
    
    def check_out_guest(self, guest_id: str) -> float:
        """Check out guest and process final billing"""
        guest = next((g for g in self.current_guests if g.guest_id == guest_id), None)
        if not guest:
            return 0.0
        
        # Calculate total charges (room + incidentals)
        room_charges = guest.total_charges
        incidental_charges = self._calculate_incidental_charges(guest)
        total_bill = room_charges + incidental_charges
        
        guest.total_charges = total_bill
        guest.reservation_status = ReservationStatus.CHECKED_OUT
        
        # Update metrics
        self.total_checkouts += 1
        stay_length = (guest.check_out_date - guest.check_in_date).days
        self.average_length_stay = (self.average_length_stay * 0.95 + stay_length * 0.05)
        
        # Update room availability
        self.available_rooms += 1
        self.occupancy_rate = (self.total_rooms - self.available_rooms) / self.total_rooms
        
        # Remove from current guests
        self.current_guests = [g for g in self.current_guests if g.guest_id != guest_id]
        
        # Record incidental revenue
        if incidental_charges > 0:
            self.other_revenue += incidental_charges
            self.post("cash", "ancillary_revenue", incidental_charges,
                     f"Incidentals: {guest_id}")
            self.income_statement["revenue"] += incidental_charges
        
        return total_bill
    
    def cancel_reservation(self, reservation_id: str) -> float:
        """Cancel reservation and process penalties"""
        reservation = next((r for r in self.reservations if r.reservation_id == reservation_id), None)
        if not reservation:
            return 0.0
        
        cancellation_penalty = 0.0
        
        # Calculate cancellation penalty based on timing
        days_until_arrival = (reservation.check_in_date - date.today()).days
        if days_until_arrival < 1:
            cancellation_penalty = reservation.total_revenue  # full charge
        elif days_until_arrival < 7:
            cancellation_penalty = reservation.total_revenue * 0.50  # 50% penalty
        elif days_until_arrival < 30:
            cancellation_penalty = reservation.total_revenue * 0.25  # 25% penalty
        
        reservation.status = ReservationStatus.CANCELLED
        
        if cancellation_penalty > 0:
            self.post("cash", "cancellation_revenue", cancellation_penalty,
                     f"Cancellation penalty: {reservation_id}")
            self.income_statement["revenue"] += cancellation_penalty
        
        return cancellation_penalty
    
    # Food and beverage operations
    def operate_restaurant(self, restaurant_name: str, covers_served: int) -> float:
        """Operate restaurant service"""
        if restaurant_name not in self.restaurants:
            return 0.0
        
        # Calculate average check based on menu items
        if self.menu_items:
            avg_item_price = sum(item.selling_price for item in self.menu_items) / len(self.menu_items)
            items_per_cover = 2.5  # average items ordered per person
            avg_check = avg_item_price * items_per_cover
        else:
            avg_check = 45.0  # default average check
        
        total_revenue = covers_served * avg_check
        
        # Calculate food costs
        food_cost = total_revenue * self.food_cost_percentage
        
        # Record revenue and costs
        self.food_beverage_revenue += total_revenue
        self.post("cash", "fb_revenue", total_revenue, f"Restaurant: {restaurant_name}")
        self.post("food_costs", "cash", food_cost, f"Food costs: {restaurant_name}")
        
        self.income_statement["revenue"] += total_revenue
        self.income_statement["cogs"] += food_cost
        
        return total_revenue
    
    def operate_bar(self, bar_name: str, drinks_served: int) -> float:
        """Operate bar service"""
        if bar_name not in self.bars:
            return 0.0
        
        avg_drink_price = 12.0  # average beverage price
        total_revenue = drinks_served * avg_drink_price
        
        # Calculate beverage costs
        beverage_cost = total_revenue * self.beverage_cost_percentage
        
        # Record revenue and costs
        self.food_beverage_revenue += total_revenue
        self.post("cash", "beverage_revenue", total_revenue, f"Bar: {bar_name}")
        self.post("beverage_costs", "cash", beverage_cost, f"Beverage costs: {bar_name}")
        
        self.income_statement["revenue"] += total_revenue
        self.income_statement["cogs"] += beverage_cost
        
        return total_revenue
    
    def create_menu_item(self, item: MenuItem) -> str:
        """Add new menu item"""
        self.menu_items.append(item)
        
        # Record menu development costs
        development_cost = 500.0  # recipe development, testing
        self.post("menu_development", "cash", development_cost, f"Menu item: {item.item_id}")
        
        return item.item_id
    
    def update_menu_pricing(self, item_id: str, new_price: float) -> bool:
        """Update menu item pricing"""
        item = next((i for i in self.menu_items if i.item_id == item_id), None)
        if not item:
            return False
        
        old_price = item.selling_price
        item.selling_price = new_price
        
        # Adjust popularity based on price change
        price_change_ratio = new_price / old_price
        if price_change_ratio > 1.1:  # price increase > 10%
            item.popularity_score = max(0.1, item.popularity_score - 0.1)
        elif price_change_ratio < 0.9:  # price decrease > 10%
            item.popularity_score = min(1.0, item.popularity_score + 0.1)
        
        return True
    
    # Event management
    def book_event(self, event: Event) -> str:
        """Book and manage events"""
        # Check facility availability
        if event.expected_attendance > self.ballroom_capacity:
            return ""
        
        self.events_scheduled.append(event)
        
        # Calculate event revenue
        if event.ticket_price > 0:
            event.total_revenue = event.expected_attendance * event.ticket_price
        else:
            event.total_revenue = event.expected_attendance * 100.0  # venue rental
        
        # Record event revenue
        self.event_revenue += event.total_revenue
        self.post("event_deposits", "event_revenue", event.total_revenue * 0.5,
                 f"Event deposit: {event.event_id}")
        
        return event.event_id
    
    def execute_event(self, event_id: str) -> float:
        """Execute scheduled event"""
        event = next((e for e in self.events_scheduled if e.event_id == event_id), None)
        if not event:
            return 0.0
        
        # Record remaining revenue
        remaining_revenue = event.total_revenue * 0.5
        self.post("cash", "event_revenue", remaining_revenue, f"Event execution: {event_id}")
        self.income_statement["revenue"] += remaining_revenue
        
        # Handle catering if required
        catering_revenue = 0.0
        if event.catering_required:
            catering_revenue = self.provide_catering(event_id, event.expected_attendance)
        
        return event.total_revenue + catering_revenue
    
    def provide_catering(self, event_id: str, guest_count: int) -> float:
        """Provide catering services"""
        catering_per_person = 35.0  # average catering cost per person
        total_catering_revenue = guest_count * catering_per_person
        
        # Calculate catering costs
        catering_cost = total_catering_revenue * 0.40  # 40% cost
        
        self.catering_revenue += total_catering_revenue
        self.post("cash", "catering_revenue", total_catering_revenue, f"Catering: {event_id}")
        self.post("catering_costs", "cash", catering_cost, f"Catering costs: {event_id}")
        
        self.income_statement["revenue"] += total_catering_revenue
        self.income_statement["cogs"] += catering_cost
        
        return total_catering_revenue
    
    # Revenue management and pricing
    def _calculate_dynamic_rate(self, check_in_date: date) -> float:
        """Calculate dynamic pricing adjustment"""
        base_adjustment = 1.0
        
        # Seasonal adjustments
        month = check_in_date.strftime("%B")
        if month in self.peak_season:
            base_adjustment *= 1.30  # 30% increase during peak season
        
        # Demand-based adjustments
        forecasted_demand = self.demand_forecasting.get(check_in_date, 0.75)
        if forecasted_demand > 0.90:
            base_adjustment *= 1.20  # 20% increase for high demand
        elif forecasted_demand < 0.50:
            base_adjustment *= 0.85  # 15% decrease for low demand
        
        # Competitor-based adjustments
        avg_competitor_rate = sum(self.competitor_rate_data.values()) / max(len(self.competitor_rate_data), 1)
        if avg_competitor_rate > self.average_daily_rate:
            base_adjustment *= 1.10  # increase if competitors are higher
        
        return base_adjustment
    
    def update_demand_forecast(self, forecast_date: date, demand_level: float) -> None:
        """Update demand forecasting data"""
        self.demand_forecasting[forecast_date] = demand_level
        
        # Adjust pricing strategy based on forecast
        if demand_level > 0.85:
            # High demand - consider rate increases
            rate_increase = min(0.20, (demand_level - 0.85) * 2)
            self.average_daily_rate *= (1 + rate_increase)
    
    def analyze_competitor_rates(self, competitor_data: Dict[str, float]) -> None:
        """Analyze competitor pricing"""
        self.competitor_rate_data.update(competitor_data)
        
        # Adjust pricing position
        avg_competitor_rate = sum(competitor_data.values()) / len(competitor_data)
        rate_gap = avg_competitor_rate - self.average_daily_rate
        
        # Adjust rates if gap is significant
        if abs(rate_gap) > (self.average_daily_rate * 0.15):  # 15% difference
            adjustment = rate_gap * 0.3  # close 30% of the gap
            self.average_daily_rate += adjustment
    
    # Amenity and facility management
    def operate_facility(self, facility_id: str, guest_count: int) -> float:
        """Operate recreational facility"""
        facility = next((f for f in self.facilities if f.facility_id == facility_id), None)
        if not facility:
            return 0.0
        
        # Check capacity
        if guest_count > facility.capacity:
            guest_count = facility.capacity
        
        revenue = guest_count * facility.revenue_per_guest
        
        # Update utilization
        facility.utilization_rate = guest_count / facility.capacity
        
        # Record facility revenue
        self.other_revenue += revenue
        self.post("cash", "facility_revenue", revenue, f"Facility: {facility_id}")
        self.income_statement["revenue"] += revenue
        
        return revenue
    
    def add_amenity(self, amenity_name: str, setup_cost: float) -> bool:
        """Add new amenity"""
        if amenity_name in self.amenities:
            return False
        
        self.amenities.append(amenity_name)
        
        # Record setup costs
        self.post("amenity_setup", "cash", setup_cost, f"Amenity: {amenity_name}")
        
        # Improve guest satisfaction
        self.guest_service_score = min(5.0, self.guest_service_score + 0.1)
        
        return True
    
    def schedule_entertainment(self, event_date: date, entertainment_options: List[str]) -> None:
        """Schedule entertainment for guests"""
        self.entertainment_schedule[event_date] = entertainment_options
        
        # Calculate entertainment costs
        entertainment_cost = len(entertainment_options) * 1000.0  # $1000 per act
        self.post("entertainment_costs", "cash", entertainment_cost, 
                 f"Entertainment: {event_date}")
        self.income_statement["opex"] += entertainment_cost
    
    # Guest service and loyalty
    def enroll_loyalty_member(self, guest_id: str, tier: str) -> bool:
        """Enroll guest in loyalty program"""
        if not self.loyalty_program:
            return False
        
        current_count = self.loyalty_members.get(tier, 0)
        self.loyalty_members[tier] = current_count + 1
        
        # Apply tier benefits
        benefits_cost = {"silver": 25.0, "gold": 50.0, "platinum": 100.0}.get(tier, 0.0)
        if benefits_cost > 0:
            self.post("loyalty_benefits", "cash", benefits_cost, f"Loyalty: {guest_id}")
        
        return True
    
    def handle_guest_complaint(self, guest_id: str, complaint_type: str, resolution_cost: float) -> bool:
        """Handle guest complaint and service recovery"""
        # Record service recovery cost
        self.post("service_recovery", "cash", resolution_cost, f"Complaint: {guest_id}")
        self.income_statement["opex"] += resolution_cost
        
        # Impact on service scores
        if complaint_type == "serious":
            self.guest_service_score = max(1.0, self.guest_service_score - 0.2)
            self.online_review_score = max(1.0, self.online_review_score - 0.1)
        else:
            self.guest_service_score = max(1.0, self.guest_service_score - 0.1)
        
        return True
    
    def conduct_guest_survey(self) -> Dict[str, float]:
        """Conduct guest satisfaction survey"""
        survey_results = {
            "overall_satisfaction": self.guest_service_score,
            "room_quality": self.guest_service_score + 0.1,
            "food_quality": self.guest_service_score - 0.1,
            "staff_service": self.guest_service_score + 0.2,
            "value_for_money": self.guest_service_score - 0.2,
            "amenities": self.guest_service_score
        }
        
        # Update service score
        avg_score = sum(survey_results.values()) / len(survey_results)
        self.guest_service_score = (self.guest_service_score * 0.9 + avg_score * 0.1)
        
        return survey_results
    
    # Seasonal operations
    def adjust_seasonal_operations(self, season: str) -> None:
        """Adjust operations for seasonal changes"""
        if season in self.peak_season:
            # Peak season adjustments
            self.average_daily_rate *= 1.25  # 25% rate increase
            
            # Increase staffing
            for dept, adjustment in self.seasonal_staffing_adjustments.items():
                if dept == "housekeeping":
                    self.housekeeping_staff = int(self.housekeeping_staff * (1 + adjustment))
                elif dept == "food_service":
                    self.food_service_staff = int(self.food_service_staff * (1 + adjustment))
        else:
            # Off-season adjustments
            self.average_daily_rate *= 0.85  # 15% rate decrease
            
            # Reduce staffing
            for dept, adjustment in self.seasonal_staffing_adjustments.items():
                if dept == "housekeeping":
                    self.housekeeping_staff = int(self.housekeeping_staff * (1 - adjustment * 0.5))
                elif dept == "food_service":
                    self.food_service_staff = int(self.food_service_staff * (1 - adjustment * 0.5))
    
    def handle_weather_impact(self, weather_condition: str, impact_severity: float) -> float:
        """Handle weather impact on operations"""
        if not self.weather_dependent_operations:
            return 0.0
        
        revenue_impact = 0.0
        
        if weather_condition in ["hurricane", "blizzard", "severe_storm"]:
            # Major weather events
            cancellation_rate = impact_severity * 0.8  # up to 80% cancellations
            lost_revenue = self.room_revenue * cancellation_rate * 0.1  # daily impact
            revenue_impact = -lost_revenue
            
            # Emergency preparedness costs
            emergency_cost = impact_severity * 10000.0
            self.post("emergency_operations", "cash", emergency_cost, f"Weather: {weather_condition}")
            self.income_statement["opex"] += emergency_cost
        
        return revenue_impact
    
    # Helper methods
    def _check_availability(self, check_in: date, check_out: date, room_type: AccommodationType) -> bool:
        """Check room availability for dates"""
        # Simplified availability check
        occupied_rooms = len([g for g in self.current_guests 
                            if g.accommodation_type == room_type 
                            and g.check_in_date <= check_in < g.check_out_date])
        
        available_rooms_of_type = self.rooms_by_type.get(room_type, 0) - occupied_rooms
        return available_rooms_of_type > 0
    
    def _calculate_incidental_charges(self, guest: Guest) -> float:
        """Calculate incidental charges for guest"""
        # Simulate incidental spending
        base_incidentals = 50.0 * guest.group_size  # $50 per person
        
        # Adjust based on loyalty level
        if guest.loyalty_level == "platinum":
            base_incidentals *= 1.5
        elif guest.loyalty_level == "gold":
            base_incidentals *= 1.2
        
        return base_incidentals
    
    # Analytics and reporting
    def calculate_revpar(self) -> float:
        """Calculate Revenue Per Available Room"""
        if self.total_rooms == 0:
            return 0.0
        
        total_revenue = self.room_revenue + self.food_beverage_revenue + self.other_revenue
        return total_revenue / self.total_rooms
    
    def calculate_adr(self) -> float:
        """Calculate Average Daily Rate"""
        occupied_rooms = self.total_rooms - self.available_rooms
        if occupied_rooms == 0:
            return 0.0
        
        return self.room_revenue / occupied_rooms
    
    def generate_performance_dashboard(self) -> Dict[str, Any]:
        """Generate comprehensive performance metrics"""
        dashboard = {
            "occupancy_metrics": {
                "occupancy_rate": self.occupancy_rate,
                "adr": self.calculate_adr(),
                "revpar": self.calculate_revpar(),
                "available_rooms": self.available_rooms,
                "average_length_stay": self.average_length_stay
            },
            "revenue_breakdown": {
                "room_revenue": self.room_revenue,
                "food_beverage_revenue": self.food_beverage_revenue,
                "event_revenue": self.event_revenue,
                "other_revenue": self.other_revenue,
                "total_revenue": (self.room_revenue + self.food_beverage_revenue + 
                                self.event_revenue + self.other_revenue)
            },
            "guest_metrics": {
                "total_checkins": self.total_checkins,
                "total_checkouts": self.total_checkouts,
                "current_guests": len(self.current_guests),
                "guest_service_score": self.guest_service_score,
                "online_review_score": self.online_review_score
            },
            "operational_metrics": {
                "food_cost_percentage": self.food_cost_percentage,
                "facility_utilization": sum(f.utilization_rate for f in self.facilities) / max(len(self.facilities), 1),
                "events_scheduled": len(self.events_scheduled),
                "loyalty_members": sum(self.loyalty_members.values())
            }
        }
        
        return dashboard