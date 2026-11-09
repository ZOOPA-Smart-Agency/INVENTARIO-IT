# Handoff: device inventory web app (prototype)

Paste this whole file into the new session, and put `inventario.html` and `documento-planificacion.txt` (in this same folder) into the project folder. Everything below describes the state at the end of the previous session.

---

## 1. What this is

The user is building a **web app to manage the company's device inventory**: laptops, desktops and all-in-ones, the employees who hold them, faults/repairs, warranty, hardware/software specs.

- The company is Spanish (Madrid and Barcelona offices). The user writes to Claude in **English**, but the app's main language is **Spanish**, and it also has **Catalan** and **English**.
- The user keeps a **planning document** in Spanish (Word file, "Aplicación web para gestionar inventario de dispositivos dentro de una empresa"). They send updated versions and expect the app to **follow the document**, and they want Claude to **point out mistakes or disagreements** with it. The latest version's text is in `documento-planificacion.txt`.
- So far everything is a **clickable front-end prototype** in a single HTML file, used to settle screens, fields and flows before building the real app.

## 2. Files and where things live

| Thing | Where |
|---|---|
| The prototype (single file, ~2,900 lines, HTML + CSS + JS, no build step) | `inventario.html` |
| Published copy (claude.ai artifact, shared "anyone with the link") | https://claude.ai/artifact/EZSWJuvxeNrcGqG1EDXTGy |
| Latest planning document (plain-text export) | `documento-planificacion.txt` |

**To run it:** open `inventario.html` in a browser. The only external resource is Google Fonts, used by the Classic design.

**Saved data** is in the browser's `localStorage`:
- `inventario-prototipo-v5`: all app data
- `inventario-prefs`: language, theme, design, the `uiChosen` flag and the session

The footer button "Restablecer datos de ejemplo" reloads the example data.

**Demo sign-in accounts** (password `demo`, simulated in the browser only):

| Email | Role |
|---|---|
| admin@empresa.es | Administrator: everything, including Settings |
| it@empresa.es | IT technician: devices, employees, faults; no Settings |
| lectura@empresa.es | Read only |

If the new session publishes to the same artifact link, it must pass that URL. Otherwise, edit the local file.

## 3. How the user likes to work

- **Short, specific requests**, often with screenshots from their Mac (Chrome). They care a lot about polish: alignment, centring, consistent wording, Apple-like feel.
- **Test changes in a real browser before reporting.** In the previous session every change was checked with Playwright scripts (see section 10). Report what was tested and anything that couldn't be.
- **Keep their saved data** when the data shape changes: `load()` contains migrations for that. Only reset the example data when unavoidable, and say so.
- **Every user-facing text in all three languages.** The key sets must stay identical (see section 9).
- **Privacy:** the user explicitly does **not** want to record whether an employee was dismissed or resigned. That's a sensitive HR matter, and this app is about devices. Leaving the company is a single neutral status: "Ha dejado la empresa".
- **Button wording:** a form's main button is one short verb (Añadir / Guardar / Registrar / Resolver / Asignar). Page-level buttons keep the full wording ("Nuevo dispositivo", "Registrar avería").
- **Classic design must never be removed.** Glass is the default, but Classic stays switchable.

## 4. Planning document (latest): what it asks for

**Devices**
- Purchase date, purchase price, supplier, invoice number (all optional); company identifier (asset tag).
- **Warranty:**
  - end date and time remaining (the extension's date if extended)
  - extended yes/no
  - "ended, date unknown" option
- **Status:**
  - Disponible, En uso, En reparación, Perdido/Robado, and reason/notes
  - Descartado, with a destination (Reciclado, Venta, Donación, Devuelto a la empresa que lo alquilaba) and an optional data destruction certificate
- **Faults:** date, type, description, parts replaced (optional), cost.
- **Employee history:** employee, start and end of possession, faults during their possession.

**Device types**

| Type | Fields |
|---|---|
| Portátil (laptop) | model, inches, touchscreen, serial number, battery health + date measured |
| Sobremesa premontado (prebuilt desktop) | model, serial number |
| Sobremesa Custom (custom-built desktop) | optional **name** instead of a model |
| Todo en uno (all-in-one) | model, inches, touchscreen, serial number |

**Specs** ("registrable" means a reusable list in Settings, with **+** in forms)

| Part | Fields |
|---|---|
| Processor | model (registrable), max frequency MHz/GHz, cores, replaceable |
| RAM | capacity TB/GB/MB, generation (registrable), frequency MHz/MT/s, replaceable. If replaceable: number of modules, capacity per module, form factor (registrable) |
| Storage, **per drive** | capacity GB/TB, type SSD/HDD/eMMC (registrable), replaceable. If replaceable: form factor (registrable), connector (registrable) |
| Graphics | model (registrable), integrated/dedicated, VRAM MB/GB |
| Network cards | model (registrable, optional), MAC. Wi-Fi: generation (registrable), Bluetooth version (registrable). Ethernet: speed Mbps/Gbps |

**Software**
- **macOS:** version (registrable), patched with OCLP, Hackintosh, FileVault
- **Windows:** version (registrable), edition (registrable), BitLocker
- **Linux:** distribution (registrable), version (registrable and tied to the distribution), LUKS
- **All systems:** joined to Active Directory

**Employees:** full name, work email, department (registrable), location (registrable), start date, devices held; status Activo / Baja temporal / Despedido/Dimitido. The app shows the last one as the neutral "Ha dejado la empresa", with no reason (see section 3).

## 5. What the prototype does

- **Sign-in and roles** (simulated). The header/sidebar shows the user; the account menu has Settings (admins only), Language (ES/CA/EN), Theme (system/light/dark), Design (Classic/Glass) and Sign out.
- **Overview:**
  - counts by status (numbers count up)
  - "Needs attention" alerts: devices held by people who left; open faults; warranties ending within N days (set in Settings); devices with encryption = no; batteries under 80%
  - devices in use by department
  - recent activity with who did it
- **Devices list:** search (tag, hostname, serial, OS, CPU, GPU, MACs, model/name, person) and filters by status, department and type.
- **Device page:**
  - current assignment
  - hardware and software (OS with OCLP/Hackintosh labels, encryption labelled BitLocker/FileVault/LUKS by OS, Active Directory)
  - screen/battery (only for types that have them), with earlier battery readings kept as history
  - network cards, purchase and warranty
  - notes
  - user history with faults during each person's possession
  - faults table with a "Held by" column
- **Device actions:** Assign, Record return (condition, next status), Log fault (optionally send to repair), Resolve fault, Change status (destination + data destruction certificate when retiring), Edit.
- **Device form:**
  - type first; then a model list filtered by type, or an optional name for types marked "identified by name"
  - type-dependent screen and battery fields
  - registrable lists with **+** quick-add: the new entry starts with the right type/distribution and is selected straight away
  - replaceable sub-fields; RAM modules × size check
  - several drives and several network cards (add/remove cards)
  - MAC validation and normalisation; warranty options
- **Employees:** list with status filter (Activo / Baja temporal / Ha dejado la empresa); employee page with current and past devices, including faults during their possession; "Cambiar situación" (status + date; if leaving, it warns about devices still to recover).
- **Settings,** in groups, each list with usage counts and delete blocked while in use:

| Group | Contains |
|---|---|
| General | Región y formato: organisation name, asset-tag prefix, date format, currency, warranty warning days, **"hostname = asset tag"** switch |
| Acceso y seguridad | Platform users: add/edit, role, password, deactivate; can't deactivate yourself or the last admin |
| Organización | Departments and offices/locations, with names in ES/EN/CA |
| Catálogo de equipos | Device types (has screen / has battery / identified by name), models (manufacturer optional) |
| Componentes | Processors (with cores + frequency), graphics (integrated/dedicated + VRAM), memory generations, memory form factors, storage types, storage form factors, connectors |
| Software | macOS versions, Windows versions, Windows editions, Linux distributions, Linux versions (each tied to a distribution) |
| Red | Network card models (Wi-Fi/Ethernet), Wi-Fi generations, Bluetooth versions |

## 6. Data model (`S` in the code)

```
settings  { orgName, tagPrefix, dateFmt, currency, warrantyDays, hostnameIsTag }
users     { id, nombre, email, rol: admin|tech|read, activo, pass, last }
types     { id, nombre{es,en,ca}, hasScreen, hasBattery, usesName }
depts / locations { id, nombre{es,en,ca}, [tipo office|remote|storage, direccion] }
models    { id, fabricante, nombre, typeId }
cpus      { id, nombre, cores, speed, speedUnit }
gpus      { id, nombre, kind integrated|dedicated, vram, vramUnit }
ramGens, ramForms, diskTypes, diskForms, diskConns, wifiGens, btVers,
macVersions, winVersions, winEditions, linuxDistros   { id, nombre }
linuxVersions { id, nombre, distroId }
nicModels { id, nombre, type wifi|eth }
employees { id, nombre, email, dept, loc, alta, estado: activo|baja|salida, estadoFecha }
devices   { id, tag, nombre(hostname), serial, typeId, modelId, customName, estado, loc,
            compra, precio, proveedor, factura, garantia, garantiaExt yes|no|'', garantiaEnded,
            destino, wipeCert, notas,
            cpuId, cpuRep,
            ramSize/ramUnit, ramGen, ramSpeed/ramSpeedUnit, ramRep, ramModules, ramModSize/ramModUnit, ramForm,
            disks[{ size, unit, type, rep, form, conn }],
            gpuId,
            screen, touch, batHealth, batDate, batLog[{ fecha, salud }],
            osFamily mac|win|linux|'', osVerId, osEditionId, osDistroId, oclp, hackintosh, enc, ad,
            nics[{ type, modelId, mac, wifiGen, btVer, speed, speedUnit }] }
assignments { id, deviceId, employeeId, desde, hasta, notas, condicion }
incidents { id, deviceId, fecha, tipo, descripcion, estado abierta|resuelta, resuelta, piezas, coste, proveedor }
log       { fecha, k (i18n key), a (args), deviceId, by }
```

- Tri-state fields use `'yes' | 'no' | ''`, where `''` means "Not defined".
- Example texts are stored as `{es, en, ca}` objects; text typed by users is plain strings.

## 7. Design

- **Classic:** green accent; Bricolage Grotesque + Instrument Sans + JetBrains Mono; top tabs; dashed **+** next to the tabs.
- **Glass (default), Apple-style:**
  - translucent frosted panels over soft colour blobs; system font; system colours (#007AFF…)
  - desktop: floating sidebar, account menu at the bottom (opens upwards)
  - phone: floating bottom tab bar
  - round blue **+** floating at the bottom right, aligned with the content's right edge; it compensates for scrollbar width
  - forms are sheets with Cancel at the top left, a centred title and the action at the top right (fixed 60px header); on phones they slide up from the bottom with the title on its own line
  - label/value rows like a settings list; coloured icon tiles for Settings groups; menu hover in blue; toggle switches for checkboxes; save confirmations drop from the top
- **Default design:** Glass, unless the user explicitly chose Classic (`prefs.uiChosen`).
- **Animations (both designs):**
  - spring press, popovers, sheets, staggered page entrance, number count-up, chart bars growing
  - shake on errors and wrong password; toast with a check that draws itself
  - Glass only: sliding tab highlight
  - all disabled with `prefers-reduced-motion`
- **Text centring layer:** CSS block at the end of `<style>`, inside `@supports (text-box: trim-both cap alphabetic)`. It centres labels on cap height and pins heights with the `cap` unit.
- **Theme:** light/dark tokens on `:root`; Glass redefines the tokens under `[data-ui="glass"]`.

## 8. Code map (inside `inventario.html`)

- `I18N { es, en, ca }`: all UI texts. `t(key, args)` returns text; `T()` returns HTML-escaped text; `tx(obj)` picks the current language from `{es,en,ca}`; `L(es, en, ca)` builds those objects (Catalan falls back to `CA_SEED[es]`).
- `seed()` builds the example data. Helpers it uses: `seedTypes()`, `seedSoftwareLists()`, `softwareToLists()`, `componentsToLists()`, `parseOS()`.
- `load()`: loads saved data and runs **migrations** (single drive → drives list, portable → hasScreen/hasBattery, new types, devices storing their own type, custom builds using a name, free-text OS → structured fields, text values → list entries, removing the leaving reason). Add a migration there for every change to the data shape.
- Helpers: `devType`, `devTitle`, `hasScreen`, `hasBattery`, `usesName`, `osText`, `encLabel`, `cpuDetail`, `gpuDetail`, `holderAt`, `faultsIn`, `empState`, `hostOf`, `modelOpts`, `linuxVerOpts`, `nicModelOpts`, `listOpts`.
- `LISTS`: Settings list definitions (columns, form, `read`, usage `count`). `simpleList()` builds name-only lists. `SET_GROUPS` sets the Settings structure.
- Views: `viewPanel`, `viewDevices` / `drawDeviceRows`, `viewDevice`, `viewEmployees` / `drawEmpRows`, `viewEmployee`, `viewSettings` and friends, `viewLogin`.
- Forms: `deviceForm`, `diskRow`, `nicRow`, `bindHwForm`, `readDevice`, `employeeForm`.
- Actions: `ACTIONS` (device/employee actions) and `SET_ACTIONS` (Settings).
- Dialogs: `openDialog` (`#dlg`), `quickAdd` (second dialog `#dlg2` for **+**), `selPlus()` (dropdown with **+**).
- Chrome: `applyChrome`, `applyUi`, `applyTheme`, `route()` (hash routes such as `#dispositivo-d2`, `#empleado-e1`, `#ajustes-graficas`), `enter()` (entrance animation), `moveTabInd()`.

## 9. Translation rules

- Every key must exist in `es`, `en` and `ca` (552 keys at handoff).
- Previous sessions checked this by evaluating the `I18N` object with Node, comparing key sets, and scanning the code for `t('…')` / `T('…')` keys missing from `I18N.es`.
- Catalan was written by Claude. The user was advised to have a native speaker review it.

## 10. How changes were tested

- Playwright (pre-installed in the old environment) loaded `file://…/inventario.html`. It set `localStorage` prefs (`{"lang":"es","ui":"glass"}`), clicked the demo admin account, drove the forms and read back `S`/`localStorage`.
- Every screen was walked in all three languages, flagging raw keys (`/\b[a-z]+_[a-z_]+\b/`), "undefined", "NaN" and page errors.
- **Migrations** were tested by loading an older copy of the file, taking its `seed()` output, saving it as `inventario-prototipo-v5`, then loading the new file.
- **Layout** was checked with screenshots at 1280px and 390px wide, light and dark, Glass and Classic.
- **Centring** was audited by screenshotting each element with labels replaced by "HHH", measuring the ink box, and running with `reducedMotion: 'reduce'` so entrance animations don't skew the results.

## 11. Suggestions already made to the user (not yet decided)

- If they use Intune or Jamf, add an **"Enrolled in MDM"** field next to Active Directory.
- Native-speaker review of the Catalan texts.
- **Next steps offered:** CSV/Excel import of the existing spreadsheet; printable QR labels; then the **real app** (suggested Django + PostgreSQL, with Microsoft 365 / Google sign-in, server-side roles and a proper audit log), using this prototype and the planning document as the spec.

## 12. Known limits of the prototype

- Sign-in is simulated, and data lives only in each browser's `localStorage`. Nothing is shared between people.
- The capital-letter text centring needs a recent Chrome or Safari; other browsers fall back to normal centring.
- Using a local folder from a cloud session wasn't available for this account, which is why this handoff exists.
