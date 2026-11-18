# Device app API

The device app (repository `INVENTARIODATA`) reads a computer's details and adds it to the inventory, or updates it. It talks to these endpoints, implemented in `inventory/agent.py`. All bodies are JSON; errors come back as `{"error": "<key>"}` with an HTTP status, where `<key>` is one of the app's translation keys.

## Signing in

`POST /api/agent/login` with `{"email": "...", "password": "..."}`. From 1.7.0, `email` can also be the account's username.

- `200`: `{"token": "...", "expiresIn": 3600, "user": {"nombre": "...", "rol": "tech"}}`
- `401 login_err` (wrong email, username or password), `403 login_off` (deactivated), `403 err_must_change` (must change the password on the website first), `403 err_forbidden` (read-only role), `429 login_locked` (too many attempts; shared with the website's limit), `503 maintenance` (a restore or update is running).

Every other call sends `Authorization: Bearer <token>`. A token lasts an hour. It stops working at once if the account's password changes, the account is deactivated, or its role becomes read-only (`401 err_auth` or `403 err_forbidden`). No cookies are used, so there is no CSRF token.

## Options

`GET /api/agent/options?serial=<serial number>&chassis=<chassis>&model=<model>&manufacturer=<maker>&hostname=<name>` (all but `serial` are optional)

```json
{
  "org": "Zoopa", "nextTag": "ZLAP018", "hostnameIsTag": false,
  "types": [{"id": "1", "nombre": {"es": "Portátil", "en": "Laptop", "ca": "Portàtil"}, "hasScreen": true, "hasBattery": true, "usesName": false,
             "code": "LAP", "match": ["thinkpad", "latitude"], "autoChassis": "laptop", "autoApple": "except",
             "nextTag": "ZLAP018"}],
  "locations": [{"id": "1", "nombre": {"es": "Oficina Madrid", "en": "Madrid office", "ca": "Oficina Madrid"}, "tipo": "office"}],
  "existing": {"id": "12", "tag": "INV-0012", "estado": "uso", "typeId": "1", "loc": "1"}
}
```

`existing` is the device with that serial number (ignoring case), or `null`.

`hostnameTag` (from 1.10.0, when `hostname` is given) says whether the computer's name can be its asset tag, for inventories where **Settings > General** makes the hostname the tag (`hostnameIsTag`): `{"name": "zlap004", "tag": "ZLAP004", "valid": true, "usedBy": null, "matches": false}`. `valid` means it follows the tags' pattern (the prefix, a device type's code or none, and a number); `tag` is that name written as a tag; `usedBy` is the tag of another device that has it or the same identifier; `matches` says whether it is already the tag of the computer with that serial number. When `hostnameIsTag` is on and a new computer is reported without a `tag`, a valid, free name becomes its tag.

Each type's `nextTag` is the asset tag its next device gets: the tag prefix, the type's `code` and a number one higher than the highest in use (`ZLAP018`). That number is counted for each code, or across every device when **Settings > General > Tag numbering** is global. Types without a code use the prefix and a plain number (`INV-0018`). The top-level `nextTag` is the one for the type the server would choose from `chassis` and `model` (see below).

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

`tag`, `typeId` and `loc` are only used when the computer is new. Without them the server picks a device type in this order: one whose `match` words (set in **Settings > Device types**) appear in `facts.manufacturer` or `facts.model`; one whose name appears there (a "MacBook Air" is a "MacBook"); the first one set to take every computer of that `facts.chassis` (`autoChassis`), then the first set to take computers of any shape (`autoChassis` `"any"`), in both cases skipping types whose `autoApple` is `"only"` when this is not an Apple computer, or `"except"` when it is (Apple means made by Apple, or a model starting with "Mac", "MacBook" or "iMac"); one that fits `facts.chassis` by having a screen or battery. Whole words only, ignoring case, and the longest matching word wins. Then it uses that type's next asset tag, and the storage location. The answer is `{"created": true|false, "device": {...}}`. Errors are `400 err_required` (no serial number, or the inventory has no device types or locations yet) and `409 err_dup` (that asset tag is taken, ignoring case, or so is its number: `ZLAP01` and `ZLAP001` are the same, and with global numbering so is `ZMB001`).

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
| `disks` | `[{"gb": 512, "type": "SSD", "connector": "NVMe", "replaceable": "yes"}]` | Replaces the drive list. What a person added (form factor, replaceable) is kept for the same position when the app does not know. From device app 0.8.0, `replaceable` is filled in: on Macs from the model (soldered on Apple silicon, T2 Macs, the 12-inch MacBook and the 2016-2017 MacBook Pro with Touch Bar), elsewhere from the connection (SATA and M.2 NVMe yes; eMMC, UFS and soldered "BGA" NVMe no). | From device app 0.9.0, `connector` says the generation when the system reports it (`SATA III` from macOS and Linux, `NVMe PCIe 4.0` from Linux), and `formFactor` (`2.5"`, `3.5"`, `M.2`, `Apple (propietario)`) is sent where the model or kind of drive settles it; both match existing list entries by name, ignoring case. |
| `gpus` | `[{"name": "NVIDIA RTX 4070", "kind": "dedicated", "vramGb": 12}]` | The first dedicated one, else the first. |
| `screenInches`, `touch` | `14.2`, `"no"` | Only for types with a screen. |
| `battery` | `{"healthPct": 92}` | Only for types with a battery. The previous reading moves to the history. |
| `os` | `{"family": "win", "version": "11 23H2", "edition": "Pro"}` | `family` is `mac`, `win` or `linux`. Linux uses `distro` and `version`. |
| `oclp` | `"2.1.0"` | Macs only, from device app 0.8.0 (and inventory 1.11.0): OpenCore Legacy Patcher's version when the Mac starts through it, `"yes"` when it starts through OpenCore without saying which version, `""` when it does not. Sets "Patched with OCLP" and its version. Left out by older apps, which then change neither. |
| `encryption` | `"yes"` | FileVault, BitLocker or LUKS. |
| `domainJoined` | `"no"` | Active Directory. |
| `nics` | `[{"type": "wifi", "model": "Intel Wi-Fi 6E AX211", "mac": "A4:C3:F0:12:34:56", "wifiGen": "6E", "btVer": "5.3"}]` | `type` is `wifi` or `eth`. Replaces the card list. `wifiGen` (`4`, `5`, `6`, `6E` or `7`) and `btVer` (`5.3`) are Wi-Fi only, and match list entries such as "Wi-Fi 6 (802.11ax)" or "Bluetooth 5.3", created if missing. Whatever is not sent (generation, Bluetooth, speed, model) is kept from the card with the same MAC address.. From device app 0.9.0 (inventory 1.15.0), Ethernet ports send `speedMbps`, the fastest speed the port supports (1000 is saved as 1 Gbps); macOS also sends the Ethernet chip as `model`.. From device app 0.9.0, USB adapters and docks are not sent: they are not the computer's own cards. |
| `agent` | `{"version": "0.1.0", "platform": "macos-aarch64"}` | For information only. |

For an existing computer, only hardware and software details change. Its asset tag, status, location, assignment, purchase data, notes, faults and history stay as they are. Each report is recorded in the activity history, with the account that sent it.
