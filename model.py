from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Apartment(Base):
    __tablename__='apartment'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    price: Mapped[float] = mapped_column(nullable=False)
    currency_id: Mapped[int] = mapped_column(ForeignKey('currency.id'))
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    main_area_id: Mapped[int] = mapped_column(ForeignKey('main_area.id'))
    second_area_id: Mapped[int] = mapped_column(ForeignKey('second_area.id'))
    street_id: Mapped[int] = mapped_column(ForeignKey('street.id'))
    subway: Mapped[bool | None]
    total_square: Mapped[float | None]
    kitchen_square: Mapped[float | None]
    living_square: Mapped[float | None]
    room: Mapped[int | None]
    total_floor: Mapped[int | None]
    flat_floor: Mapped[int | None]
    deal_type_id: Mapped[int] = mapped_column(ForeignKey('deal_type.id'))
    checked_apartment: Mapped[bool | None]
    animal: Mapped[bool | None]
    newbuild_id: Mapped[int] = mapped_column(ForeignKey('newbuild.id'))
    agency_id: Mapped[int] = mapped_column(ForeignKey('agency.id'))
    photo_count: Mapped[int | None]
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(unique=True)
    publication_date: Mapped[datetime.date] = mapped_column(Date)
    parse_date: Mapped[datetime.date] = mapped_column(Date)
    description: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(nullable=False)
    no_active_date: Mapped[datetime.date] = mapped_column(Date)
    apartment_currency: Mapped['Currency'] = relationship(back_populates='currency_apartment')
    apartment_deal_type: Mapped['DealType'] = relationship(back_populates='deal_type_apartment')
    apartment_city: Mapped['City'] = relationship(back_populates='city_apartment')
    apartment_agency: Mapped['Agency'] = relationship(back_populates='agency_apartment')
    apartment_newbuild: Mapped['Newbuild'] = relationship(back_populates='newbuild_apartment')
    apartment_main_area: Mapped['MainArea'] = relationship(back_populates='main_area_apartment')
    apartment_second_area: Mapped['SecondArea'] = relationship(back_populates='second_area_apartment')
    apartment_street: Mapped['Street'] = relationship(back_populates='street_apartment')


class StatTable(Base):
    __tablename__ = 'stat_table'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    parse_date: Mapped[datetime.date] = mapped_column(Date)
    num_ads: Mapped[int] = mapped_column(nullable=False)
    stat_city: Mapped['City'] = relationship(back_populates='city_stat')


class City(Base):
    __tablename__='city'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    city_agency: Mapped['Agency'] = relationship(back_populates='agency_city')
    city_main_area: Mapped['MainArea'] = relationship(back_populates='main_area_city')
    city_second_area: Mapped['SecondArea'] = relationship(back_populates='second_area_city')
    city_street: Mapped['Street'] = relationship(back_populates='street_city')
    city_newbuild: Mapped['Newbuild'] = relationship(back_populates='newbuild_city')
    city_stat: Mapped['StatTable'] = relationship(back_populates='stat_city')
    city_apartment: Mapped['Apartment'] = relationship(back_populates='apartment_city')


class Agency(Base):
    __tablename__='agency'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    name: Mapped[str] = mapped_column(nullable=False)
    agency_city: Mapped['City'] = relationship(back_populates='city_agency')
    agency_apartment: Mapped['Apartment'] = relationship(back_populates='apartment_agency')


class Currency(Base):
    __tablename__='currency'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str | None]
    currency_apartment: Mapped['Apartment'] = relationship(back_populates='apartment_currency')


class DealType(Base):
    __tablename__='deal_type'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    deal_type_apartment: Mapped['Apartment'] = relationship(back_populates='apartment_deal_type')


class MainArea(Base):
    __tablename__='main_area'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    name: Mapped[str] = mapped_column(nullable=False)
    main_area_city: Mapped['City'] = relationship(back_populates='city_main_area')
    main_area_apartment: Mapped['Apartment'] = relationship(back_populates='apartment_main_area')


class SecondArea(Base):
    __tablename__='second_area'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    name: Mapped[str] = mapped_column(nullable=False)
    second_area_city: Mapped['City'] = relationship(back_populates='city_second_area')
    second_area_apartment: Mapped['Apartment'] = relationship(back_populates='apartment_second_area')


class Newbuild(Base):
    __tablename__='newbuild'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    name: Mapped[str] = mapped_column(nullable=False)
    newbuild_city: Mapped['City'] = relationship(back_populates='city_newbuild')
    newbuild_apartment: Mapped['Apartment'] = relationship(back_populates='apartment_newbuild')


class Street(Base):
    __tablename__='street'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    name: Mapped[str] = mapped_column(nullable=False)
    street_city: Mapped['City'] = relationship(back_populates='city_street')
    street_apartment: Mapped['Apartment'] = relationship(back_populates='apartment_street')