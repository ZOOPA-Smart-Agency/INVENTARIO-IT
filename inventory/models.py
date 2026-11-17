import re

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models import Q
from django.utils import timezone

TRI = [("", "Not defined"), ("yes", "Yes"), ("no", "No")]
USERNAME_RE = re.compile(r"[a-z0-9._-]{2,150}")


def clean_username(value):
    """A username as stored: lowercase letters, digits, dots, dashes and underscores; "" when not valid."""
    value = str(value or "").strip().lower()
    return value if USERNAME_RE.fullmatch(value) else ""


def suggest_username(email, taken=None):
    """A free username made from the start of an email address: ana.lopez@x.es -> ana.lopez (or ana.lopez2...)."""
    base = re.sub(r"[^a-z0-9._-]", "", str(email or "").split("@")[0].lower())[:140] or "user"
    base = base if len(base) >= 2 else base + "0"
    taken = set(User.objects.exclude(username=None).values_list("username", flat=True)) if taken is None else taken
    name, n = base, 1
    while name in taken:
        n += 1
        name = f"{base}{n}"
    return name


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra):
        email = self.normalize_email(email).lower()
        extra["username"] = clean_username(extra.get("username")) or suggest_username(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra):
        extra.update(rol=User.Role.ADMIN, is_staff=True, is_superuser=True)
        return self.create_user(email, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "admin"
        TECH = "tech"
        READ = "read"

    email = models.EmailField(unique=True)
    # Signs in like the email does; optional, unique, lowercase (see clean_username).
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    nombre = models.CharField(max_length=200)
    rol = models.CharField(max_length=10, choices=Role.choices, default=Role.TECH)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    must_change_password = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre"]


class AppSettings(models.Model):
    """Single row (pk=1) with the organisation-wide settings."""

    org_name = models.CharField(max_length=200, default="Empresa")
    tag_prefix = models.CharField(max_length=20, default="INV-", blank=True)
    # How tag numbers are counted: "type" (separately for each type code) or "global" (once for every device).
    tag_numbering = models.CharField(max_length=10, default="type")
    date_fmt = models.CharField(max_length=10, default="dmy")
    currency = models.CharField(max_length=3, default="EUR")
    warranty_days = models.PositiveIntegerField(default=90)
    hostname_is_tag = models.BooleanField(default=False)

    # Password rules, applied to new and changed passwords.
    pw_enforce = models.BooleanField(default=True)
    pw_min_enabled = models.BooleanField(default=True)
    pw_min_length = models.PositiveIntegerField(default=10)
    pw_upper = models.BooleanField(default=True)
    pw_number = models.BooleanField(default=True)
    pw_symbol = models.BooleanField(default=True)

    # Company logo shown instead of the app icon. Kept in the database so it survives redeploys.
    logo = models.BinaryField(null=True, blank=True)
    logo_type = models.CharField(max_length=40, blank=True)
    logo_version = models.PositiveIntegerField(default=0)

    # Updates installed by themselves at this hour (server time) when a new release is published.
    auto_update = models.BooleanField(default=False)
    auto_update_hour = models.PositiveSmallIntegerField(default=3)

    @classmethod
    def load(cls):
        return cls.objects.get_or_create(pk=1)[0]


# ---- Registrable lists -------------------------------------------------------


class NamedItem(models.Model):
    nombre = models.CharField(max_length=200)

    class Meta:
        abstract = True
        ordering = ["id"]


class TranslatedItem(models.Model):
    """`nombre` is stored as {"es": ..., "en": ..., "ca": ...}."""

    nombre = models.JSONField()

    class Meta:
        abstract = True
        ordering = ["id"]


class DeviceType(TranslatedItem):
    has_screen = models.BooleanField(default=False)
    has_battery = models.BooleanField(default=False)
    uses_name = models.BooleanField(default=False)
    # Goes in the asset tags of this type, after the prefix: Z + LAP + 001. Capital letters and digits only.
    code = models.CharField(max_length=10, blank=True)
    # Words, separated by commas, that make the device app choose this type when the computer's maker or model
    # contains one of them (for example "MacBook" or "Surface, ThinkPad").
    match = models.CharField(max_length=300, blank=True)
    # Also chosen for every computer of this shape ("any", "laptop", "desktop" or "all_in_one"; "" for none), maybe
    # only Apple computers or all but them: so all laptops except Apple ones can go to Portátil, and every Apple
    # computer to a type of its own.
    auto_chassis = models.CharField(max_length=12, blank=True)
    # Which makers that rule covers: "" all, "only" only Apple computers, "except" all but Apple computers.
    auto_apple = models.CharField(max_length=6, blank=True)

    CHASSIS = {"any", "laptop", "desktop", "all_in_one"}
    APPLE = {"", "only", "except"}

    def match_words(self):
        return [w.strip().lower() for w in self.match.replace("\n", ",").split(",") if w.strip()]

    def save(self, *args, **kwargs):
        self.code = "".join(c for c in (self.code or "").upper() if c.isascii() and c.isalnum())[:10]
        if self.auto_chassis not in self.CHASSIS:
            self.auto_chassis = ""
        if self.auto_apple not in self.APPLE:
            self.auto_apple = ""
        super().save(*args, **kwargs)


class Department(TranslatedItem):
    pass


class Location(TranslatedItem):
    tipo = models.CharField(max_length=10, default="office")
    direccion = models.CharField(max_length=300, blank=True)


class DeviceModel(NamedItem):
    fabricante = models.CharField(max_length=100, blank=True)
    type = models.ForeignKey(DeviceType, on_delete=models.PROTECT)


class Cpu(NamedItem):
    cores = models.PositiveIntegerField(null=True, blank=True)
    speed = models.FloatField(null=True, blank=True)
    speed_unit = models.CharField(max_length=5, default="GHz")


class Gpu(NamedItem):
    kind = models.CharField(max_length=12, blank=True)
    vram = models.FloatField(null=True, blank=True)
    vram_unit = models.CharField(max_length=5, default="GB")


class RamGeneration(NamedItem):
    pass


class RamFormFactor(NamedItem):
    pass


class DiskType(NamedItem):
    pass


class DiskFormFactor(NamedItem):
    pass


class DiskConnector(NamedItem):
    pass


class WifiGeneration(NamedItem):
    pass


class BluetoothVersion(NamedItem):
    pass


class MacVersion(NamedItem):
    pass


class WinVersion(NamedItem):
    pass


class WinEdition(NamedItem):
    pass


class LinuxDistro(NamedItem):
    pass


class LinuxVersion(NamedItem):
    distro = models.ForeignKey(LinuxDistro, on_delete=models.PROTECT)


class NicModel(NamedItem):
    type = models.CharField(max_length=5, default="wifi")


# ---- Core records ------------------------------------------------------------


class Employee(models.Model):
    class State(models.TextChoices):
        ACTIVE = "activo"
        LEAVE = "baja"
        LEFT = "salida"  # deliberately no reason: dismissal/resignation is not recorded

    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    dept = models.ForeignKey(Department, null=True, blank=True, on_delete=models.PROTECT)
    loc = models.ForeignKey(Location, null=True, blank=True, on_delete=models.PROTECT)
    alta = models.DateField()
    estado = models.CharField(max_length=10, choices=State.choices, default=State.ACTIVE)
    estado_fecha = models.DateField(null=True, blank=True)
    # A temporary contract or an internship ("prácticas"), rather than a permanent one.
    temporal = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]


class Device(models.Model):
    class State(models.TextChoices):
        IN_USE = "uso"
        AVAILABLE = "disponible"
        REPAIR = "reparacion"
        RETIRED = "descartado"
        LOST = "perdido"

    OS_FAMILIES = [("", "None"), ("mac", "macOS"), ("win", "Windows"), ("linux", "Linux")]

    tag = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100, blank=True)
    serial = models.CharField(max_length=100)
    type = models.ForeignKey(DeviceType, on_delete=models.PROTECT)
    model = models.ForeignKey(DeviceModel, null=True, blank=True, on_delete=models.PROTECT)
    custom_name = models.CharField(max_length=200, blank=True)
    estado = models.CharField(max_length=12, choices=State.choices, default=State.AVAILABLE)
    loc = models.ForeignKey(Location, on_delete=models.PROTECT)

    compra = models.DateField(null=True, blank=True)
    precio = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    proveedor = models.CharField(max_length=200, blank=True)
    factura = models.CharField(max_length=100, blank=True)
    garantia = models.DateField(null=True, blank=True)
    garantia_ext = models.CharField(max_length=3, choices=TRI, blank=True)
    garantia_ended = models.BooleanField(default=False)
    destino = models.CharField(max_length=10, blank=True)
    wipe_cert = models.CharField(max_length=100, blank=True)
    notas = models.TextField(blank=True)

    cpu = models.ForeignKey(Cpu, null=True, blank=True, on_delete=models.PROTECT)
    cpu_rep = models.CharField(max_length=3, choices=TRI, blank=True)
    ram_size = models.FloatField(null=True, blank=True)
    ram_unit = models.CharField(max_length=5, default="GB")
    ram_gen = models.ForeignKey(RamGeneration, null=True, blank=True, on_delete=models.PROTECT)
    ram_speed = models.FloatField(null=True, blank=True)
    ram_speed_unit = models.CharField(max_length=5, default="MT/s")
    ram_rep = models.CharField(max_length=3, choices=TRI, blank=True)
    ram_modules = models.PositiveIntegerField(null=True, blank=True)
    ram_mod_size = models.FloatField(null=True, blank=True)
    ram_mod_unit = models.CharField(max_length=5, default="GB")
    ram_form = models.ForeignKey(RamFormFactor, null=True, blank=True, on_delete=models.PROTECT)
    gpu = models.ForeignKey(Gpu, null=True, blank=True, on_delete=models.PROTECT)

    screen = models.FloatField(null=True, blank=True)
    touch = models.CharField(max_length=3, choices=TRI, blank=True)
    bat_health = models.FloatField(null=True, blank=True)
    bat_date = models.DateField(null=True, blank=True)

    os_family = models.CharField(max_length=5, choices=OS_FAMILIES, blank=True)
    mac_version = models.ForeignKey(MacVersion, null=True, blank=True, on_delete=models.PROTECT)
    win_version = models.ForeignKey(WinVersion, null=True, blank=True, on_delete=models.PROTECT)
    win_edition = models.ForeignKey(WinEdition, null=True, blank=True, on_delete=models.PROTECT)
    linux_distro = models.ForeignKey(LinuxDistro, null=True, blank=True, on_delete=models.PROTECT)
    linux_version = models.ForeignKey(LinuxVersion, null=True, blank=True, on_delete=models.PROTECT)
    oclp = models.CharField(max_length=3, choices=TRI, blank=True)
    hackintosh = models.CharField(max_length=3, choices=TRI, blank=True)
    enc = models.CharField(max_length=3, choices=TRI, blank=True)
    ad = models.CharField(max_length=3, choices=TRI, blank=True)

    class Meta:
        ordering = ["id"]


class Disk(models.Model):
    device = models.ForeignKey(Device, related_name="disks", on_delete=models.CASCADE)
    size = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=5, default="GB")
    type = models.ForeignKey(DiskType, null=True, blank=True, on_delete=models.PROTECT)
    rep = models.CharField(max_length=3, choices=TRI, blank=True)
    form = models.ForeignKey(DiskFormFactor, null=True, blank=True, on_delete=models.PROTECT)
    conn = models.ForeignKey(DiskConnector, null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ["id"]


class NetworkCard(models.Model):
    device = models.ForeignKey(Device, related_name="nics", on_delete=models.CASCADE)
    type = models.CharField(max_length=5, default="wifi")
    model = models.ForeignKey(NicModel, null=True, blank=True, on_delete=models.PROTECT)
    mac = models.CharField(max_length=17, blank=True)
    wifi_gen = models.ForeignKey(WifiGeneration, null=True, blank=True, on_delete=models.PROTECT)
    bt_ver = models.ForeignKey(BluetoothVersion, null=True, blank=True, on_delete=models.PROTECT)
    speed = models.FloatField(null=True, blank=True)
    speed_unit = models.CharField(max_length=5, default="Gbps")

    class Meta:
        ordering = ["id"]


class BatteryReading(models.Model):
    device = models.ForeignKey(Device, related_name="battery_readings", on_delete=models.CASCADE)
    fecha = models.DateField(null=True, blank=True)
    salud = models.FloatField()

    class Meta:
        ordering = ["-id"]


class Assignment(models.Model):
    device = models.ForeignKey(Device, related_name="assignments", on_delete=models.PROTECT)
    employee = models.ForeignKey(Employee, related_name="assignments", on_delete=models.PROTECT)
    desde = models.DateField()
    hasta = models.DateField(null=True, blank=True)
    notas = models.TextField(blank=True)
    condicion = models.CharField(max_length=10, blank=True)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["device"], condition=Q(hasta__isnull=True), name="one_open_assignment_per_device"
            )
        ]


class Incident(models.Model):
    device = models.ForeignKey(Device, related_name="incidents", on_delete=models.PROTECT)
    fecha = models.DateField()
    tipo = models.CharField(max_length=10)
    descripcion = models.TextField()
    estado = models.CharField(max_length=10, default="abierta")
    resuelta = models.DateField(null=True, blank=True)
    piezas = models.CharField(max_length=300, blank=True)
    coste = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    proveedor = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["id"]


class AuditEvent(models.Model):
    """Append-only history. `key` and `args` are rendered in each viewer's language."""

    at = models.DateTimeField(default=timezone.now, editable=False)  # restores keep the original time
    key = models.CharField(max_length=40)
    args = models.JSONField(default=dict)
    device = models.ForeignKey(Device, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-id"]


class Maintenance(models.Model):
    """Single row (pk=1): set while a restore runs, so everyone else sees a maintenance page. Not part of backups."""

    active = models.BooleanField(default=False)
    kind = models.CharField(max_length=20, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    started_by = models.CharField(max_length=200, blank=True)
    phase = models.CharField(max_length=20, blank=True)
    done = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(null=True, blank=True)


class UpdaterState(models.Model):
    """Single row (pk=1) written by the updater service (deploy/updater): it is alive, and what GitHub offers.

    Not part of backups. The web app only sets check_requested; everything else comes from the updater.
    """

    last_seen = models.DateTimeField(null=True, blank=True)
    running_version = models.CharField(max_length=40, blank=True)
    latest_tag = models.CharField(max_length=40, blank=True)
    latest_name = models.CharField(max_length=200, blank=True)
    latest_notes = models.TextField(blank=True)
    latest_url = models.CharField(max_length=300, blank=True)
    latest_published = models.DateTimeField(null=True, blank=True)
    check_status = models.CharField(max_length=20, blank=True)
    checked_at = models.DateTimeField(null=True, blank=True)
    check_requested = models.BooleanField(default=False)


class UpdateJob(models.Model):
    """One installation of a release, asked for by an administrator or by the automatic schedule."""

    class Status(models.TextChoices):
        QUEUED = "queued"
        RUNNING = "running"
        DONE = "done"
        FAILED = "failed"            # nothing was changed
        ROLLED_BACK = "rolled_back"  # the new version did not work; the previous one and its data are back

    created_at = models.DateTimeField(default=timezone.now)
    requested_by = models.CharField(max_length=200, blank=True)
    automatic = models.BooleanField(default=False)
    from_version = models.CharField(max_length=40, blank=True)
    target = models.CharField(max_length=40)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.QUEUED)
    phase = models.CharField(max_length=20, blank=True)
    message = models.TextField(blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]
