# Device app API

The device app (repository `INVENTARIODATA`) reads a computer's details and adds it to the inventory, or updates it. It talks to these endpoints, implemented in `inventory/agent.py`. All bodies are JSON; errors come back as `{"error": "<key>"}` with an HTTP status, where `<key>` is one of the app's translation keys.

## Signing in

`POST /api/agent/login` with `{"email": "...", "password": "..."}`

- `200`: `{"token": "...", "expiresIn": 3600, "user": {"nombre": "...", "rol": "tech"}}`
- `401 login_err` (wrong email or password), `403 login_off` (deactivated), `403 err_must_change` (must change the password on the website first), `403 err_forbidden` (read-only role), `429 login_locked` (too many attempts; shared with the website's limit), `503 maintenance` (a restore or update is running).

Every other call sends `Authorization: Bearer <token>`. A token lasts an hour. It stops working at once if the account's password changes, the account is deactivated, or its role becomes read-only (`401 err_auth` or `403 err_forbidden`). No cookies are used, so there is no CSRF token.

## Options

`GET /api/agent/options?serial=<serial number>`

```json
{
  "org": "Zoopa", "nextTag": "INV-0018", "hostnameIsTag": false,
  "types": [{"id": "1", "nombre": {"es": "Portátil", "en": "Laptop", "ca": "Portàtil"}, "hasScreen": true, "hasBattery": true, "usesName": false}],
  "locations": [{"id": "1", "nombre": {"es": "Oficina Madrid", "en": "Madrid office", "ca": "Oficina Madrid"}, "tipo": "office"}],
  "existing": {"id": "12", "tag": "INV-0012", "estado": "uso", "typeId": "1", "loc": "1"}
}
```

`existing` is the device with that serial number (ignoring case), or `null`.

## Reporting a computer

`POST /api/agent/report`

```json
{
  "tag": "INV-0018",
  "typeId": "1",
  "loc": "1",
  "facts": { ... }
}
```

`tag`, `typeId` and `loc` are only used when the computer is new. Without them the server uses the next free asset tag, a device type that fits `facts.chassis`, and the storage location. The answer is `{"created": true|false, "device": {...}}`. Errors are `400 err_required` (no serial number, or the inventory has no device types or locations yet) and `409 err_dup` (that asset tag is taken).

### Facts

Every field is optional except `serial`. Unknown fields are ignored, and values outside sensible limits are dropped. Tri-state values are `"yes"`, `"no"`, or `""` for unknown.

| Field | Example | Notes |
|---|---|---|
| `serial` | `"C02XK3JHMD6R"` | Required. Matches an existing device, ignoring case. |
| `hostname` | `"MAD-LT-001"` | Ignored when the hostname is the asset tag (a setting). |
| `manufacturer`, `model` | `"Apple"`, `"MacBook Pro 14\""` | Model list entry, created if new. For types identified by name, it becomes the name. |
| `chassis` | `"laptop"` | `laptop`, `desktop`, `all_in_one` or `unknown`; picks the device type for new computers. |
| `cpu` | `{"name": "Apple M3 Pro", "cores": 11, "maxGhz": 4.05}` | Processor list entry. |
| `ram` | `{"gb": 18, "type": "LPDDR5", "mts": 6400, "replaceable": "no", "modules": 2, "moduleGb": 8, "formFactor": "SO-DIMM"}` | |
| `disks` | `[{"gb": 512, "type": "SSD", "connector": "NVMe", "replaceable": ""}]` | Replaces the drive list. What a person added (form factor, replaceable) is kept for the same position. |
| `gpus` | `[{"name": "NVIDIA RTX 4070", "kind": "dedicated", "vramGb": 12}]` | The first dedicated one, else the first. |
| `screenInches`, `touch` | `14.2`, `"no"` | Only for types with a screen. |
| `battery` | `{"healthPct": 92}` | Only for types with a battery. The previous reading moves to the history. |
| `os` | `{"family": "win", "version": "11 23H2", "edition": "Pro"}` | `family` is `mac`, `win` or `linux`. Linux uses `distro` and `version`. |
| `encryption` | `"yes"` | FileVault, BitLocker or LUKS. |
| `domainJoined` | `"no"` | Active Directory. |
| `nics` | `[{"type": "wifi", "model": "Intel Wi-Fi 6E AX211", "mac": "A4:C3:F0:12:34:56"}]` | `type` is `wifi` or `eth`. Replaces the card list. Wi-Fi generation, Bluetooth and speed are kept for the same MAC address. |
| `agent` | `{"version": "0.1.0", "platform": "macos-aarch64"}` | For information only. |

For an existing computer, only hardware and software details change. Its asset tag, status, location, assignment, purchase data, notes, faults and history stay as they are. Each report is recorded in the activity history, with the account that sent it.
