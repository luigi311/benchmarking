import click
from datetime import datetime
from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Manufacturer, Vendor, GPU, CPU, Driver, Benchmark, Run
from presentmon import parse_presetmon


# Helper to get DB session
def get_session():
    cfg = dotenv_values('.env')
    url = cfg.get('DATABASE_URL') or (
        f"{cfg['DB_DIALECT']}://{cfg['DB_USER']}:{cfg['DB_PASS']}@{cfg['DB_HOST']}:{cfg['DB_PORT']}/{cfg['DB_NAME']}"
    )
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

@click.group()
def cli():
    """Benchmark DB Management CLI"""
    pass

@cli.command()
@click.option('--name', prompt='Manufacturer name', type=str)
def add_manufacturer(name):
    """Add a new manufacturer"""
    session = get_session()
    m = Manufacturer(name=name)
    session.add(m)
    session.commit()
    click.echo(f"Created Manufacturer ID={m.id}")
    session.close()

@cli.command()
@click.option('--name', 'card_name', prompt='Graphic card vendor name')
@click.option('--model', prompt='Graphic card model')
@click.option('--manufacturer-id', type=int, help='Existing manufacturer ID (skip selection)')
@click.option('--vendor-id', type=int, help='Existing vendor ID (skip selection)')
def add_gpu(card_name, model, manufacturer_id, vendor_id):
    """Add a new graphic card"""
    session = get_session()
    # select manufacturer if not provided
    if manufacturer_id is None:
        mans = session.query(Manufacturer).all()
        for m in mans:
            click.echo(f"{m.id}: {m.name}")
        manufacturer_id = int(click.prompt('Select manufacturer by ID', type=click.Choice([str(m.id) for m in mans]), show_choices=False))
    # select vendor if not provided
    if vendor_id is None:
        vens = session.query(Vendor).all()
        for v in vens:
            click.echo(f"{v.id}: {v.name}")
        vendor_id = int(click.prompt('Select vendor by ID', type=click.Choice([str(v.id) for v in vens]), show_choices=False))

    gc = GPU(
        manufacturer_id=manufacturer_id,
        vendor_id=vendor_id,
        name=card_name,
        model=model
    )
    session.add(gc)
    session.commit()
    click.echo(f"Created GPU ID={gc.id}")
    session.close()

@cli.command()
@click.option('--model', prompt='CPU model')
@click.option('--manufacturer-id', type=int, help='Existing manufacturer ID (skip selection)')
def add_cpu(model, manufacturer_id):
    """Add a new CPU"""
    session = get_session()
    if manufacturer_id is None:
        mans = session.query(Manufacturer).all()
        for m in mans:
            click.echo(f"{m.id}: {m.name}")
        manufacturer_id = int(click.prompt('Select manufacturer by ID', type=click.Choice([str(m.id) for m in mans]), show_choices=False))
    cpu = CPU(manufacturer_id=manufacturer_id, model=model)
    session.add(cpu)
    session.commit()
    click.echo(f"Created CPU ID={cpu.id}")
    session.close()


@cli.command()
@click.option('--version', prompt='Driver version')
@click.option('--manufacturer-id', type=int, help='Existing manufacturer ID (skip selection)')
def add_driver(version, manufacturer_id):
    """Add a new driver"""
    session = get_session()
    if manufacturer_id is None:
        mans = session.query(Manufacturer).all()
        for m in mans:
            click.echo(f"{m.id}: {m.name}")
        manufacturer_id = int(click.prompt('Select manufacturer by ID', type=click.Choice([str(m.id) for m in mans]), show_choices=False))
    d = Driver(manufacturer_id=manufacturer_id, version=version)
    session.add(d)
    session.commit()
    click.echo(f"Created Driver ID={d.id}")
    session.close()

@cli.command()
@click.option('--name', prompt='Vendor name', type=str)
def add_vendor(name):
    """Add a new vendor"""
    session = get_session()
    v = Vendor(name=name)
    session.add(v)
    session.commit()
    click.echo(f"Created Vendor ID={v.id}")
    session.close()

@cli.command()
@click.option('--application', prompt='Application name')
@click.option('--version', prompt='Application version')
@click.option('--settings', prompt='Settings')
@click.option('--resolution', prompt='Resolution')
def add_benchmark(application, version, settings, resolution):
    """Add a new benchmark application"""
    session = get_session()
    b = Benchmark(application=application, version=version, settings=settings, resolution=resolution)
    session.add(b)
    session.commit()
    click.echo(f"Created Benchmark ID={b.id}")
    session.close()

@cli.command()
@click.option('--benchmark-id', type=int, help='Existing benchmark ID')
@click.option('--gpu-id', type=int, help='Existing GPU ID')
@click.option('--driver-id', type=int, help='Existing driver ID')
@click.option('--cpu-id', type=int, help='Existing CPU ID')
@click.option('--run-date', prompt='Run date', default=lambda: datetime.utcnow().date(), show_default=True)
@click.option('--csv-file', prompt='PresentMon CSV file path', type=click.Path(exists=True))
def add_run(benchmark_id, gpu_id, driver_id, cpu_id, run_date, csv_file):
    """Add a new run and import PresentMon results"""
    session = get_session()
    # interactive selection for foreign keys if not provided
    if benchmark_id is None:
        items = session.query(Benchmark).all()
        for i in items:
            click.echo(f"{i.id}: {i.application} v{i.version} {i.resolution} {i.settings}")
        benchmark_id = int(click.prompt('Select benchmark by ID', type=click.Choice([str(i.id) for i in items]), show_choices=False))
    if gpu_id is None:
        items = session.query(GPU).all()
        for i in items:
            click.echo(f"{i.id}: {i.name} ({i.model})")
        gpu_id = int(click.prompt('Select gpu by ID', type=click.Choice([str(i.id) for i in items]), show_choices=False))
    if driver_id is None:
        items = session.query(Driver).all()
        for i in items:
            click.echo(f"{i.id}: {i.version}")
        driver_id = int(click.prompt('Select driver by ID', type=click.Choice([str(i.id) for i in items]), show_choices=False))
    if cpu_id is None:
        items = session.query(CPU).all()
        for i in items:
            click.echo(f"{i.id}: {i.model}")
        cpu_id = int(click.prompt('Select CPU by ID', type=click.Choice([str(i.id) for i in items]), show_choices=False))

    r = Run(
        benchmark_id=benchmark_id,
        gpu_id=gpu_id,
        driver_id=driver_id,
        cpu_id=cpu_id,
        run_date=run_date
    )
    session.add(r)
    session.flush()  # get r.id
    parse_presetmon(session, csv_file, r.id)
    session.commit()
    click.echo(f"Created Run ID={r.id} and imported results.")
    session.close()


if __name__ == '__main__':
    cli()