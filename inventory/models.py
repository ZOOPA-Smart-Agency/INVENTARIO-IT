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
    # The profile picture's version: 0 without one; it changes with every upload, so its address does too.
    photo_version = models.PositiveIntegerField(default=0)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre"]


class ProfilePhoto(models.Model):
    """An account's profile picture: a 256-pixel square JPEG, made by the server from the uploaded image.
    Kept apart from User so loading accounts never loads pictures."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="photo")
    data = models.BinaryField()


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
    # Devices without disk encryption are shown as a problem (Overview, the device's page); off: only noted.
    require_encryption = models.BooleanField(default=True)
    # The activity log's largest size in MB (0: no limit); past it the oldest entries are deleted (see logsize.py).
    log_max_mb = models.PositiveIntegerField(default=0)

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
    # How the logo is shown: "" as uploaded, "app" cropped to the app icon's rounded square, "circle"
    logo_shape = models.CharField(max_length=10, blank=True, default="")

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
    # Someone can belong to several departments and work from several offices.
    depts = models.ManyToManyField(Department, blank=True, related_name="employees")
    locs = models.ManyToManyField(Location, blank=True, related_name="employees")
    alta = models.DateField()
    estado = models.CharField(max_length=10, choices=State.choices, default=State.ACTIVE)
    estado_fecha = models.DateField(null=True, blank=True)
    class Contract(models.TextChoices):
        UNSET = "", "Not defined"
        PERMANENT = "indefinido"
        TEMPORARY = "temporal"
        INTERNSHIP = "practicas"

    contrato = models.CharField(max_length=10, choices=Contract.choices, default=Contract.UNSET, blank=True)

    class Meta:
        ordering = ["id"]


class Device(models.Model):
    class State(models.TextChoices):
        IN_USE = "uso"
        AVAILABLE = "disponible"
        REPAIR = "reparacion"
        FAULTY = "averiado"  # broken and unusable, not yet sent for repair, replaced or retired
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
    # data checks someone looked at and chose to ignore for this device (their keys, as the web app names them)
    checks_ignored = models.JSONField(default=list, blank=True)

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
    bat_cycles = models.PositiveIntegerField(null=True, blank=True)  # full charge cycles, as the device app reports them

    os_family = models.CharField(max_length=5, choices=OS_FAMILIES, blank=True)
    mac_version = models.ForeignKey(MacVersion, null=True, blank=True, on_delete=models.PROTECT)
    win_version = models.ForeignKey(WinVersion, null=True, blank=True, on_delete=models.PROTECT)
    win_edition = models.ForeignKey(WinEdition, null=True, blank=True, on_delete=models.PROTECT)
    linux_distro = models.ForeignKey(LinuxDistro, null=True, blank=True, on_delete=models.PROTECT)
    linux_version = models.ForeignKey(LinuxVersion, null=True, blank=True, on_delete=models.PROTECT)
    oclp = models.CharField(max_length=3, choices=TRI, blank=True)
    oclp_version = models.CharField(max_length=20, blank=True)  # OpenCore Legacy Patcher's version, when known
    os_number = models.CharField(max_length=20, blank=True)  # the exact system version with its updates ("26.2.1"); macOS
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
    # what the drive says about itself (SMART), as the device app reports it; nobody types these
    health = models.CharField(max_length=10, blank=True)  # "ok", "warning", "failing"
    wear = models.FloatField(null=True, blank=True)  # SSDs: percent of rated life used
    hours = models.PositiveIntegerField(null=True, blank=True)  # hours powered on
    checked = models.DateField(null=True, blank=True)  # when the device app last read them

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
    ciclos = models.PositiveIntegerField(null=True, blank=True)


class DiskReading(models.Model):
    """An earlier health reading of one of a device's drives, kept when a newer one differs (to see wear grow)."""
    device = models.ForeignKey(Device, related_name="disk_readings", on_delete=models.CASCADE)
    fecha = models.DateField(null=True, blank=True)
    drive = models.CharField(max_length=60)  # "512 GB SSD", to tell the device's drives apart
    health = models.CharField(max_length=10, blank=True)
    wear = models.FloatField(null=True, blank=True)
    hours = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    class Meta:
        ordering = ["-id"]


class Assignment(models.Model):
    device = models.ForeignKey(Device, related_name="assignments", on_delete=models.PROTECT)
    # who has it: a person, or a whole department (a shared device); exactly one of the two
    employee = models.ForeignKey(Employee, related_name="assignments", null=True, blank=True, on_delete=models.PROTECT)
    dept = models.ForeignKey(Department, related_name="assignments", null=True, blank=True, on_delete=models.PROTECT)
    desde = models.DateField()
    hasta = models.DateField(null=True, blank=True)
    notas = models.TextField(blank=True)
    condicion = models.CharField(max_length=10, blank=True)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["device"], condition=Q(hasta__isnull=True), name="one_open_assignment_per_device"
            ),
            models.CheckConstraint(
                condition=Q(employee__isnull=False, dept__isnull=True) | Q(employee__isnull=True, dept__isnull=False),
                name="assignment_to_a_person_or_a_department",
            ),
        ]

    @property
    def holder_name(self):
        """The person's name, or the department's (a translated name, as the activity log expects)."""
        return self.employee.nombre if self.employee_id else self.dept.nombre


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
        # newest first by when it happened: some entries are written after the fact (how an update ended, at the
        # time it did); the id settles entries of the same moment
        ordering = ["-at", "-id"]
        indexes = [models.Index(fields=["-at", "-id"], name="auditevent_newest")]


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
