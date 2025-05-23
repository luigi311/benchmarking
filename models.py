from sqlalchemy import BigInteger, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Manufacturer(Base):
    __tablename__ = 'manufacturers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Vendor(Base):
    __tablename__ = 'vendors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class GPU(Base):
    __tablename__ = 'gpus'
    id = Column(Integer, primary_key=True)
    manufacturer_id = Column(Integer, ForeignKey('manufacturers.id'), nullable=False)
    vendor_id = Column(Integer, ForeignKey('vendors.id'), nullable=False)
    name = Column(String, nullable=False)
    model = Column(String, nullable=False)

class CPU(Base):
    __tablename__ = 'cpus'
    id = Column(Integer, primary_key=True)
    manufacturer_id = Column(Integer, ForeignKey('manufacturers.id'), nullable=False)
    model = Column(String, nullable=False)

class Driver(Base):
    __tablename__ = 'drivers'
    id = Column(Integer, primary_key=True)
    manufacturer_id = Column(Integer, ForeignKey('manufacturers.id'), nullable=False)
    version = Column(String, nullable=False)

class Benchmark(Base):
    __tablename__ = 'benchmarks'
    id = Column(Integer, primary_key=True)
    application = Column(String, nullable=False)
    version = Column(String, nullable=False)
    settings = Column(String)
    resolution = Column(String)

class Run(Base):
    __tablename__ = 'runs'
    id = Column(Integer, primary_key=True)
    benchmark_id = Column(Integer, ForeignKey('benchmarks.id'), nullable=False)
    gpu_id = Column(Integer, ForeignKey('gpus.id'), nullable=False)
    driver_id = Column(Integer, ForeignKey('drivers.id'), nullable=False)
    cpu_id = Column(Integer, ForeignKey('cpus.id'), nullable=False)
    run_date = Column(Date)

class Result(Base):
    __tablename__ = 'results'
    run_id = Column(Integer, ForeignKey('runs.id'), primary_key=True)
    sample_time_ms = Column(Integer, primary_key=True)
    frame_time = Column(Float)
    cpu_busy = Column(Float)
    cpu_wait = Column(Float)
    gpu_latency = Column(Float)
    gpu_time = Column(Float)
    gpu_busy = Column(Float)
    gpu_wait = Column(Float)
    display_latency = Column(Float)
    gpu_power = Column(Float)
    gpu_voltage = Column(Float)
    gpu_frequency = Column(Float)
    gpu_temperature = Column(Float)
    gpu_utilization = Column(Float)
    gpu_memory_frequency = Column(Float)
    gpu_memory_size_used = Column(BigInteger)
    gpu_fan_speed_0 = Column(Integer)
    gpu_fan_speed_1 = Column(Integer)
    gpu_fan_speed_2 = Column(Integer)
    gpu_fan_speed_3 = Column(Integer)
    cpu_utilization = Column(Float)
    cpu_power = Column(Float)
    cpu_temperature = Column(Float)
    cpu_frequency = Column(Float)
