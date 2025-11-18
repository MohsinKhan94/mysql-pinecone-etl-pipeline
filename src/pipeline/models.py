from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Package(Base):
    """
    SQLAlchemy model for the 'packages' table.
    """
    __tablename__ = 'packages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    pkgURL = Column(String(500))
    numberOfDays = Column(String(100))
    tourDetail = Column(Text)
    ageRange = Column(String(100))
    isChildFriendly = Column(Boolean)
    isHandicapAccessible = Column(Boolean)
    insurancerequired = Column(Boolean)
    promotionPercentage = Column(String(50))
    seatsPerTour = Column(String(50))
    groupSize = Column(String(50))
    basePrice = Column(String(100))
    singleSupplementPrc = Column(String(100))

    # Relationships to related tables
    moods = relationship("PackageMood", back_populates="package", lazy="select")
    sub_moods = relationship("SubMood", back_populates="package", lazy="select")
    destinations = relationship("Destination", back_populates="package", lazy="select")
    days = relationship("PkgDay", back_populates="package", lazy="select")
    months = relationship("PkgMonth", back_populates="package", lazy="select")
    years = relationship("PkgYear", back_populates="package", lazy="select")
    types = relationship("PkgType", back_populates="package", lazy="select")
    tour_plans = relationship("TourPlan", back_populates="package", lazy="select")
    prices = relationship("NumberTravelerPrice", back_populates="package", lazy="select")
    meals = relationship("MealSummary", back_populates="package", lazy="select")
    transportations = relationship("Transportation", back_populates="package", lazy="select")
    transport_upgrades = relationship("TransportationUpgrade", back_populates="package", lazy="select")

    def to_text(self):
        """
        Concatenates relevant text fields into a single string for embedding.
        """
        parts = [
            f"Package: {self.name}",
            f"URL: {self.pkgURL}",
            f"Duration: {self.numberOfDays}",
            f"Details: {self.tourDetail}",
            f"Age Range: {self.ageRange}",
            f"Promotion: {self.promotionPercentage}",
            f"Group Size: {self.groupSize}",
            f"Base Price: {self.basePrice}",
        ]

        # Add related data if available
        if self.moods:
            mood_list = [mood.mood for mood in self.moods if mood.mood]
            if mood_list:
                parts.append(f"Moods: {', '.join(mood_list)}")

        if self.destinations:
            dest_list = [dest.destination for dest in self.destinations if dest.destination]
            if dest_list:
                parts.append(f"Destinations: {', '.join(dest_list)}")

        if self.types:
            type_list = [type.type for type in self.types if type.type]
            if type_list:
                parts.append(f"Types: {', '.join(type_list)}")

        if self.days:
            day_list = [day.day for day in self.days if day.day]
            if day_list:
                parts.append(f"Available Days: {', '.join(day_list)}")

        if self.months:
            month_list = [month.month for month in self.months if month.month]
            if month_list:
                parts.append(f"Available Months: {', '.join(month_list)}")

        if self.years:
            year_list = [year.year for year in self.years if year.year]
            if year_list:
                parts.append(f"Available Years: {', '.join(year_list)}")

        if self.tour_plans:
            plan_list = [f"{plan.dayNumber}: {plan.detail}" for plan in self.tour_plans if plan.detail]
            if plan_list:
                parts.append(f"Tour Plans: {'; '.join(plan_list[:3])}")  # Limit to first 3 to avoid too much text

        if self.meals:
            meal_list = [f"{meal.mealType}: {meal.detail}" for meal in self.meals if meal.detail]
            if meal_list:
                parts.append(f"Meals: {'; '.join(meal_list)}")

        if self.transportations:
            transport_list = [f"{transport.mode}: {transport.detail}" for transport in self.transportations if transport.detail]
            if transport_list:
                parts.append(f"Transportation: {'; '.join(transport_list)}")

        if self.transport_upgrades:
            upgrade_list = [f"{upgrade.upgradeType}: {upgrade.detail}" for upgrade in self.transport_upgrades if upgrade.detail]
            if upgrade_list:
                parts.append(f"Transportation Upgrades: {'; '.join(upgrade_list)}")

        if self.prices:
            price_list = [f"{price.rangeTitle}: ${price.price}" for price in self.prices if price.rangeTitle and price.price]
            if price_list:
                parts.append(f"Prices: {'; '.join(price_list)}")

        return "\n".join(part for part in parts if part and str(part).strip() != "None" and str(part).strip() != ":")


class PackageMood(Base):
    __tablename__ = 'packageMood'

    id = Column(Integer, primary_key=True, autoincrement=True)
    package_id = Column(Integer, ForeignKey('packages.id'))
    mood = Column(String(255))

    package = relationship("Package", back_populates="moods")


class SubMood(Base):
    __tablename__ = 'subMood'

    id = Column(Integer, primary_key=True, autoincrement=True)
    package_id = Column(Integer, ForeignKey('packages.id'))
    sub_mood = Column(String(255))

    package = relationship("Package", back_populates="sub_moods")


class Destination(Base):
    __tablename__ = 'destinations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    package_id = Column(Integer, ForeignKey('packages.id'))
    destination = Column(String(255))

    package = relationship("Package", back_populates="destinations")


class PkgDay(Base):
    __tablename__ = 'pkgDays'

    id = Column(Integer, primary_key=True, autoincrement=True)
    package_id = Column(Integer, ForeignKey('packages.id'))
    day = Column(String(50))

    package = relationship("Package", back_populates="days")


class PkgMonth(Base):
    __tablename__ = 'pkgMonths'

    id = Column(Integer, primary_key=True, autoincrement=True)
    package_id = Column(Integer, ForeignKey('packages.id'))
    month = Column(String(50))

    package = relationship("Package", back_populates="months")


class PkgYear(Base):
    __tablename__ = 'pkgYears'

    id = Column(Integer, primary_key=True, autoincrement=True)
    package_id = Column(Integer, ForeignKey('packages.id'))
    year = Column(String(50))

    package = relationship("Package", back_populates="years")


class PkgType(Base):
    __tablename__ = 'pkgType'

    id = Column(Integer, primary_key=True, autoincrement=True)
    package_id = Column(Integer, ForeignKey('packages.id'))
    type = Column(String(255))

    package = relationship("Package", back_populates="types")


class TourPlan(Base):
    __tablename__ = 'tourPlan'

    id = Column(Integer, primary_key=True, autoincrement=True)
    package_id = Column(Integer, ForeignKey('packages.id'))
    dayNumber = Column(String(50))
    detail = Column(Text)

    package = relationship("Package", back_populates="tour_plans")


class NumberTravelerPrice(Base):
    __tablename__ = 'numberTravelerPrice'

    id = Column(Integer, primary_key=True, autoincrement=True)
    package_id = Column(Integer, ForeignKey('packages.id'))
    rangeTitle = Column(String(255))
    price = Column(Integer)

    package = relationship("Package", back_populates="prices")


class MealSummary(Base):
    __tablename__ = 'mealSummary'

    id = Column(Integer, primary_key=True, autoincrement=True)
    package_id = Column(Integer, ForeignKey('packages.id'))
    mealType = Column(String(255))
    detail = Column(Text)

    package = relationship("Package", back_populates="meals")


class Transportation(Base):
    __tablename__ = 'transportation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    package_id = Column(Integer, ForeignKey('packages.id'))
    mode = Column(String(255))
    detail = Column(Text)

    package = relationship("Package", back_populates="transportations")


class TransportationUpgrade(Base):
    __tablename__ = 'transportationUpgrade'

    id = Column(Integer, primary_key=True, autoincrement=True)
    package_id = Column(Integer, ForeignKey('packages.id'))
    upgradeType = Column(String(255))
    detail = Column(Text)

    package = relationship("Package", back_populates="transport_upgrades")

