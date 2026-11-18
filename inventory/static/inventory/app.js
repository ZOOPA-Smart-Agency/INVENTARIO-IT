/* ================= i18n ================= */
const I18N = {
  es: {
    log_agent_created: '{tag} añadido por la aplicación de dispositivos', log_agent_updated: '{tag} actualizado por la aplicación de dispositivos',
    install_app: 'Instalar la aplicación', install_done: 'Aplicación instalada', install_ios_t: 'Añadir a la pantalla de inicio', install_ios_1: 'Toca el botón Compartir (el cuadrado con una flecha hacia arriba).', install_ios_2: 'Elige «Añadir a pantalla de inicio».', install_ios_3: 'Confirma con «Añadir». La aplicación aparecerá junto a las demás y se abrirá en su propia ventana.', install_mac_t: 'Añadir al Dock', install_mac_1: 'En la barra de menús de Safari, abre «Archivo».', install_mac_2: 'Elige «Añadir al Dock…» y confirma. La aplicación se abrirá en su propia ventana.',
    up_with_updater: 'El instalador de este servidor comprueba GitHub cada hora y puede instalar las versiones nuevas.', up_no_updater: 'El instalador automático no está activo en este servidor, así que las versiones nuevas se instalan a mano (lo explica el README).', up_install: 'Instalar {v}', up_confirm_t: 'Instalar la versión {v}', up_confirm_b1: 'Antes de empezar se hace una copia de seguridad completa.', up_confirm_b2: 'La aplicación estará en mantenimiento unos minutos; el resto de usuarios verá un aviso.', up_confirm_b3: 'Si algo falla, se vuelve automáticamente a la versión actual con sus datos.', up_confirm_ok: 'Instalar', up_title: 'Instalando la versión {v}', up_title_other: 'Instalando una actualización', up_queued: 'Esperando al instalador…', up_note: 'Puedes cerrar esta página: la instalación sigue en el servidor.', up_watch: '{name} está instalando una actualización. Cuando termine, la página se recargará sola.', up_watch_auto: 'Se está instalando una actualización automática. Cuando termine, la página se recargará sola.', up_ph_backup: 'Haciendo una copia de seguridad…', up_ph_download: 'Descargando la versión nueva…', up_ph_build: 'Preparando la versión nueva…', up_ph_restart: 'Reiniciando la aplicación…', up_ph_check: 'Comprobando que todo funciona…', up_ph_rollback: 'Algo ha fallado: volviendo a la versión anterior…', up_done: 'Versión {v} instalada. Recargando…', up_done_generic: 'Actualización instalada. Recargando…', up_installed_toast: 'Ahora usas la versión {v}.', up_result_rolled_back: 'La actualización no ha funcionado y se ha vuelto a la versión anterior. {msg}', up_result_failed: 'No se ha podido instalar la actualización. {msg}', up_auto_h: 'Actualizaciones automáticas', up_auto_on: 'Instalar las versiones nuevas automáticamente', up_auto_hour: 'Cada día a las', up_auto_d: 'A esa hora (la del servidor) se instala la última versión publicada, si hay una nueva, con copia de seguridad y vuelta atrás si algo falla. Nunca se instalan versiones de prueba. Si falla, no se reintenta hasta el día siguiente.', up_history: 'Historial', up_th_date: 'Fecha', up_th_version: 'Versión', up_th_how: 'Cómo', up_th_result: 'Resultado', up_how_auto: 'Automática', up_how_manual: 'Por {name}', up_st_queued: 'En cola', up_st_running: 'Instalando', up_st_done: 'Instalada', up_st_failed: 'No instalada', up_st_rolled_back: 'Revertida', up_no_history: 'Todavía no se ha instalado ninguna actualización desde aquí.', up_steps_1: 'Cuando se publica una versión nueva en GitHub, aparece aquí.', up_steps_2: 'Pulsa «Instalar», o deja que se instale sola a la hora elegida.', up_steps_3: 'El instalador hace una copia de seguridad, instala la versión y comprueba que funciona; si no, vuelve atrás solo.', err_no_updater: 'El instalador automático no responde en este servidor.', err_update_stale: 'Esa versión ya no es la última disponible. Vuelve a comprobar las actualizaciones.', err_update_busy: 'Ya hay una actualización o una restauración en curso.', log_update_requested: 'Instalación de la versión {v} solicitada',
    ab_access: 'Acceso a GitHub', ab_access_app: 'GitHub App', ab_access_token: 'Token', ab_access_none: 'Sin configurar (solo repositorios públicos)', ab_st_app_missing: 'La GitHub App no está instalada en el repositorio, o no tiene acceso a él. Instálala y elige este repositorio.', ab_st_app_key: 'Falta la clave privada de la GitHub App o no es válida. Revisa APP_UPDATE_GITHUB_APP_ID y la clave en el servidor.',
    set_updates: 'Actualizaciones', set_updates_sub: 'Busca versiones nuevas publicadas en GitHub', ab_current: 'Versión instalada', ab_how_h: 'Cómo se instala una versión nueva', ab_how_1: 'Se publica una versión nueva (release) en GitHub; se prueba y se prepara automáticamente.', ab_how_2: 'Haz una copia de seguridad en Ajustes › Datos › Copias de seguridad.', ab_how_3: 'Quien gestiona el servidor despliega la versión nueva. Los cambios en la base de datos se aplican solos al arrancar.',
    bk_log_label: 'Entradas del historial', ab_python: 'Python', ab_django: 'Django', ab_postgres: 'PostgreSQL',
    set_about: 'Acerca de', set_about_sub: 'Versión, datos y tecnología de la aplicación', ab_version: 'Versión', ab_build: 'Compilación', ab_env: 'Entorno', ab_env_production: 'Producción', ab_env_development: 'Desarrollo', ab_since: 'En uso desde', ab_tz: 'Zona horaria', ab_data: 'Datos', ab_dbsize: 'Tamaño de la base de datos', ab_tech: 'Tecnología', ab_loading: 'Cargando…', ab_unknown: 'Desconocida', ab_updates: 'Actualizaciones', ab_repo: 'Se comparan con las versiones publicadas en GitHub ({repo}).', ab_check: 'Buscar actualizaciones', ab_checking: 'Buscando…', ab_never: 'Todavía no se ha comprobado.', ab_checked: 'Comprobado el {d}.', ab_st_current: 'Tienes la última versión ({v}).', ab_st_update: 'Hay una versión nueva: {v}', ab_published: 'Publicada el {d}.', ab_open: 'Ver en GitHub', ab_install: 'Para instalarla, despliega la nueva versión en el servidor. Haz antes una copia de seguridad.', ab_st_none: 'Todavía no se ha publicado ninguna versión en GitHub.', ab_st_private: 'No se puede consultar el repositorio porque es privado. Conecta una GitHub App de solo lectura (o un token) en el servidor: lo explica el README.', ab_st_auth: 'GitHub ha rechazado el acceso: el token o la GitHub App no son válidos o no tienen acceso al repositorio.', ab_st_error: 'No se ha podido conectar con GitHub. Inténtalo más tarde.', ab_st_off: 'La búsqueda de actualizaciones está desactivada (APP_UPDATE_REPO).',
    mt_title: 'Estamos haciendo tareas de mantenimiento', mt_body: 'La aplicación de {org} no está disponible durante unos minutos.', mt_auto: 'Esta página se actualizará sola cuando vuelva a estar disponible.', mt_watch: '{name} está restaurando una copia de seguridad. Cuando termine, se cerrará la sesión de todos los usuarios.', mt_done: 'Restauración terminada. Vuelve a iniciar sesión.', mt_back: 'La aplicación vuelve a estar disponible.', maintenance: 'La aplicación está en mantenimiento.', err_maintenance_busy: 'Ya hay otra restauración en curso.', pr_finishing: 'Comprobando los datos restaurados…',
    pr_keep_open: 'No cierres ni recargues esta página hasta que termine.',
    pr_export: 'Exportando copia', pr_prepare: 'Preparando los datos…', pr_prepare_enc: 'Preparando y cifrando los datos…', pr_download: 'Descargando el archivo…', pr_check: 'Comprobando la copia', pr_upload: 'Subiendo el archivo…', pr_read: 'Leyendo la copia…', pr_restore: 'Restaurando copia', pr_restoring: 'Sustituyendo los datos…', pr_step: 'Paso {n} de {total}', pr_left: 'Quedan unos {t}', pr_elapsed: '{t} en curso', pr_leave: 'Hay una copia de seguridad en curso.',
    bk_encrypt: 'Proteger con contraseña (recomendado)', bk_encrypt_d: 'La copia se cifra con AES-256 y solo se puede abrir con esta contraseña.', bk_pw: 'Contraseña de la copia', bk_pw2: 'Repite la contraseña', bk_pw_lost: 'Guárdala en un lugar seguro: si la pierdes, no habrá forma de restaurar esta copia.', bk_plain_warn: 'Sin contraseña, cualquiera que tenga el archivo podrá leer todos los datos.', bk_pw_t: 'Copia protegida', bk_pw_d: 'Esta copia está protegida con contraseña. Escríbela para ver qué contiene.', bk_unlock: 'Abrir', bk_enc_yes: 'Protegida con contraseña', err_bk_pw_short: 'La contraseña de la copia debe tener al menos 10 caracteres.', err_backup_password: 'La contraseña no es correcta o el archivo está dañado.', err_backup_password_required: 'Esta copia está protegida con contraseña.',
    grp_data: 'Datos', grp_data_d: 'Copias de seguridad y restauración', set_data: 'Copias de seguridad', set_data_sub: 'Exporta todos los datos o restaura una copia anterior', bk_export_h: 'Exportar una copia', bk_export_d: 'Descarga un archivo .invbackup con todos los datos y ajustes: dispositivos, empleados, historial, averías, usuarios, listas, logotipo y configuración.', bk_export_warn: 'Contiene datos personales y las contraseñas de los usuarios (cifradas). Guarda el archivo en un lugar seguro.', bk_export_btn: 'Descargar copia', bk_exported: 'Copia descargada', bk_restore_h: 'Restaurar una copia', bk_restore_d: 'Carga un archivo .invbackup exportado desde esta aplicación.', bk_restore_warn: 'Se sustituirán todos los datos y ajustes actuales por los de la copia y se cerrará la sesión de todos los usuarios, incluida la tuya. No se puede deshacer.', bk_restore_btn: 'Restaurar desde un archivo', bk_confirm_t: 'Restaurar copia', bk_confirm_b: 'Copia del {d}, hecha por {by}. Contiene:', bk_n_devices: '{n} dispositivos', bk_n_employees: '{n} empleados', bk_n_users: '{n} usuarios', bk_n_log: '{n} entradas del historial', bk_first: 'Descargar antes una copia de los datos actuales', bk_restore_ok: 'Restaurar', bk_restored: 'Copia restaurada. Vuelve a iniciar sesión.', err_backup_invalid: 'El archivo no es una copia válida de esta aplicación.', err_backup_version: 'Esta copia es de otra versión de la aplicación y no se puede restaurar aquí.', err_backup_no_admin: 'La copia no tiene ningún administrador activo, así que nadie podría entrar.', err_backup_size: 'El archivo es demasiado grande (máximo 50 MB).', log_backup_export: 'Copia de seguridad exportada', log_backup_restore: 'Copia de seguridad restaurada',
    set_brand: 'Logotipo', set_brand_sub: 'Sustituye el icono de la aplicación por el de tu empresa.', brand_upload: 'Subir imagen', brand_change: 'Cambiar imagen', brand_remove: 'Quitar logotipo', brand_formats: 'PNG, JPG, WebP, GIF o SVG de hasta 512 KB. Mejor si es cuadrada y con fondo transparente.', brand_where: 'Se verá en el menú, en la pantalla de inicio de sesión y en la pestaña del navegador.', brand_saved: 'Logotipo actualizado', brand_removed: 'Se ha vuelto al icono original', err_logo_type: 'Ese archivo no es una imagen compatible.', err_logo_size: 'La imagen pesa más de 512 KB.', go_home: 'Ir al resumen', pc_title: 'Cambia tu contraseña', pc_sub: 'Por seguridad, elige una contraseña nueva antes de continuar.', pc_current: 'Contraseña actual', pc_new: 'Contraseña nueva', pc_repeat: 'Repite la contraseña nueva', pc_btn: 'Cambiar', pc_done: 'Contraseña cambiada', err_pw_current: 'La contraseña actual no es correcta.', err_pw_same: 'La contraseña nueva debe ser distinta de la actual.', err_must_change: 'Antes de seguir, cambia tu contraseña.', f_must_change: 'Pedir que cambie la contraseña al iniciar sesión', f_must_change_d: 'Útil cuando le das una contraseña temporal.', chip_must_change: 'Debe cambiar la contraseña', chip_must_change_d: 'Tendrá que elegir una contraseña nueva la próxima vez que inicie sesión.', log_pwchanged: '{name} ha cambiado su contraseña',
    pw_h: 'Seguridad de las contraseñas', pw_enforce: 'Exigir requisitos de seguridad', pw_enforce_d: 'Las contraseñas que no los cumplan no se aceptarán.', pw_off: 'Sin requisitos: se aceptará cualquier contraseña.', pw_minlabel: 'Longitud mínima', pw_chars: 'caracteres', pw_c_upper: 'Al menos una mayúscula', pw_c_number: 'Al menos un número', pw_c_symbol: 'Al menos un símbolo', pw_c_min: 'Al menos {n} caracteres', pw_weak: 'Contraseña insegura', pw_ok: 'Contraseña aceptable', pw_strong: 'Contraseña segura', pw_empty: 'Escribe una contraseña para ver su seguridad', pw_applies: 'Se aplica a las contraseñas nuevas o cambiadas. Las actuales siguen funcionando.', set_pwpolicy: 'Contraseñas', set_pwpolicy_sub: 'Elige qué requisitos deben cumplir las contraseñas.', err_pw_minlen: 'La longitud mínima debe ser un número entre 1 y 128.',
    su_title: 'Configuración inicial', su_sub: 'Deja la aplicación lista en tres pasos.', su_step: 'Paso {n} de 3', su_org_h: 'Tu organización', su_org: 'Nombre de la organización', su_prefix: 'Prefijo de las etiquetas', su_date: 'Formato de fecha', su_currency: 'Moneda', su_token: 'Código de instalación', su_token_hint: 'Lo define quien ha desplegado la aplicación (DJANGO_SETUP_TOKEN).', su_places_h: 'Oficinas y departamentos', su_locs: 'Ubicaciones', su_locs_hint: 'Dónde están los equipos. Marca un almacén para que los equipos devueltos vuelvan allí.', su_depts: 'Departamentos', su_depts_hint: 'Opcional: también puedes añadirlos después en Ajustes.', su_add_loc: 'Añadir ubicación', su_add_dept: 'Añadir departamento', su_name: 'Nombre', su_remove: 'Quitar', su_admin_h: 'Tu cuenta de administrador', su_admin_sub: 'Con esta cuenta entrarás y podrás crear las del resto del equipo.', su_fullname: 'Nombre completo', su_email: 'Correo electrónico', su_pass: 'Contraseña', su_pass2: 'Repite la contraseña', su_back: 'Atrás', su_next: 'Siguiente', su_finish: 'Terminar', su_blocked_t: 'Falta el código de instalación', su_blocked_b: 'La instalación no se puede completar todavía: define la variable DJANGO_SETUP_TOKEN en el servidor y recarga esta página.', su_done: '¡Todo listo! Ya puedes añadir tus dispositivos.', err_su_org: 'Indica el nombre de la organización.', err_su_loc: 'Añade al menos una ubicación con nombre.', err_su_admin: 'Rellena tu nombre y un correo válido.', err_su_mismatch: 'Las contraseñas no coinciden.', err_setup_token: 'El código de instalación no es correcto.', err_setup_done: 'La aplicación ya está configurada. Inicia sesión.', log_setup: 'Instalación inicial completada',
    err_network: 'No se ha podido conectar con el servidor. Inténtalo de nuevo.', err_forbidden: 'No tienes permiso para hacer esto.', err_invalid: 'Hay datos no válidos. Revisa el formulario.', err_conflict: 'El dispositivo ha cambiado. Recarga la página e inténtalo de nuevo.', err_not_found: 'Este registro ya no existe.', err_dates: 'La fecha de fin no puede ser anterior a la de inicio.', err_asg_dates: 'La fecha de entrega no puede ser anterior a la última devolución de este equipo.', err_fix_dates: 'La fecha de resolución no puede ser anterior a la de la avería.', err_serial_dup: 'Ya hay otro dispositivo con ese número de serie.', err_auth: 'Tu sesión ha caducado. Vuelve a iniciar sesión.', err_pass_weak: 'La contraseña no cumple los requisitos de seguridad.', login_locked: 'Demasiados intentos. Espera 15 minutos e inténtalo de nuevo.',
    brand: 'Inventario de equipos', nav_summary: 'Resumen', nav_devices: 'Dispositivos', nav_people: 'Empleados',
    cancel: 'Cancelar', save: 'Guardar', close: 'Cerrar', lang_group: 'Idioma', theme_group: 'Tema', theme_auto: 'Usar el tema del sistema', theme_light: 'Tema claro', theme_dark: 'Tema oscuro',
    yes: 'Sí', no: 'No', none: 'Ninguno', plus_aria: 'Añadir {x}',
    st_uso: 'En uso', st_disponible: 'Disponible', st_reparacion: 'En reparación', st_averiado: 'Averiado', st_descartado: 'Descartado', st_perdido: 'Perdido / robado',
    it_fault: 'Avería', it_repair: 'Reparación', it_part: 'Cambio de pieza', it_maint: 'Mantenimiento', it_loss: 'Pérdida / robo',
    cd_good: 'Bueno', cd_worn: 'Desgastado', cd_damaged: 'Dañado',
    ds_recycle: 'Reciclado', ds_sale: 'Venta', ds_donation: 'Donación', ds_lease: 'Devuelto a la empresa que lo alquilaba',
    lk_office: 'Oficina', lk_remote: 'Teletrabajo', lk_storage: 'Almacén',
    age_lt: 'menos de 1 mes', age_y: n => n === 1 ? '1 año' : n + ' años', age_m: n => n === 1 ? '1 mes' : n + ' meses', age_and: ' y ',

    login_title: 'Entrar', login_sub: 'Inventario de equipos de {org}', f_email: 'Email', f_pass: 'Contraseña', login_btn: 'Entrar',
    login_err: 'El correo, el nombre de usuario o la contraseña no son correctos.', login_off: 'Esta cuenta está desactivada. Pide a un administrador que la active.',
    logout: 'Cerrar sesión', settings: 'Ajustes', no_perm: 'Solo los administradores pueden abrir los ajustes.',
    role_admin: 'Administrador', role_tech: 'Técnico IT', role_read: 'Solo lectura',
    role_admin_d: 'Todo, incluidos los ajustes y los usuarios', role_tech_d: 'Gestiona equipos, empleados y averías', role_read_d: 'Consulta el inventario sin cambiar nada',

    summary_title: 'Resumen', summary_sub: '{n} equipos activos · valor de compra {v}', new_device: 'Nuevo dispositivo', retired_stat: 'Descartados o perdidos',
    attention: 'Requiere atención', nothing: 'Nada pendiente.',
    al_recover: 'Recuperar {tag}', al_recover_s: '{name} dejó la empresa el {date} y aún lo tiene asignado',
    al_inc: 'Incidencia abierta en {tag}', al_inc_s: '{desc} · desde el {date}',
    al_war: 'Garantía de {tag} vence en {n} días', al_enc: '{tag} sin cifrado de disco', al_enc_s: 'Activa el cifrado (BitLocker, FileVault o LUKS) antes de que salga de la oficina',
    by_dept: 'Equipos en uso por departamento', activity: 'Actividad reciente',

    devices_title: 'Dispositivos', devices_sub: 'Equipos de la empresa',
    search_dev: 'Buscar por etiqueta, nombre, n.º de serie, MAC, modelo o persona', lbl_search_in: 'Buscar en', search_in: 'Buscar en «{x}»', sf_all: 'Todos los datos', sf_tag: 'Etiqueta', sf_name: 'Nombre del equipo', sf_serial: 'N.º de serie', sf_model: 'Modelo', sf_cpu: 'Procesador', sf_ram: 'Memoria', sf_disk: 'Almacenamiento', sf_gpu: 'Gráficos', sf_os: 'Sistema', sf_mac: 'MAC', sf_person: 'Asignado a', lbl_search: 'Buscar', lbl_status: 'Estado', lbl_dept: 'Departamento', lbl_type: 'Tipo',
    f_active: 'Todos los activos', f_all: 'Todos', f_alldepts: 'Todos los departamentos', f_alltypes: 'Todos los tipos',
    th_tag: 'Etiqueta', th_device: 'Equipo', th_assigned: 'Asignado a', th_status: 'Estado', th_warranty: 'Garantía',
    left_badge: 'ha dejado la empresa', no_match_dev: 'Ningún dispositivo coincide con los filtros.',
    w_expired: 'Vencida', w_expired_on: 'Vencida el {d}', w_soon: 'Vence en {n} días',

    back_devices: '← Dispositivos', not_found_dev: 'No existe ese dispositivo.', back_list: 'Volver a la lista', serial_no: 'N.º de serie',
    btn_return: 'Registrar devolución', btn_assign: 'Asignar',
    health_ok: 'Estado correcto', health_warning: 'Con avisos', health_failing: 'Fallando', wear_pct: 'Desgaste {n} %', hours_on: '{n} h de uso', disk_checked: 'Leído por la app de registro el {d}', disk_prev: 'antes: {x}', bat_cycles: '{n} ciclos',
    al_places_lost: 'Ningún empleado tiene departamento ni ubicación', al_places_lost_s: 'Restaurar una copia hecha con las versiones 1.10.0 a 1.15.0 los perdía. Si restauraste una, asígnalos de nuevo o restaura una copia nueva.',
    al_faulty: '{tag} está averiado', al_faulty_s: 'No se puede usar: envíalo a reparar, sustitúyelo o retíralo.',
    al_disk_fail: '{tag}: disco fallando', al_disk_fail_s: '{x}: el propio disco informa de que falla. Haz una copia de los datos y sustitúyelo.', al_disk_warn: '{tag}: disco con avisos', al_disk_warn_s: '{x}: el disco informa de problemas; vigílalo.', al_disk_wear: '{tag}: SSD desgastado al {n} %', al_disk_wear_s: '{x}: se acerca al final de su vida útil.',
    chk_head: n => n === 1 ? '1 dato a revisar' : n + ' datos a revisar', chk_fix_app: 'Para corregirlo, vuelve a pasar la app de registro (0.9.0 o posterior) en este equipo.', chk_fix_edit: 'Corrígelo con Editar.',
    chk_ignore: 'Ignorar', chk_ignore_title: 'Ignorar este aviso', chk_ignore_body: 'El aviso dejará de mostrarse para {tag}, para todo el equipo de IT. Hazlo solo si has comprobado que el dato es correcto.', chk_ignored_done: 'Aviso ignorado',
    chk_show_ignored: n => n === 1 ? 'Volver a mostrar 1 aviso ignorado' : 'Volver a mostrar ' + n + ' avisos ignorados', f_review: 'Con datos a revisar', al_check: '{tag}: {n} datos a revisar',
    log_check_ignored: '{tag}: aviso de datos ignorado', log_check_reset: '{tag}: avisos de datos ignorados, mostrados de nuevo',
    chk_screen_missing: 'Falta el tamaño de pantalla', chk_screen_missing_h: 'Las versiones anteriores de la app no lo leían en los Mac ni en algunos portátiles con Windows.',
    chk_battery_missing: 'Falta la salud de la batería', chk_battery_missing_h: 'En muchos portátiles con Windows, las versiones anteriores de la app no la leían.',
    chk_eth_model_missing: 'Falta el modelo de la tarjeta Ethernet', chk_eth_model_missing_h: 'En los Mac, las versiones anteriores de la app no lo leían.',
    chk_dup_serial: 'Número de serie repetido', chk_dup_serial_h: 'Otro dispositivo tiene el mismo número de serie; la app de registro actualizaría el primero que encuentre.',
    chk_dup_mac: 'Dirección MAC repetida', chk_dup_mac_h: 'Otro dispositivo tiene una tarjeta de red con la misma MAC; una de las dos está mal.',
    chk_usb_nic: 'Posible adaptador USB: {x}', chk_usb_nic_h: 'Parece un adaptador o una base USB, que pasa de un equipo a otro, no la tarjeta del propio equipo. Las versiones anteriores de la app lo registraban.',
    chk_card_number: 'Chip Wi-Fi dudoso: {x}', chk_card_number_h: 'En Mac antiguos, ese número es el de la tarjeta de Apple, no el del chip.',
    chk_eth_speed: 'Velocidad de Ethernet imposible', chk_eth_speed_h: 'Más de 100 Gbps: seguramente se escribieron megabits con la unidad en Gbps.',
    chk_disk_size: 'Capacidad de disco exacta: {x}', chk_disk_size_h: 'Seguramente es el modelo de {y}; las versiones anteriores guardaban la capacidad exacta en lugar de la que se vende.',
    chk_raid_conn: 'Conector «RAID»', chk_raid_conn_h: 'En Windows, un disco NVMe detrás del controlador de Intel aparecía como RAID.',
    chk_conn_missing: 'Disco sin conector', chk_conn_missing_h: 'Un disco no reemplazable perdía el conector al editar el equipo.',
    chk_mac_dimm: 'Memoria «DIMM» en un Mac', chk_mac_dimm_h: 'Los Mac usan SO-DIMM (salvo el Mac Pro); las versiones anteriores de la app ponían DIMM.',
    chk_soldered_modules: 'Módulos en memoria soldada', chk_soldered_modules_h: 'La memoria es soldada pero conserva datos de módulos de un registro anterior.',
    chk_lpddr_replaceable: 'LPDDR marcada como reemplazable', chk_lpddr_replaceable_h: 'La memoria LPDDR va soldada; algunos equipos la anunciaban como SO-DIMM.',
    chk_arc_dedicated: 'Gráfica integrada marcada como dedicada', chk_arc_dedicated_h: 'Intel Arc de los Core Ultra va dentro del procesador, sin memoria propia.',
    chk_vram_4: 'Memoria de vídeo de 4 GB', chk_vram_4_h: 'Windows no decía más de 4 GB; si la tarjeta tiene más, la cifra está mal.',
    chk_model_type: 'Modelo de otro tipo', chk_model_type_h: 'El modelo pertenece a otro tipo de dispositivo distinto del del equipo.',
    chk_in_use_nobody: 'En uso sin asignar', chk_in_use_nobody_h: 'Está en uso, pero no está asignado a nadie.',
    chk_assigned_idle: 'Asignado sin estar en uso', chk_assigned_idle_h: 'Tiene una asignación abierta, pero su estado no es «En uso».',
    chk_asg_overlap: 'Asignaciones solapadas', chk_asg_overlap_h: 'Hay asignaciones que se solapan o que terminan antes de empezar; el historial de quién lo tenía no es fiable.',
    chk_fix_before: 'Avería resuelta antes de registrarse', chk_fix_before_h: 'Una avería tiene fecha de resolución anterior a la de registro.',
    chk_warranty_before: 'Garantía anterior a la compra', chk_warranty_before_h: 'La garantía termina antes de la fecha de compra.',
    chk_battery_range: 'Salud de batería por encima del 100 %', chk_battery_range_h: 'Una lectura de batería de más del 100 % no es posible.', gen_n: n => n + '.ª gen.', ultra_s: n => 'Serie ' + n, ryzen_s: n => 'serie ' + n, reload: 'Actualizar', reloaded: 'Datos actualizados', mi_to_emp: 'A un empleado', mi_to_emp_d: 'Lo usará una persona', mi_to_dept: 'A un departamento', mi_to_dept_d: 'Equipo compartido por todo el departamento', assign_title_dept: 'Asignar {tag} a un departamento', btn_fault: 'Registrar avería', btn_status: 'Cambiar estado', btn_edit: 'Editar',
    n_left: '{name} dejó la empresa el {date}. Recupera este equipo y registra la devolución.', n_noenc: 'El disco no está cifrado.',
    current: 'Asignación actual', since: 'Desde el {d} ({age})', delivered_with: 'Entregado con: {x}', out_service: 'Fuera de servicio.', unassigned_at: 'Sin asignar. Está en {loc}.',
    hw: 'Hardware y software', k_type: 'Tipo', cores: n => n === 1 ? '1 núcleo' : n + ' núcleos', k_cpu: 'Procesador', k_ram: 'Memoria', k_disk: 'Almacenamiento', k_os: 'Sistema', k_enc: 'Cifrado', k_loc: 'Ubicación',
    net: 'Red', k_wifi_chip: 'Chip Wi-Fi', k_wifi_gen: 'Generación', k_mac_wifi: 'MAC Wi-Fi', k_mac_eth: 'MAC Ethernet', no_wifi: 'Sin chip Wi-Fi', no_eth: 'Sin puerto Ethernet',
    purchase: 'Compra y garantía', k_bought: 'Fecha de compra', k_age: 'Antigüedad', k_wend: 'Fin de garantía', k_supplier: 'Proveedor', k_invoice: 'Factura', k_price: 'Precio', k_repcost: 'Gasto en reparaciones',
    notes: 'Notas', user_hist: 'Historial de usuarios', th_person: 'Persona', th_from: 'Desde', th_to: 'Hasta', th_dur: 'Duración', th_handover: 'Entrega y devolución',
    current_lbl: 'Actual', returned_cond: 'Devuelto en estado: {c}', never_assigned: 'Nunca se ha asignado.',
    inc_hist: 'Averías, reparaciones y cambios de piezas', th_date: 'Fecha', th_kind: 'Tipo', th_desc: 'Descripción', th_parts: 'Piezas', th_cost: 'Coste',
    open: 'Abierta', resolved: 'Resuelta', mark_resolved: 'Marcar resuelta', no_inc: 'Sin incidencias registradas.',

    people_title: 'Empleados', people_sub: 'Personas a las que se asignan equipos', new_person: 'Nuevo empleado', search_people: 'Buscar por nombre, email o departamento',
    lbl_situation: 'Situación', f_staff: 'Activos', f_left: 'De baja', th_name: 'Nombre', th_loc: 'Ubicación', th_curdev: 'Equipos actuales', th_sit: 'Situación',
    left_on: 'Baja {d}', no_match_people: 'Nadie coincide con la búsqueda.',
    back_people: '← Empleados', not_found_person: 'No existe esa persona.', btn_leave: 'Dar de baja', left_since: 'Baja desde {d}',
    n_person_left: n => `Esta persona ya no está en la empresa y tiene ${n} equipo${n > 1 ? 's' : ''} sin devolver.`,
    cur_devices: 'Equipos asignados ahora', th_handed: 'Entregado con', no_cur: 'No tiene equipos asignados.', past_devices: 'Equipos anteriores', no_hist: 'Sin historial.',
    data: 'Datos', k_hired: 'Fecha de alta', k_tenure: 'Antigüedad', k_email: 'Email',

    fd_tag: 'Etiqueta de inventario', fd_host: 'Nombre del equipo (hostname)', fd_serial: 'N.º de serie', fd_model: 'Modelo', sect_hw: 'Hardware y software',
    fd_cpu: 'Modelo de procesador', fd_cpu_ph: 'Intel Core Ultra 7 155U', fd_cores: 'Núcleos', fd_cpu_speed: 'Frecuencia máxima', fd_ram: 'Capacidad de RAM', fd_ram_gen: 'Generación de memoria', fd_ram_speed: 'Frecuencia de memoria',
    fd_disk: 'Capacidad de almacenamiento', fd_disk_type: 'Tipo de almacenamiento', hw_hint: 'Todos los datos de hardware son opcionales. Deja «Sin definir» lo que no sepas.',
    fd_cpu_rep: 'Procesador reemplazable', fd_ram_rep: 'Memoria reemplazable', fd_disk_rep: 'Almacenamiento reemplazable',
    fd_ram_form: 'Formato de memoria', fd_disk_form: 'Formato', fd_m2: 'Tamaño M.2',
    undef: 'Sin definir', rp_yes: 'Sí, reemplazable', rp_no: 'No, soldado a la placa', rp_yes_s: 'Reemplazable', rp_no_s: 'Soldado',
    ff_onboard: 'Soldada en placa', ffd_onboard: 'Soldado en placa', ffd_25: '2,5 pulgadas', ffd_35: '3,5 pulgadas', ffd_prop: 'Propietario', unit_aria: 'Unidad', not_set: 'Sin indicar', fd_os: 'Sistema operativo', fd_loc: 'Ubicación', fd_enc: 'Disco cifrado',
    sect_net: 'Red', fd_wifi: 'Chip Wi-Fi', fd_mac_wifi: 'MAC Wi-Fi', fd_mac_eth: 'MAC Ethernet', mac_ph: 'AA:BB:CC:DD:EE:FF', err_mac: 'Las direcciones MAC deben tener el formato AA:BB:CC:DD:EE:FF',
    sect_purchase: 'Compra y garantía', fd_bought: 'Fecha de compra', fd_wend: 'Fin de garantía', fd_supplier: 'Proveedor', fd_invoice: 'N.º de factura', fd_price: 'Precio ({c})', fd_notes: 'Notas',
    err_required: 'La etiqueta y el número de serie son obligatorios', err_dup: 'Ya existe un dispositivo con esa etiqueta o ese número identificador', f_numbering: 'Numeración de las etiquetas', num_type: 'Por tipo de dispositivo', num_global: 'Global, para todos los dispositivos', num_type_hint: 'Cada código cuenta por su lado: {a} y {b} pueden convivir.', num_global_hint: 'Un único número para todos: si existe {a}, el siguiente MacBook será {c} y no {b}.',
created: '{tag} añadido', edit_title: 'Editar {tag}', saved: 'Cambios guardados',
    fe_name: 'Nombre completo', fe_email: 'Email corporativo', fe_dept: 'Departamento', fe_depts: 'Departamentos', fe_locs: 'Ubicaciones', no_dept: 'Sin departamento', no_loc: 'Sin ubicación', add_dept: 'Añadir otro departamento', add_loc: 'Añadir otra ubicación', fe_loc: 'Ubicación', fe_hired: 'Fecha de alta', k_contract: 'Contrato', ct_indefinido: 'Indefinido', ct_temporal: 'Temporal', ct_practicas: 'Prácticas', ct_all: 'Todos los contratos', ct_unset: 'Sin definir', err_person: 'El nombre y el email son obligatorios',
    assign_title: 'Asignar {tag}', fa_dept: 'Departamento', err_dept: 'Elige un departamento', shared_dept: 'Equipo compartido del departamento', fa_emp: 'Empleado', already_has: '(ya tiene {n})', fa_date: 'Fecha de entrega', fa_acc: 'Accesorios entregados', fa_acc_ph: 'Cargador, dock, ratón…', assign_btn: 'Asignar', assigned_to: 'Asignado a {name}',
    return_title: 'Devolución de {tag}', return_intro: 'Lo devuelve {name}, que lo tiene desde el {d}.', fr_date: 'Fecha de devolución', fr_cond: 'Estado físico', fr_next: 'Después de la devolución',
    next_avail: 'Disponible en el almacén', next_rep: 'Enviar a reparación', next_faulty: 'Averiado, no se puede usar', next_disc: 'Descartar', fr_notes_ph: 'Falta el cargador, borrado de datos hecho…', return_prefix: 'Devolución: ', return_done: 'Devolución registrada',
    fault_title: 'Registrar avería en {tag}', fi_date: 'Fecha', fi_type: 'Tipo', fi_desc: 'Descripción del problema', fi_parts: 'Piezas cambiadas', fi_cost: 'Coste ({c})', fi_tech: 'Servicio técnico',
    in_war: 'En garantía hasta el {d}', out_war: 'Fuera de garantía', fi_rep: 'Enviar el equipo a reparación ahora', err_desc: 'Describe el problema',fault_done: 'Incidencia registrada',
    resolve_title: 'Cerrar incidencia', fs_date: 'Fecha de resolución', fs_cost: 'Coste final ({c})', resolve_done: 'Incidencia cerrada',
    status_title: 'Cambiar estado de {tag}', fc_new: 'Nuevo estado', fc_warn: 'Si lo pasas a disponible, descartado o perdido, se cerrará la asignación a {name}.',
    sect_disposal: 'Solo si se descarta', fc_dest: 'Destino', fc_cert: 'Certificado de destrucción de datos', fc_reason: 'Motivo o notas',
    disc_note: a => `Descartado el ${a.d}. Destino: ${a.m}.${a.c ? ' Certificado de destrucción de datos ' + a.c + '.' : ''}`, status_done: 'Estado actualizado',
    add: 'Añadir', person_added: '{name} añadido', edit_person: 'Editar a {name}',
    leave_title: 'Dar de baja a {name}', fl_date: 'Fecha de baja', fl_pending: a => `Tiene ${a.n} equipo${a.n > 1 ? 's' : ''} por recuperar: ${a.tags}. Seguirán asignados hasta que registres la devolución.`, leave_done: 'Baja registrada',

    set_title: 'Ajustes', set_sub: 'Configuración de {org}', set_home: 'Todos los ajustes',
    grp_general: 'General', grp_general_d: 'Nombre de la organización, fechas, moneda y avisos',
    grp_access: 'Acceso y seguridad', grp_access_d: 'Quién puede entrar y con qué permisos',
    grp_org: 'Organización', grp_org_d: 'Estructura de la empresa y sus sedes',
    grp_catalog: 'Catálogo de equipos', grp_catalog_d: 'Qué clases de equipos tenéis y de qué fabricantes',
    grp_parts: 'Componentes', grp_parts_d: 'Procesadores, gráficas, memoria y almacenamiento registrados para reutilizarlos',
    set_users: 'Usuarios de la plataforma', set_users_sub: 'Quién puede entrar en el inventario y qué puede hacer',
    set_region: 'Región y formato', set_region_sub: 'Fechas, moneda y opciones generales',
    set_depts: 'Departamentos', set_depts_sub: 'Se asignan a cada empleado',
    set_locs: 'Oficinas y ubicaciones', set_locs_sub: 'Dónde están los equipos y dónde trabaja cada persona',
    set_types: 'Tipos de dispositivo', set_types_sub: 'Categorías de equipos y si tienen pantalla integrada o batería',
    set_models: 'Modelos', set_models_sub: 'Fabricante, modelo y tipo de cada equipo',
    set_wifi: 'Chips Wi-Fi', set_wifi_sub: 'Tarjetas de red inalámbrica y la generación Wi-Fi que soportan',
    set_ram: 'Generaciones de memoria', set_ram_sub: 'Generaciones de RAM, como DDR4, DDR5 o LPDDR5X', set_disk: 'Tipos de almacenamiento', set_disk_sub: 'Tecnologías de disco, como SSD, HDD o eMMC',
    item_ram: 'generación de memoria', item_disk: 'tipo de almacenamiento', f_simple_name: 'Nombre',
    menu_lang: 'Idioma', menu_theme: 'Tema', menu_ui: 'Diseño', ui_classic: 'Clásico', ui_glass: 'Cristal', add_menu: 'Añadir', add_device_d: 'Portátil, sobremesa, monitor…', add_person_d: 'Persona a la que asignar equipos', account_menu: 'Menú de la cuenta',
    item_dept: 'departamento', item_loc: 'ubicación', item_type: 'tipo de dispositivo', item_model: 'modelo', item_wifi: 'chip Wi-Fi', item_user: 'usuario',
    add_x: 'Añadir {x}', edit_x: 'Editar {x}', delete: 'Eliminar', delete_title: 'Eliminar {name}', delete_body: 'Se eliminará «{name}». No se puede deshacer.', deleted: 'Eliminado',
    in_use_cant: 'No se puede eliminar porque está en uso', added_x: '{x} añadido',
    th_usage: 'En uso', u_people: n => n === 1 ? '1 empleado' : n + ' empleados', u_devices: n => n === 1 ? '1 equipo' : n + ' equipos', u_models: n => n === 1 ? '1 modelo' : n + ' modelos', u_none: 'Sin uso',
    f_name_es: 'Nombre en español', f_name_en: 'Nombre en inglés', f_name_ca: 'Nombre en catalán', f_name_hint: 'Si dejas alguno vacío, se usa uno de los otros nombres.', err_name: 'Escribe un nombre',
    f_loc_kind: 'Tipo de ubicación', f_address: 'Dirección', th_address: 'Dirección', th_kind: 'Tipo',
    f_maker: 'Fabricante', f_model_name: 'Modelo', f_type: 'Tipo de dispositivo', th_maker: 'Fabricante', th_model: 'Modelo', err_model: 'El fabricante y el modelo son obligatorios',
    f_chip: 'Nombre del chip', f_chip_ph: 'Intel Wi-Fi 7 BE200', f_gen: 'Generación Wi-Fi', th_chip: 'Chip', th_gen: 'Generación', f_bt: 'Bluetooth', th_bt: 'Bluetooth',
    th_role: 'Rol', th_last: 'Último acceso', never: 'Nunca', f_role: 'Rol', f_pass_tmp: 'Contraseña inicial', f_pass_new: 'Nueva contraseña', f_pass_hint: 'Déjala vacía para no cambiarla.',
    u_active: 'Activo', u_inactive: 'Desactivado', deactivate: 'Desactivar', activate: 'Activar', you: '(tú)',
    err_self: 'No puedes desactivar tu propia cuenta', err_last_admin: 'Tiene que quedar al menos un administrador activo', err_email_dup: 'Ya hay un usuario con ese email', err_username: 'El nombre de usuario solo puede tener letras minúsculas, números, puntos, guiones y guiones bajos (al menos 2)', err_username_dup: 'Ya hay un usuario con ese nombre de usuario', f_login_id: 'Correo o nombre de usuario', f_username: 'Nombre de usuario', f_username_hint: 'Sirve para iniciar sesión igual que el correo. Déjalo vacío para entrar solo con el correo.', f_username_hint_new: 'Sirve para iniciar sesión igual que el correo. Si lo dejas vacío, se crea a partir del correo.', err_pass: 'Escribe una contraseña', err_user: 'El nombre y el email son obligatorios',
    user_on: 'Cuenta activada', user_off: 'Cuenta desactivada',
    f_org: 'Nombre de la organización', f_prefix: 'Prefijo de las etiquetas de inventario', f_prefix_hint: 'Las etiquetas son el prefijo, el código del tipo de dispositivo y un número, como {x}',
    f_datefmt: 'Formato de fecha', f_currency: 'Moneda', f_wdays: 'Avisar de garantías que vencen en los próximos (días)',
    df_dmy: 'Día/mes/año', df_mdy: 'Mes/día/año', df_ymd: 'Año-mes-día (ISO)', df_dmydot: 'Día.mes.año', region_saved: 'Ajustes guardados', region_preview: 'Vista previa: {d} · {m}',

    log_created: '{tag} dado de alta en el inventario', log_edited: '{tag}: datos actualizados', log_assigned: '{tag} asignado a {name}', log_loan: '{tag} asignado a {name} (préstamo)',
    log_returned: '{name} devolvió {tag} ({cond})', log_incident: 'Incidencia registrada en {tag}: {desc}', log_repair: '{tag} enviado a reparación: {desc}', log_resolved: 'Incidencia de {tag} resuelta',
    log_status: a => `${a.tag} pasa a «${a.st}»${a.reason ? ': ' + a.reason : ''}`, log_left: a => `${a.name} ha dejado la empresa${a.tags ? '. Pendiente recuperar ' + a.tags : ''}`,
    log_disposed: '{tag} descartado y entregado a gestor RAEE', log_setting: 'Ajustes: {x}',
    es_activo: 'Activo',
    es_baja: 'Baja temporal',
    es_salida: 'Ha dejado la empresa',
    btn_situation: 'Cambiar situación',
    sit_title: 'Situación de {name}',
    fs_state: 'Situación',
    fs_since: 'Desde',
    sit_done: 'Situación actualizada',
    since_d: 'desde el {d}',
    n_onleave: '{name} está de baja temporal desde el {d}.',
    log_onleave: '{name} está de baja temporal',
    log_back: '{name} vuelve a estar activo',
    sect_screen: 'Pantalla y batería',
    fd_screen: 'Tamaño de pantalla (pulgadas)',
    fd_touch: 'Pantalla táctil',
    fd_bat: 'Salud de la batería (%)',
    fd_bat_date: 'Fecha de la medición',
    k_screen: 'Pantalla',
    k_battery: 'Batería',
    touch_s: 'Táctil',
    notouch_s: 'No táctil',
    bat_measured: 'medida el {d}',
    bat_prev: 'Mediciones anteriores: {x}',
    al_bat: '{tag}: batería al {p} %',
    al_bat_s: 'Por debajo del 80 %: valora cambiarla',
    set_cpus: 'Procesadores',
    set_cpus_sub: 'Modelos de procesador con sus núcleos y frecuencia máxima',
    item_cpu: 'procesador',
    th_cores: 'Núcleos',
    th_freq: 'Frecuencia máx.',
    cpu_hint: 'Los núcleos y la frecuencia se guardan con el modelo y se muestran en cada equipo que lo use.',
    fd_ram_modules: 'Número de módulos',
    fd_ram_modsize: 'Capacidad de cada módulo',
    ram_mismatch: '{n} × {s} = {t}, que no coincide con la capacidad total',
    set_ramforms: 'Formatos de memoria',
    set_ramforms_sub: 'Formatos de módulo, como SO-DIMM, DIMM o CAMM2',
    item_ramform: 'formato de memoria',
    fd_disk_conn: 'Conector',
    set_diskforms: 'Formatos de almacenamiento',
    set_diskforms_sub: 'Tamaños de unidad, como M.2 2280 o 2,5 pulgadas',
    item_diskform: 'formato de almacenamiento',
    set_conns: 'Conectores de almacenamiento',
    set_conns_sub: 'Interfaz de la unidad, como NVMe PCIe 4.0 o SATA',
    item_conn: 'conector',
    sect_gpu: 'Gráficos',
    k_gpu: 'Gráficos',
    fd_gpu: 'Modelo de gráfica',
    fd_gpu_kind: 'Integrada o dedicada',
    gpu_integrated: 'Integrada',
    gpu_dedicated: 'Dedicada',
    sect_sw: 'Software y ubicación',
    grp_network: 'Red',
    grp_network_d: 'Modelos de tarjeta, generaciones Wi-Fi y versiones de Bluetooth',
    set_wifigens: 'Generaciones Wi-Fi',
    set_wifigens_sub: 'Estándares inalámbricos, como Wi-Fi 6E o Wi-Fi 7',
    item_wifigen: 'generación Wi-Fi',
    set_bt: 'Versiones de Bluetooth',
    set_bt_sub: 'Versiones como Bluetooth 5.3',
    item_bt: 'versión de Bluetooth',
    nic_add: 'Añadir tarjeta de red',
    nic_remove: 'Quitar',
    nic_type: 'Tipo de tarjeta',
    nic_model: 'Modelo (opcional)',
    nic_mac: 'Dirección MAC',
    nic_gen: 'Generación Wi-Fi',
    nic_bt: 'Bluetooth',
    nic_speed: 'Velocidad máxima',
    no_nics: 'No hay tarjetas de red registradas.',
    fd_wext: 'Garantía ampliada',
    fd_wended: 'La garantía ya ha terminado, pero no se sabe la fecha',
    w_ended_unknown: 'Vencida (fecha desconocida)',
    w_ext_chip: 'Ampliada',
    w_left: 'quedan {x}',
    th_faults: 'Averías',
    th_holder: 'Lo tenía',
    nobody: 'Nadie',
    k_dest: 'Destino',
    disk_add: 'Añadir disco',
    disk_n: 'Disco {n}',
    fd_capacity: 'Capacidad',
    host_same: 'También se usa como nombre del equipo (hostname). Puedes cambiarlo en Ajustes.',
    f_hosttag: 'El nombre del equipo (hostname) es el mismo que la etiqueta de inventario',
    f_hosttag_hint: 'Si lo activas, no hace falta escribir el hostname: cada equipo usa su etiqueta, por ejemplo {x}.',
    no_cert: 'sin certificado',
    w_ext_hint: 'Con garantía ampliada, indica la fecha en que termina la ampliación.',
    type_screen: 'Tiene pantalla integrada',
    type_battery: 'Tiene batería',
    fd_customname: 'Nombre (opcional)',
    fd_customname_ph: 'Workstation de vídeo',
    type_usesname: 'Se identifica con un nombre en lugar de un modelo (montaje propio)',
    type_code: 'Código para las etiquetas', type_code_hint: 'Va después del prefijo y antes del número, como LAP en {x}. Sin código, los equipos se numeran sin él.', th_code: 'Código', type_auto: 'Asignar también todos los', auto_none: 'Ninguno', auto_laptop: 'Portátiles', auto_desktop: 'Sobremesas', auto_aio: 'Todo en uno', auto_any: 'Equipos de cualquier forma', auto_brand: 'De qué marcas', auto_allbrands: 'Todas', auto_onlyapple: 'Solo Apple', auto_notapple: 'Todas excepto Apple', type_auto_hint: 'Para los equipos que no coinciden con ninguna palabra ni nombre de tipo. Por ejemplo: todos los portátiles excepto los de Apple, o todos los equipos de Apple. Una forma concreta gana a «cualquier forma».', type_match: 'Asignar automáticamente en la app de registro', type_match_ph: 'MacBook, ThinkPad', type_match_hint: 'Palabras separadas por comas. Un equipo cuyo fabricante o modelo contenga una de ellas recibe este tipo. Si coinciden varias, gana la más larga.',
    err_model_req: 'Elige un modelo, o añade uno con +',
    no_models: 'Todavía no hay modelos de este tipo',
    fd_osver: 'Versión',
    fd_osed: 'Edición',
    fd_distro: 'Distribución',
    fd_oclp: 'Parcheado con OCLP',
    fd_ad: 'Unido al directorio activo',
    k_ad: 'Directorio activo',
    chip_oclp: 'Parcheado (OCLP)', chip_oclp_v: 'Parcheado (OCLP {v})', fd_oclp_ver: 'Versión de OCLP',
    grp_software: 'Software',
    grp_software_d: 'Versiones de sistema operativo, ediciones, distribuciones y sus versiones',
    set_macver: 'Versiones de macOS',
    set_macver_sub: 'Como 15 Sequoia o 26 Tahoe',
    item_macver: 'versión de macOS',
    set_winver: 'Versiones de Windows',
    set_winver_sub: 'Como 10 o 11 24H2',
    item_winver: 'versión de Windows',
    set_wined: 'Ediciones de Windows',
    set_wined_sub: 'Como Pro, Home o Enterprise',
    item_wined: 'edición de Windows',
    set_distros: 'Distribuciones de Linux',
    set_distros_sub: 'Como Ubuntu, Debian o Fedora',
    item_distro: 'distribución de Linux',
    set_linuxver: 'Versiones de Linux',
    set_linuxver_sub: 'Cada versión pertenece a una distribución, como Ubuntu 24.04 LTS',
    item_linuxver: 'versión de Linux',
    pick_distro_first: 'Elige primero una distribución',
    err_linuxver: 'Elige la distribución y escribe la versión',
    u_versions: n => n === 1 ? '1 versión' : n + ' versiones',
    set_gpus: 'Gráficas',
    set_gpus_sub: 'Modelos de gráfica, si son integradas o dedicadas y su VRAM',
    item_gpu: 'gráfica',
    gpu_hint: 'Si es integrada o dedicada y la VRAM se guardan con el modelo y se muestran en cada equipo que lo use.',
    th_vram: 'VRAM',
    set_nicmodels: 'Modelos de tarjeta de red',
    set_nicmodels_sub: 'Tarjetas Wi-Fi y Ethernet, como Intel AX211 o Realtek RTL8125',
    item_nicmodel: 'modelo de tarjeta de red',
    ok_record: 'Registrar',
    ok_resolve: 'Resolver',
  },
  en: {
    log_agent_created: '{tag} added by the device app', log_agent_updated: '{tag} updated by the device app',
    install_app: 'Install the app', install_done: 'App installed', install_ios_t: 'Add to Home Screen', install_ios_1: 'Tap the Share button (the square with an arrow pointing up).', install_ios_2: 'Choose “Add to Home Screen”.', install_ios_3: 'Confirm with “Add”. The app appears next to your others and opens in its own window.', install_mac_t: 'Add to Dock', install_mac_1: 'In Safari’s menu bar, open “File”.', install_mac_2: 'Choose “Add to Dock…” and confirm. The app opens in its own window.',
    up_with_updater: 'This server’s installer checks GitHub every hour and can install new versions.', up_no_updater: 'The automatic installer is not running on this server, so new versions are installed by hand (the README explains how).', up_install: 'Install {v}', up_confirm_t: 'Install version {v}', up_confirm_b1: 'A full backup is made before anything else.', up_confirm_b2: 'The app will be under maintenance for a few minutes; everyone else sees a notice.', up_confirm_b3: 'If anything fails, the current version and its data come back automatically.', up_confirm_ok: 'Install', up_title: 'Installing version {v}', up_title_other: 'Installing an update', up_queued: 'Waiting for the installer…', up_note: 'You can close this page: the installation carries on on the server.', up_watch: '{name} is installing an update. When it finishes, this page reloads by itself.', up_watch_auto: 'An automatic update is being installed. When it finishes, this page reloads by itself.', up_ph_backup: 'Making a backup…', up_ph_download: 'Downloading the new version…', up_ph_build: 'Preparing the new version…', up_ph_restart: 'Restarting the app…', up_ph_check: 'Checking everything works…', up_ph_rollback: 'Something failed: going back to the previous version…', up_done: 'Version {v} installed. Reloading…', up_done_generic: 'Update installed. Reloading…', up_installed_toast: 'You are now using version {v}.', up_result_rolled_back: 'The update did not work, so the previous version is back. {msg}', up_result_failed: 'The update could not be installed. {msg}', up_auto_h: 'Automatic updates', up_auto_on: 'Install new versions automatically', up_auto_hour: 'Every day at', up_auto_d: 'At that time (the server’s), the latest published version is installed if there is a new one, with a backup first and a rollback if anything fails. Test versions are never installed. If it fails, it is not retried until the next day.', up_history: 'History', up_th_date: 'Date', up_th_version: 'Version', up_th_how: 'How', up_th_result: 'Result', up_how_auto: 'Automatic', up_how_manual: 'By {name}', up_st_queued: 'Queued', up_st_running: 'Installing', up_st_done: 'Installed', up_st_failed: 'Not installed', up_st_rolled_back: 'Rolled back', up_no_history: 'No update has been installed from here yet.', up_steps_1: 'When a new version is published on GitHub, it appears here.', up_steps_2: 'Press Install, or let it install itself at the chosen time.', up_steps_3: 'The installer makes a backup, installs the version and checks it works; if not, it goes back by itself.', err_no_updater: 'The automatic installer is not answering on this server.', err_update_stale: 'That version is no longer the latest. Check for updates again.', err_update_busy: 'An update or restore is already running.', log_update_requested: 'Installation of version {v} requested',
    ab_access: 'GitHub access', ab_access_app: 'GitHub App', ab_access_token: 'Token', ab_access_none: 'Not set up (public repositories only)', ab_st_app_missing: 'The GitHub App is not installed on the repository, or cannot access it. Install it and choose this repository.', ab_st_app_key: 'The GitHub App’s private key is missing or not valid. Check APP_UPDATE_GITHUB_APP_ID and the key on the server.',
    set_updates: 'Updates', set_updates_sub: 'Check for new versions published on GitHub', ab_current: 'Installed version', ab_how_h: 'How a new version is installed', ab_how_1: 'A new version (release) is published on GitHub; it is tested and prepared automatically.', ab_how_2: 'Make a backup in Settings › Data › Backups.', ab_how_3: 'Whoever manages the server deploys the new version. Database changes are applied automatically when it starts.',
    bk_log_label: 'History entries', ab_python: 'Python', ab_django: 'Django', ab_postgres: 'PostgreSQL',
    set_about: 'About', set_about_sub: 'The app’s version, data and technology', ab_version: 'Version', ab_build: 'Build', ab_env: 'Environment', ab_env_production: 'Production', ab_env_development: 'Development', ab_since: 'In use since', ab_tz: 'Time zone', ab_data: 'Data', ab_dbsize: 'Database size', ab_tech: 'Technology', ab_loading: 'Loading…', ab_unknown: 'Unknown', ab_updates: 'Updates', ab_repo: 'Compared with the releases published on GitHub ({repo}).', ab_check: 'Check for updates', ab_checking: 'Checking…', ab_never: 'Not checked yet.', ab_checked: 'Checked on {d}.', ab_st_current: 'You have the latest version ({v}).', ab_st_update: 'A new version is available: {v}', ab_published: 'Published on {d}.', ab_open: 'View on GitHub', ab_install: 'To install it, deploy the new version on the server. Make a backup first.', ab_st_none: 'No version has been published on GitHub yet.', ab_st_private: 'The repository cannot be read because it is private. Connect a read-only GitHub App (or a token) on the server, as the README explains.', ab_st_auth: 'GitHub refused access: the token or GitHub App is not valid or cannot access the repository.', ab_st_error: 'Could not connect to GitHub. Please try again later.', ab_st_off: 'The update check is turned off (APP_UPDATE_REPO).',
    mt_title: 'Maintenance in progress', mt_body: 'The {org} app is unavailable for a few minutes.', mt_auto: 'This page will refresh by itself when the app is available again.', mt_watch: '{name} is restoring a backup. When it finishes, every user will be signed out.', mt_done: 'Restore finished. Please sign in again.', mt_back: 'The app is available again.', maintenance: 'The app is under maintenance.', err_maintenance_busy: 'Another restore is already running.', pr_finishing: 'Checking the restored data…',
    pr_keep_open: 'Do not close or reload this page until it finishes.',
    pr_export: 'Exporting backup', pr_prepare: 'Preparing the data…', pr_prepare_enc: 'Preparing and encrypting the data…', pr_download: 'Downloading the file…', pr_check: 'Checking the backup', pr_upload: 'Uploading the file…', pr_read: 'Reading the backup…', pr_restore: 'Restoring backup', pr_restoring: 'Replacing the data…', pr_step: 'Step {n} of {total}', pr_left: 'About {t} left', pr_elapsed: '{t} so far', pr_leave: 'A backup is in progress.',
    bk_encrypt: 'Protect with a password (recommended)', bk_encrypt_d: 'The backup is encrypted with AES-256 and can only be opened with this password.', bk_pw: 'Backup password', bk_pw2: 'Repeat the password', bk_pw_lost: 'Keep it somewhere safe: if you lose it, there is no way to restore this backup.', bk_plain_warn: 'Without a password, anyone who has the file can read all the data.', bk_pw_t: 'Protected backup', bk_pw_d: 'This backup is protected with a password. Enter it to see what it contains.', bk_unlock: 'Open', bk_enc_yes: 'Password protected', err_bk_pw_short: 'The backup password must be at least 10 characters.', err_backup_password: 'The password is not correct, or the file is damaged.', err_backup_password_required: 'This backup is protected with a password.',
    grp_data: 'Data', grp_data_d: 'Backups and restore', set_data: 'Backups', set_data_sub: 'Export all data or restore an earlier backup', bk_export_h: 'Export a backup', bk_export_d: 'Downloads one .invbackup file with all data and settings: devices, employees, history, faults, users, lists, logo and configuration.', bk_export_warn: 'It contains personal data and users’ passwords (encrypted). Keep the file somewhere safe.', bk_export_btn: 'Download backup', bk_exported: 'Backup downloaded', bk_restore_h: 'Restore a backup', bk_restore_d: 'Load an .invbackup file exported from this app.', bk_restore_warn: 'All current data and settings will be replaced with the backup’s, and every user will be signed out, including you. This cannot be undone.', bk_restore_btn: 'Restore from a file', bk_confirm_t: 'Restore backup', bk_confirm_b: 'Backup from {d}, made by {by}. It contains:', bk_n_devices: '{n} devices', bk_n_employees: '{n} employees', bk_n_users: '{n} users', bk_n_log: '{n} history entries', bk_first: 'Download a backup of the current data first', bk_restore_ok: 'Restore', bk_restored: 'Backup restored. Please sign in again.', err_backup_invalid: 'That file is not a valid backup of this app.', err_backup_version: 'This backup is from a different version of the app and cannot be restored here.', err_backup_no_admin: 'The backup has no active administrator, so nobody could sign in.', err_backup_size: 'The file is too large (50 MB maximum).', log_backup_export: 'Backup exported', log_backup_restore: 'Backup restored',
    set_brand: 'Logo', set_brand_sub: 'Replace the app icon with your company’s.', brand_upload: 'Upload image', brand_change: 'Change image', brand_remove: 'Remove logo', brand_formats: 'PNG, JPG, WebP, GIF or SVG up to 512 KB. Square with a transparent background works best.', brand_where: 'It appears in the menu, on the sign-in page and in the browser tab.', brand_saved: 'Logo updated', brand_removed: 'Back to the original icon', err_logo_type: 'That file is not a supported image.', err_logo_size: 'The image is larger than 512 KB.', go_home: 'Go to the overview', pc_title: 'Change your password', pc_sub: 'For security, choose a new password before you continue.', pc_current: 'Current password', pc_new: 'New password', pc_repeat: 'Repeat the new password', pc_btn: 'Change', pc_done: 'Password changed', err_pw_current: 'The current password is not correct.', err_pw_same: 'The new password must be different from the current one.', err_must_change: 'Please change your password before continuing.', f_must_change: 'Ask them to change the password at sign-in', f_must_change_d: 'Useful when you give them a temporary password.', chip_must_change: 'Must change password', chip_must_change_d: 'They will have to choose a new password the next time they sign in.', log_pwchanged: '{name} changed their password',
    pw_h: 'Password security', pw_enforce: 'Enforce security requirements', pw_enforce_d: 'Passwords that do not meet them will not be accepted.', pw_off: 'No requirements: any password will be accepted.', pw_minlabel: 'Minimum length', pw_chars: 'characters', pw_c_upper: 'At least one uppercase letter', pw_c_number: 'At least one number', pw_c_symbol: 'At least one symbol', pw_c_min: 'At least {n} characters', pw_weak: 'Insecure password', pw_ok: 'Acceptable password', pw_strong: 'Secure password', pw_empty: 'Type a password to see how secure it is', pw_applies: 'Applies to new or changed passwords. Current ones keep working.', set_pwpolicy: 'Passwords', set_pwpolicy_sub: 'Choose which requirements passwords must meet.', err_pw_minlen: 'The minimum length must be a number from 1 to 128.',
    su_title: 'Initial setup', su_sub: 'Get the app ready in three steps.', su_step: 'Step {n} of 3', su_org_h: 'Your organisation', su_org: 'Organisation name', su_prefix: 'Asset tag prefix', su_date: 'Date format', su_currency: 'Currency', su_token: 'Setup code', su_token_hint: 'Set by whoever deployed the app (DJANGO_SETUP_TOKEN).', su_places_h: 'Offices and departments', su_locs: 'Locations', su_locs_hint: 'Where your devices are. Mark one as storage so returned devices go back there.', su_depts: 'Departments', su_depts_hint: 'Optional: you can also add them later in Settings.', su_add_loc: 'Add location', su_add_dept: 'Add department', su_name: 'Name', su_remove: 'Remove', su_admin_h: 'Your administrator account', su_admin_sub: 'You will sign in with this account and create everyone else’s.', su_fullname: 'Full name', su_email: 'Email', su_pass: 'Password', su_pass2: 'Repeat the password', su_back: 'Back', su_next: 'Next', su_finish: 'Finish', su_blocked_t: 'Setup code missing', su_blocked_b: 'Setup cannot be completed yet: set the DJANGO_SETUP_TOKEN variable on the server and reload this page.', su_done: 'All set! You can start adding your devices.', err_su_org: 'Enter the organisation’s name.', err_su_loc: 'Add at least one location with a name.', err_su_admin: 'Enter your name and a valid email.', err_su_mismatch: 'The passwords do not match.', err_setup_token: 'That setup code is not correct.', err_setup_done: 'The app is already set up. Please sign in.', log_setup: 'Initial setup completed',
    err_network: 'Could not reach the server. Please try again.', err_forbidden: 'You do not have permission to do this.', err_invalid: 'Some data is not valid. Please check the form.', err_conflict: 'This device has changed. Reload the page and try again.', err_not_found: 'This record no longer exists.', err_dates: 'The end date cannot be before the start date.', err_asg_dates: 'The handover date cannot be before this device was last returned.', err_fix_dates: 'The date it was fixed cannot be before the fault was logged.', err_serial_dup: 'Another device already has that serial number.', err_auth: 'Your session has expired. Please sign in again.', err_pass_weak: 'That password does not meet the security requirements.', login_locked: 'Too many attempts. Wait 15 minutes and try again.',
    brand: 'Device inventory', nav_summary: 'Overview', nav_devices: 'Devices', nav_people: 'Employees',
    cancel: 'Cancel', save: 'Save', close: 'Close', lang_group: 'Language', theme_group: 'Theme', theme_auto: 'Use system theme', theme_light: 'Light theme', theme_dark: 'Dark theme',
    yes: 'Yes', no: 'No', none: 'None', plus_aria: 'Add {x}',
    st_uso: 'In use', st_disponible: 'Available', st_reparacion: 'In repair', st_averiado: 'Faulty', st_descartado: 'Retired', st_perdido: 'Lost / stolen',
    it_fault: 'Fault', it_repair: 'Repair', it_part: 'Part replacement', it_maint: 'Maintenance', it_loss: 'Loss / theft',
    cd_good: 'Good', cd_worn: 'Worn', cd_damaged: 'Damaged',
    ds_recycle: 'Recycled', ds_sale: 'Sale', ds_donation: 'Donation', ds_lease: 'Returned to the leasing company',
    lk_office: 'Office', lk_remote: 'Remote work', lk_storage: 'Storage',
    age_lt: 'under 1 month', age_y: n => n === 1 ? '1 year' : n + ' years', age_m: n => n === 1 ? '1 month' : n + ' months', age_and: ' and ',

    login_title: 'Sign in', login_sub: '{org} device inventory', f_email: 'Email', f_pass: 'Password', login_btn: 'Sign in',
    login_err: 'The email, username or password is not correct.', login_off: 'This account is deactivated. Ask an administrator to turn it back on.',
    logout: 'Sign out', settings: 'Settings', no_perm: 'Only administrators can open settings.',
    role_admin: 'Administrator', role_tech: 'IT technician', role_read: 'Read only',
    role_admin_d: 'Everything, including settings and users', role_tech_d: 'Manages devices, employees and faults', role_read_d: 'Views the inventory without changing anything',

    summary_title: 'Overview', summary_sub: '{n} active devices · purchase value {v}', new_device: 'New device', retired_stat: 'Retired or lost',
    attention: 'Needs attention', nothing: 'Nothing pending.',
    al_recover: 'Recover {tag}', al_recover_s: '{name} left on {date} and still has it',
    al_inc: 'Open fault on {tag}', al_inc_s: '{desc} · since {date}',
    al_war: 'Warranty for {tag} ends in {n} days', al_enc: '{tag} has no disk encryption', al_enc_s: 'Turn on encryption (BitLocker, FileVault or LUKS) before it leaves the office',
    by_dept: 'Devices in use by department', activity: 'Recent activity',

    devices_title: 'Devices', devices_sub: 'Company equipment',
    search_dev: 'Search by tag, name, serial number, MAC, model or person', lbl_search_in: 'Search in', search_in: 'Search in “{x}”', sf_all: 'All details', sf_tag: 'Tag', sf_name: 'Computer name', sf_serial: 'Serial number', sf_model: 'Model', sf_cpu: 'Processor', sf_ram: 'Memory', sf_disk: 'Storage', sf_gpu: 'Graphics', sf_os: 'System', sf_mac: 'MAC', sf_person: 'Assigned to', lbl_search: 'Search', lbl_status: 'Status', lbl_dept: 'Department', lbl_type: 'Type',
    f_active: 'All active', f_all: 'All', f_alldepts: 'All departments', f_alltypes: 'All types',
    th_tag: 'Tag', th_device: 'Device', th_assigned: 'Assigned to', th_status: 'Status', th_warranty: 'Warranty',
    left_badge: 'left', no_match_dev: 'No devices match these filters.',
    w_expired: 'Expired', w_expired_on: 'Expired on {d}', w_soon: 'Ends in {n} days',

    back_devices: '← Devices', not_found_dev: 'That device does not exist.', back_list: 'Back to the list', serial_no: 'Serial no.',
    btn_return: 'Record return', btn_assign: 'Assign',
    health_ok: 'Healthy', health_warning: 'Warnings', health_failing: 'Failing', wear_pct: '{n}% worn', hours_on: '{n} h on', disk_checked: 'Read by the device app on {d}', disk_prev: 'before: {x}', bat_cycles: '{n} cycles',
    al_places_lost: 'No employee has a department or location', al_places_lost_s: 'Restoring a backup made by versions 1.10.0 to 1.15.0 lost them. If you restored one, set them again or restore a newer backup.',
    al_faulty: '{tag} is faulty', al_faulty_s: 'It cannot be used: send it for repair, replace it or retire it.',
    al_disk_fail: '{tag}: drive failing', al_disk_fail_s: '{x}: the drive itself reports it is failing. Back up its data and replace it.', al_disk_warn: '{tag}: drive with warnings', al_disk_warn_s: '{x}: the drive reports problems; keep an eye on it.', al_disk_wear: '{tag}: SSD {n}% worn', al_disk_wear_s: '{x}: it is near the end of its rated life.',
    chk_head: n => n === 1 ? '1 detail to check' : n + ' details to check', chk_fix_app: 'To correct it, run the device app (0.9.0 or later) on this computer again.', chk_fix_edit: 'Correct it with Edit.',
    chk_ignore: 'Ignore', chk_ignore_title: 'Ignore this warning', chk_ignore_body: 'The warning will no longer show for {tag}, for the whole IT team. Only do this if you have checked the detail is right.', chk_ignored_done: 'Warning ignored',
    chk_show_ignored: n => n === 1 ? 'Show 1 ignored warning again' : 'Show ' + n + ' ignored warnings again', f_review: 'With details to check', al_check: '{tag}: {n} details to check',
    log_check_ignored: '{tag}: data warning ignored', log_check_reset: '{tag}: ignored data warnings shown again',
    chk_screen_missing: 'Screen size missing', chk_screen_missing_h: 'Earlier versions of the app did not read it on Macs and on some Windows laptops.',
    chk_battery_missing: 'Battery health missing', chk_battery_missing_h: 'On many Windows laptops, earlier versions of the app did not read it.',
    chk_eth_model_missing: 'Ethernet card model missing', chk_eth_model_missing_h: 'On Macs, earlier versions of the app did not read it.',
    chk_dup_serial: 'Repeated serial number', chk_dup_serial_h: 'Another device has the same serial number; the device app would update whichever it finds first.',
    chk_dup_mac: 'Repeated MAC address', chk_dup_mac_h: 'Another device has a network card with the same MAC; one of them is wrong.',
    chk_usb_nic: 'Possible USB adapter: {x}', chk_usb_nic_h: 'It looks like a USB adapter or dock, which moves between computers, not this computer’s own card. Earlier versions of the app saved them.',
    chk_card_number: 'Doubtful Wi-Fi chip: {x}', chk_card_number_h: 'On older Macs that number is Apple’s card number, not the chip.',
    chk_eth_speed: 'Impossible Ethernet speed', chk_eth_speed_h: 'Over 100 Gbps: probably megabits typed with the unit on Gbps.',
    chk_disk_size: 'Exact drive size: {x}', chk_disk_size_h: 'Probably the {y} model; earlier versions saved the exact size instead of the size sold.',
    chk_raid_conn: '“RAID” connector', chk_raid_conn_h: 'On Windows, an NVMe drive behind Intel’s storage controller showed as RAID.',
    chk_conn_missing: 'Drive without a connector', chk_conn_missing_h: 'A non-replaceable drive lost its connector when the device was edited.',
    chk_mac_dimm: '“DIMM” memory on a Mac', chk_mac_dimm_h: 'Macs use SO-DIMM (except the Mac Pro); earlier versions of the app said DIMM.',
    chk_soldered_modules: 'Modules on soldered memory', chk_soldered_modules_h: 'The memory is soldered but keeps module details from an earlier record.',
    chk_lpddr_replaceable: 'LPDDR marked replaceable', chk_lpddr_replaceable_h: 'LPDDR memory is soldered; some computers announced it as SO-DIMM.',
    chk_arc_dedicated: 'Built-in graphics marked dedicated', chk_arc_dedicated_h: 'Intel Arc in Core Ultra processors is part of the processor, with no memory of its own.',
    chk_vram_4: '4 GB of video memory', chk_vram_4_h: 'Windows said no more than 4 GB; if the card has more, the figure is wrong.',
    chk_model_type: 'Model of another type', chk_model_type_h: 'The model belongs to a different device type from the device’s.',
    chk_in_use_nobody: 'In use but unassigned', chk_in_use_nobody_h: 'It is in use, but not assigned to anyone.',
    chk_assigned_idle: 'Assigned but not in use', chk_assigned_idle_h: 'It has an open assignment, but its status is not “In use”.',
    chk_asg_overlap: 'Overlapping assignments', chk_asg_overlap_h: 'Some assignments overlap or end before they start; the history of who had it is not reliable.',
    chk_fix_before: 'Fault fixed before it was logged', chk_fix_before_h: 'A fault has a fixed date before the date it was logged.',
    chk_warranty_before: 'Warranty ends before purchase', chk_warranty_before_h: 'The warranty ends before the purchase date.',
    chk_battery_range: 'Battery health above 100%', chk_battery_range_h: 'A battery reading above 100% is not possible.', gen_n: n => n + ([11, 12, 13].includes(n % 100) ? 'th' : ({ 1: 'st', 2: 'nd', 3: 'rd' })[n % 10] || 'th') + ' gen', ultra_s: n => 'Series ' + n, ryzen_s: n => n + ' series', reload: 'Refresh', reloaded: 'Up to date', mi_to_emp: 'To an employee', mi_to_emp_d: 'One person will use it', mi_to_dept: 'To a department', mi_to_dept_d: 'Shared by the whole department', assign_title_dept: 'Assign {tag} to a department', btn_fault: 'Log fault', btn_status: 'Change status', btn_edit: 'Edit',
    n_left: '{name} left on {date}. Recover this device and record the return.', n_noenc: 'The disk is not encrypted.',
    current: 'Current assignment', since: 'Since {d} ({age})', delivered_with: 'Handed over with: {x}', out_service: 'Out of service.', unassigned_at: 'Unassigned. Located at {loc}.',
    hw: 'Hardware and software', k_type: 'Type', cores: n => n === 1 ? '1 core' : n + ' cores', k_cpu: 'Processor', k_ram: 'Memory', k_disk: 'Storage', k_os: 'Operating system', k_enc: 'Encryption', k_loc: 'Location',
    net: 'Network', k_wifi_chip: 'Wi-Fi chip', k_wifi_gen: 'Generation', k_mac_wifi: 'Wi-Fi MAC', k_mac_eth: 'Ethernet MAC', no_wifi: 'No Wi-Fi chip', no_eth: 'No Ethernet port',
    purchase: 'Purchase and warranty', k_bought: 'Purchase date', k_age: 'Age', k_wend: 'Warranty end', k_supplier: 'Supplier', k_invoice: 'Invoice', k_price: 'Price', k_repcost: 'Repair spend',
    notes: 'Notes', user_hist: 'User history', th_person: 'Person', th_from: 'From', th_to: 'To', th_dur: 'Duration', th_handover: 'Handover and return',
    current_lbl: 'Current', returned_cond: 'Returned in condition: {c}', never_assigned: 'Never assigned.',
    inc_hist: 'Faults, repairs and part replacements', th_date: 'Date', th_kind: 'Type', th_desc: 'Description', th_parts: 'Parts', th_cost: 'Cost',
    open: 'Open', resolved: 'Resolved', mark_resolved: 'Mark resolved', no_inc: 'No faults logged.',

    people_title: 'Employees', people_sub: 'People who are assigned devices', new_person: 'New employee', search_people: 'Search by name, email or department',
    lbl_situation: 'Employment', f_staff: 'Active', f_left: 'Left', th_name: 'Name', th_loc: 'Location', th_curdev: 'Current devices', th_sit: 'Employment',
    left_on: 'Left {d}', no_match_people: 'Nobody matches the search.',
    back_people: '← Employees', not_found_person: 'That person does not exist.', btn_leave: 'Record leaving', left_since: 'Left on {d}',
    n_person_left: n => `This person has left the company and has ${n} device${n > 1 ? 's' : ''} not returned.`,
    cur_devices: 'Devices assigned now', th_handed: 'Handed over with', no_cur: 'No devices assigned.', past_devices: 'Previous devices', no_hist: 'No history.',
    data: 'Details', k_hired: 'Start date', k_tenure: 'Time at company', k_email: 'Email',

    fd_tag: 'Asset tag', fd_host: 'Device name (hostname)', fd_serial: 'Serial number', fd_model: 'Model', sect_hw: 'Hardware and software',
    fd_cpu: 'Processor model', fd_cpu_ph: 'Intel Core Ultra 7 155U', fd_cores: 'Cores', fd_cpu_speed: 'Max frequency', fd_ram: 'RAM capacity', fd_ram_gen: 'Memory generation', fd_ram_speed: 'Memory frequency',
    fd_disk: 'Storage capacity', fd_disk_type: 'Storage type', hw_hint: 'All hardware details are optional. Leave anything you don’t know as “Not defined”.',
    fd_cpu_rep: 'Replaceable processor', fd_ram_rep: 'Replaceable memory', fd_disk_rep: 'Replaceable storage',
    fd_ram_form: 'Memory form factor', fd_disk_form: 'Form factor', fd_m2: 'M.2 size',
    undef: 'Not defined', rp_yes: 'Yes, replaceable', rp_no: 'No, soldered to the board', rp_yes_s: 'Replaceable', rp_no_s: 'Soldered',
    ff_onboard: 'Soldered on board', ffd_onboard: 'Soldered on board', ffd_25: '2.5-inch', ffd_35: '3.5-inch', ffd_prop: 'Proprietary', unit_aria: 'Unit', not_set: 'Not set', fd_os: 'Operating system', fd_loc: 'Location', fd_enc: 'Disk encrypted',
    sect_net: 'Network', fd_wifi: 'Wi-Fi chip', fd_mac_wifi: 'Wi-Fi MAC', fd_mac_eth: 'Ethernet MAC', mac_ph: 'AA:BB:CC:DD:EE:FF', err_mac: 'MAC addresses must look like AA:BB:CC:DD:EE:FF',
    sect_purchase: 'Purchase and warranty', fd_bought: 'Purchase date', fd_wend: 'Warranty end', fd_supplier: 'Supplier', fd_invoice: 'Invoice no.', fd_price: 'Price ({c})', fd_notes: 'Notes',
    err_required: 'Asset tag and serial number are required', err_dup: 'Another device already has that tag or identification number', f_numbering: 'Tag numbering', num_type: 'By device type', num_global: 'Global, across all devices', num_type_hint: 'Each code counts on its own: {a} and {b} can both exist.', num_global_hint: 'One number for everything: if {a} exists, the next MacBook is {c}, not {b}.',
created: '{tag} added', edit_title: 'Edit {tag}', saved: 'Changes saved',
    fe_name: 'Full name', fe_email: 'Work email', fe_dept: 'Department', fe_depts: 'Departments', fe_locs: 'Locations', no_dept: 'No department', no_loc: 'No location', add_dept: 'Add another department', add_loc: 'Add another location', fe_loc: 'Location', fe_hired: 'Start date', k_contract: 'Contract', ct_indefinido: 'Permanent', ct_temporal: 'Temporary', ct_practicas: 'Internship', ct_all: 'All contracts', ct_unset: 'Not defined', err_person: 'Name and email are required',
    assign_title: 'Assign {tag}', fa_dept: 'Department', err_dept: 'Choose a department', shared_dept: 'Shared by the department', fa_emp: 'Employee', already_has: '(already has {n})', fa_date: 'Handover date', fa_acc: 'Accessories handed over', fa_acc_ph: 'Charger, dock, mouse…', assign_btn: 'Assign', assigned_to: 'Assigned to {name}',
    return_title: 'Return of {tag}', return_intro: '{name} is returning it. They have had it since {d}.', fr_date: 'Return date', fr_cond: 'Physical condition', fr_next: 'After the return',
    next_avail: 'Available in storage', next_rep: 'Send for repair', next_faulty: 'Faulty, cannot be used', next_disc: 'Retire', fr_notes_ph: 'Charger missing, data wiped…', return_prefix: 'Return: ', return_done: 'Return recorded',
    fault_title: 'Log fault on {tag}', fi_date: 'Date', fi_type: 'Type', fi_desc: 'Problem description', fi_parts: 'Parts replaced', fi_cost: 'Cost ({c})', fi_tech: 'Repair service',
    in_war: 'Under warranty until {d}', out_war: 'Out of warranty', fi_rep: 'Send the device for repair now', err_desc: 'Describe the problem',fault_done: 'Fault logged',
    resolve_title: 'Close fault', fs_date: 'Resolution date', fs_cost: 'Final cost ({c})', resolve_done: 'Fault closed',
    status_title: 'Change status of {tag}', fc_new: 'New status', fc_warn: 'Setting it to available, retired or lost closes the assignment to {name}.',
    sect_disposal: 'Only if retiring', fc_dest: 'Destination', fc_cert: 'Data destruction certificate', fc_reason: 'Reason or notes',
    disc_note: a => `Retired on ${a.d}. Destination: ${a.m}.${a.c ? ' Data destruction certificate ' + a.c + '.' : ''}`, status_done: 'Status updated',
    add: 'Add', person_added: '{name} added', edit_person: 'Edit {name}',
    leave_title: 'Record {name} leaving', fl_date: 'Leaving date', fl_pending: a => `They have ${a.n} device${a.n > 1 ? 's' : ''} to recover: ${a.tags}. They stay assigned until you record the return.`, leave_done: 'Leaving recorded',

    set_title: 'Settings', set_sub: 'Configuration for {org}', set_home: 'All settings',
    grp_general: 'General', grp_general_d: 'Organisation name, dates, currency and alerts',
    grp_access: 'Access and security', grp_access_d: 'Who can sign in and with which permissions',
    grp_org: 'Organisation', grp_org_d: 'Company structure and sites',
    grp_catalog: 'Device catalogue', grp_catalog_d: 'What kinds of devices you have and who makes them',
    grp_parts: 'Components', grp_parts_d: 'Processors, graphics, memory and storage saved for reuse',
    set_users: 'Platform users', set_users_sub: 'Who can sign in to the inventory and what they can do',
    set_region: 'Region and format', set_region_sub: 'Dates, currency and general options',
    set_depts: 'Departments', set_depts_sub: 'Assigned to each employee',
    set_locs: 'Offices and locations', set_locs_sub: 'Where devices are kept and where each person works',
    set_types: 'Device types', set_types_sub: 'Device categories and whether they have a built-in screen or battery',
    set_models: 'Models', set_models_sub: 'Manufacturer, model and type of each device',
    set_wifi: 'Wi-Fi chips', set_wifi_sub: 'Wireless network cards and the Wi-Fi generation they support',
    set_ram: 'Memory generations', set_ram_sub: 'RAM generations such as DDR4, DDR5 or LPDDR5X', set_disk: 'Storage types', set_disk_sub: 'Drive technologies such as SSD, HDD or eMMC',
    item_ram: 'memory generation', item_disk: 'storage type', f_simple_name: 'Name',
    menu_lang: 'Language', menu_theme: 'Theme', menu_ui: 'Design', ui_classic: 'Classic', ui_glass: 'Glass', add_menu: 'Add', add_device_d: 'Laptop, desktop, monitor…', add_person_d: 'Someone to assign devices to', account_menu: 'Account menu',
    item_dept: 'department', item_loc: 'location', item_type: 'device type', item_model: 'model', item_wifi: 'Wi-Fi chip', item_user: 'user',
    add_x: 'Add {x}', edit_x: 'Edit {x}', delete: 'Delete', delete_title: 'Delete {name}', delete_body: '“{name}” will be deleted. This cannot be undone.', deleted: 'Deleted',
    in_use_cant: 'Cannot be deleted because it is in use', added_x: '{x} added',
    th_usage: 'In use', u_people: n => n === 1 ? '1 employee' : n + ' employees', u_devices: n => n === 1 ? '1 device' : n + ' devices', u_models: n => n === 1 ? '1 model' : n + ' models', u_none: 'Not used',
    f_name_es: 'Name in Spanish', f_name_en: 'Name in English', f_name_ca: 'Name in Catalan', f_name_hint: 'If you leave one empty, one of the other names is used.', err_name: 'Enter a name',
    f_loc_kind: 'Location type', f_address: 'Address', th_address: 'Address', th_kind: 'Type',
    f_maker: 'Manufacturer', f_model_name: 'Model', f_type: 'Device type', th_maker: 'Manufacturer', th_model: 'Model', err_model: 'Manufacturer and model are required',
    f_chip: 'Chip name', f_chip_ph: 'Intel Wi-Fi 7 BE200', f_gen: 'Wi-Fi generation', th_chip: 'Chip', th_gen: 'Generation', f_bt: 'Bluetooth', th_bt: 'Bluetooth',
    th_role: 'Role', th_last: 'Last sign-in', never: 'Never', f_role: 'Role', f_pass_tmp: 'Initial password', f_pass_new: 'New password', f_pass_hint: 'Leave empty to keep the current one.',
    u_active: 'Active', u_inactive: 'Deactivated', deactivate: 'Deactivate', activate: 'Activate', you: '(you)',
    err_self: 'You cannot deactivate your own account', err_last_admin: 'At least one active administrator must remain', err_email_dup: 'A user with that email already exists', err_username: 'A username can only have lowercase letters, digits, dots, dashes and underscores (at least 2)', err_username_dup: 'A user with that username already exists', f_login_id: 'Email or username', f_username: 'Username', f_username_hint: 'Signs in just like the email. Leave it empty to sign in with the email only.', f_username_hint_new: 'Signs in just like the email. If left empty, one is made from the email.', err_pass: 'Enter a password', err_user: 'Name and email are required',
    user_on: 'Account activated', user_off: 'Account deactivated',
    f_org: 'Organisation name', f_prefix: 'Asset tag prefix', f_prefix_hint: 'Tags are the prefix, the device type’s code and a number, such as {x}',
    f_datefmt: 'Date format', f_currency: 'Currency', f_wdays: 'Warn about warranties ending within (days)',
    df_dmy: 'Day/month/year', df_mdy: 'Month/day/year', df_ymd: 'Year-month-day (ISO)', df_dmydot: 'Day.month.year', region_saved: 'Settings saved', region_preview: 'Preview: {d} · {m}',

    log_created: '{tag} added to the inventory', log_edited: '{tag}: details updated', log_assigned: '{tag} assigned to {name}', log_loan: '{tag} assigned to {name} (loan)',
    log_returned: '{name} returned {tag} ({cond})', log_incident: 'Fault logged on {tag}: {desc}', log_repair: '{tag} sent for repair: {desc}', log_resolved: 'Fault on {tag} resolved',
    log_status: a => `${a.tag} set to “${a.st}”${a.reason ? ': ' + a.reason : ''}`, log_left: a => `${a.name} left the company${a.tags ? '. Still to recover: ' + a.tags : ''}`,
    log_disposed: '{tag} retired and handed to a WEEE recycler', log_setting: 'Settings: {x}',
    es_activo: 'Active',
    es_baja: 'Temporary leave',
    es_salida: 'Left the company',
    btn_situation: 'Change status',
    sit_title: 'Employment status of {name}',
    fs_state: 'Status',
    fs_since: 'Since',
    sit_done: 'Status updated',
    since_d: 'since {d}',
    n_onleave: '{name} has been on temporary leave since {d}.',
    log_onleave: '{name} is on temporary leave',
    log_back: '{name} is active again',
    sect_screen: 'Screen and battery',
    fd_screen: 'Screen size (inches)',
    fd_touch: 'Touchscreen',
    fd_bat: 'Battery health (%)',
    fd_bat_date: 'Measured on',
    k_screen: 'Screen',
    k_battery: 'Battery',
    touch_s: 'Touchscreen',
    notouch_s: 'Not touch',
    bat_measured: 'measured on {d}',
    bat_prev: 'Earlier readings: {x}',
    al_bat: '{tag}: battery at {p}%',
    al_bat_s: 'Below 80%: consider replacing it',
    set_cpus: 'Processors',
    set_cpus_sub: 'Processor models with their cores and maximum frequency',
    item_cpu: 'processor',
    th_cores: 'Cores',
    th_freq: 'Max frequency',
    cpu_hint: 'Cores and frequency are stored with the model and shown on every device that uses it.',
    fd_ram_modules: 'Number of modules',
    fd_ram_modsize: 'Capacity per module',
    ram_mismatch: '{n} × {s} = {t}, which does not match the total capacity',
    set_ramforms: 'Memory form factors',
    set_ramforms_sub: 'Module form factors such as SO-DIMM, DIMM or CAMM2',
    item_ramform: 'memory form factor',
    fd_disk_conn: 'Connector',
    set_diskforms: 'Storage form factors',
    set_diskforms_sub: 'Drive sizes such as M.2 2280 or 2.5-inch',
    item_diskform: 'storage form factor',
    set_conns: 'Storage connectors',
    set_conns_sub: 'Drive interface such as NVMe PCIe 4.0 or SATA',
    item_conn: 'connector',
    sect_gpu: 'Graphics',
    k_gpu: 'Graphics',
    fd_gpu: 'Graphics model',
    fd_gpu_kind: 'Integrated or dedicated',
    gpu_integrated: 'Integrated',
    gpu_dedicated: 'Dedicated',
    sect_sw: 'Software and location',
    grp_network: 'Network',
    grp_network_d: 'Card models, Wi-Fi generations and Bluetooth versions',
    set_wifigens: 'Wi-Fi generations',
    set_wifigens_sub: 'Wireless standards such as Wi-Fi 6E or Wi-Fi 7',
    item_wifigen: 'Wi-Fi generation',
    set_bt: 'Bluetooth versions',
    set_bt_sub: 'Versions such as Bluetooth 5.3',
    item_bt: 'Bluetooth version',
    nic_add: 'Add network card',
    nic_remove: 'Remove',
    nic_type: 'Card type',
    nic_model: 'Model (optional)',
    nic_mac: 'MAC address',
    nic_gen: 'Wi-Fi generation',
    nic_bt: 'Bluetooth',
    nic_speed: 'Maximum speed',
    no_nics: 'No network cards recorded.',
    fd_wext: 'Extended warranty',
    fd_wended: 'The warranty has ended, but the date is unknown',
    w_ended_unknown: 'Expired (date unknown)',
    w_ext_chip: 'Extended',
    w_left: '{x} left',
    th_faults: 'Faults',
    th_holder: 'Held by',
    nobody: 'Nobody',
    k_dest: 'Destination',
    disk_add: 'Add drive',
    disk_n: 'Drive {n}',
    fd_capacity: 'Capacity',
    host_same: 'Also used as the device name (hostname). You can change this in Settings.',
    f_hosttag: 'The device name (hostname) is the same as the asset tag',
    f_hosttag_hint: 'When this is on, there is no hostname to type: each device uses its tag, for example {x}.',
    no_cert: 'no certificate',
    w_ext_hint: 'For an extended warranty, enter the date the extension ends.',
    type_screen: 'Has a built-in screen',
    type_battery: 'Has a battery',
    fd_customname: 'Name (optional)',
    fd_customname_ph: 'Video workstation',
    type_usesname: 'Identified by a name instead of a model (custom build)',
    type_code: 'Code for asset tags', type_code_hint: 'Goes after the prefix and before the number, like LAP in {x}. Without a code, devices are numbered without one.', th_code: 'Code', type_auto: 'Also assign all', auto_none: 'None', auto_laptop: 'Laptops', auto_desktop: 'Desktops', auto_aio: 'All-in-ones', auto_any: 'Computers of any shape', auto_brand: 'From which makers', auto_allbrands: 'All', auto_onlyapple: 'Only Apple', auto_notapple: 'All except Apple', type_auto_hint: 'For computers that match no word or type name. For example: all laptops except Apple ones, or every Apple computer. A specific shape wins over “any shape”.', type_match: 'Assign automatically in the device app', type_match_ph: 'MacBook, ThinkPad', type_match_hint: 'Words separated by commas. A computer whose maker or model contains one of them gets this type. If several match, the longest wins.',
    err_model_req: 'Choose a model, or add one with +',
    no_models: 'No models of this type yet',
    fd_osver: 'Version',
    fd_osed: 'Edition',
    fd_distro: 'Distribution',
    fd_oclp: 'Patched with OCLP',
    fd_ad: 'Joined to Active Directory',
    k_ad: 'Active Directory',
    chip_oclp: 'Patched (OCLP)', chip_oclp_v: 'Patched (OCLP {v})', fd_oclp_ver: 'OCLP version',
    grp_software: 'Software',
    grp_software_d: 'Operating system versions, editions, distributions and their versions',
    set_macver: 'macOS versions',
    set_macver_sub: 'Such as 15 Sequoia or 26 Tahoe',
    item_macver: 'macOS version',
    set_winver: 'Windows versions',
    set_winver_sub: 'Such as 10 or 11 24H2',
    item_winver: 'Windows version',
    set_wined: 'Windows editions',
    set_wined_sub: 'Such as Pro, Home or Enterprise',
    item_wined: 'Windows edition',
    set_distros: 'Linux distributions',
    set_distros_sub: 'Such as Ubuntu, Debian or Fedora',
    item_distro: 'Linux distribution',
    set_linuxver: 'Linux versions',
    set_linuxver_sub: 'Each version belongs to a distribution, such as Ubuntu 24.04 LTS',
    item_linuxver: 'Linux version',
    pick_distro_first: 'Choose a distribution first',
    err_linuxver: 'Choose the distribution and enter the version',
    u_versions: n => n === 1 ? '1 version' : n + ' versions',
    set_gpus: 'Graphics',
    set_gpus_sub: 'Graphics models, whether integrated or dedicated, and their VRAM',
    item_gpu: 'graphics model',
    gpu_hint: 'Integrated or dedicated and VRAM are stored with the model and shown on every device that uses it.',
    th_vram: 'VRAM',
    set_nicmodels: 'Network card models',
    set_nicmodels_sub: 'Wi-Fi and Ethernet cards such as Intel AX211 or Realtek RTL8125',
    item_nicmodel: 'network card model',
    ok_record: 'Record',
    ok_resolve: 'Resolve',
  },
  ca: {
    log_agent_created: '{tag} afegit per l’aplicació de dispositius', log_agent_updated: '{tag} actualitzat per l’aplicació de dispositius',
    install_app: 'Instal·la l’aplicació', install_done: 'Aplicació instal·lada', install_ios_t: 'Afegeix a la pantalla d’inici', install_ios_1: 'Toca el botó Compartir (el quadrat amb una fletxa cap amunt).', install_ios_2: 'Tria «Afegeix a la pantalla d’inici».', install_ios_3: 'Confirma amb «Afegeix». L’aplicació apareixerà amb les altres i s’obrirà a la seva pròpia finestra.', install_mac_t: 'Afegeix al Dock', install_mac_1: 'A la barra de menús de Safari, obre «Arxiu».', install_mac_2: 'Tria «Afegeix al Dock…» i confirma. L’aplicació s’obrirà a la seva pròpia finestra.',
    up_with_updater: 'L’instal·lador d’aquest servidor comprova GitHub cada hora i pot instal·lar les versions noves.', up_no_updater: 'L’instal·lador automàtic no està actiu en aquest servidor, així que les versions noves s’instal·len a mà (ho explica el README).', up_install: 'Instal·la {v}', up_confirm_t: 'Instal·la la versió {v}', up_confirm_b1: 'Abans de començar es fa una còpia de seguretat completa.', up_confirm_b2: 'L’aplicació estarà en manteniment uns minuts; la resta d’usuaris veurà un avís.', up_confirm_b3: 'Si alguna cosa falla, es torna automàticament a la versió actual amb les seves dades.', up_confirm_ok: 'Instal·la', up_title: 'Instal·lant la versió {v}', up_title_other: 'Instal·lant una actualització', up_queued: 'Esperant l’instal·lador…', up_note: 'Pots tancar aquesta pàgina: la instal·lació continua al servidor.', up_watch: '{name} està instal·lant una actualització. Quan acabi, la pàgina es recarregarà sola.', up_watch_auto: 'S’està instal·lant una actualització automàtica. Quan acabi, la pàgina es recarregarà sola.', up_ph_backup: 'Fent una còpia de seguretat…', up_ph_download: 'Descarregant la versió nova…', up_ph_build: 'Preparant la versió nova…', up_ph_restart: 'Reiniciant l’aplicació…', up_ph_check: 'Comprovant que tot funciona…', up_ph_rollback: 'Alguna cosa ha fallat: tornant a la versió anterior…', up_done: 'Versió {v} instal·lada. Recarregant…', up_done_generic: 'Actualització instal·lada. Recarregant…', up_installed_toast: 'Ara fas servir la versió {v}.', up_result_rolled_back: 'L’actualització no ha funcionat i s’ha tornat a la versió anterior. {msg}', up_result_failed: 'No s’ha pogut instal·lar l’actualització. {msg}', up_auto_h: 'Actualitzacions automàtiques', up_auto_on: 'Instal·la les versions noves automàticament', up_auto_hour: 'Cada dia a les', up_auto_d: 'A aquesta hora (la del servidor) s’instal·la l’última versió publicada, si n’hi ha una de nova, amb còpia de seguretat i tornada enrere si alguna cosa falla. Mai no s’instal·len versions de prova. Si falla, no es torna a provar fins l’endemà.', up_history: 'Historial', up_th_date: 'Data', up_th_version: 'Versió', up_th_how: 'Com', up_th_result: 'Resultat', up_how_auto: 'Automàtica', up_how_manual: 'Per {name}', up_st_queued: 'En cua', up_st_running: 'Instal·lant', up_st_done: 'Instal·lada', up_st_failed: 'No instal·lada', up_st_rolled_back: 'Revertida', up_no_history: 'Encara no s’ha instal·lat cap actualització des d’aquí.', up_steps_1: 'Quan es publica una versió nova a GitHub, apareix aquí.', up_steps_2: 'Prem «Instal·la», o deixa que s’instal·li sola a l’hora triada.', up_steps_3: 'L’instal·lador fa una còpia de seguretat, instal·la la versió i comprova que funciona; si no, torna enrere sol.', err_no_updater: 'L’instal·lador automàtic no respon en aquest servidor.', err_update_stale: 'Aquesta versió ja no és l’última disponible. Torna a comprovar les actualitzacions.', err_update_busy: 'Ja hi ha una actualització o una restauració en curs.', log_update_requested: 'Instal·lació de la versió {v} sol·licitada',
    ab_access: 'Accés a GitHub', ab_access_app: 'GitHub App', ab_access_token: 'Token', ab_access_none: 'Sense configurar (només repositoris públics)', ab_st_app_missing: 'La GitHub App no està instal·lada al repositori, o no hi té accés. Instal·la-la i tria aquest repositori.', ab_st_app_key: 'Falta la clau privada de la GitHub App o no és vàlida. Revisa APP_UPDATE_GITHUB_APP_ID i la clau al servidor.',
    set_updates: 'Actualitzacions', set_updates_sub: 'Cerca versions noves publicades a GitHub', ab_current: 'Versió instal·lada', ab_how_h: 'Com s’instal·la una versió nova', ab_how_1: 'Es publica una versió nova (release) a GitHub; es prova i es prepara automàticament.', ab_how_2: 'Fes una còpia de seguretat a Configuració › Dades › Còpies de seguretat.', ab_how_3: 'Qui gestiona el servidor desplega la versió nova. Els canvis a la base de dades s’apliquen sols en arrencar.',
    bk_log_label: 'Entrades de l’historial', ab_python: 'Python', ab_django: 'Django', ab_postgres: 'PostgreSQL',
    set_about: 'Quant a', set_about_sub: 'Versió, dades i tecnologia de l’aplicació', ab_version: 'Versió', ab_build: 'Compilació', ab_env: 'Entorn', ab_env_production: 'Producció', ab_env_development: 'Desenvolupament', ab_since: 'En ús des de', ab_tz: 'Zona horària', ab_data: 'Dades', ab_dbsize: 'Mida de la base de dades', ab_tech: 'Tecnologia', ab_loading: 'Carregant…', ab_unknown: 'Desconeguda', ab_updates: 'Actualitzacions', ab_repo: 'Es comparen amb les versions publicades a GitHub ({repo}).', ab_check: 'Cerca actualitzacions', ab_checking: 'Cercant…', ab_never: 'Encara no s’ha comprovat.', ab_checked: 'Comprovat el {d}.', ab_st_current: 'Tens l’última versió ({v}).', ab_st_update: 'Hi ha una versió nova: {v}', ab_published: 'Publicada el {d}.', ab_open: 'Mostra-la a GitHub', ab_install: 'Per instal·lar-la, desplega la versió nova al servidor. Fes abans una còpia de seguretat.', ab_st_none: 'Encara no s’ha publicat cap versió a GitHub.', ab_st_private: 'No es pot consultar el repositori perquè és privat. Connecta una GitHub App de només lectura (o un token) al servidor, com explica el README.', ab_st_auth: 'GitHub ha rebutjat l’accés: el token o la GitHub App no són vàlids o no tenen accés al repositori.', ab_st_error: 'No s’ha pogut connectar amb GitHub. Torna-ho a provar més tard.', ab_st_off: 'La cerca d’actualitzacions està desactivada (APP_UPDATE_REPO).',
    mt_title: 'Estem fent tasques de manteniment', mt_body: 'L’aplicació de {org} no està disponible durant uns minuts.', mt_auto: 'Aquesta pàgina s’actualitzarà sola quan torni a estar disponible.', mt_watch: '{name} està restaurant una còpia de seguretat. Quan acabi, es tancarà la sessió de tots els usuaris.', mt_done: 'Restauració acabada. Torna a iniciar sessió.', mt_back: 'L’aplicació torna a estar disponible.', maintenance: 'L’aplicació està en manteniment.', err_maintenance_busy: 'Ja hi ha una altra restauració en curs.', pr_finishing: 'Comprovant les dades restaurades…',
    pr_keep_open: 'No tanquis ni recarreguis aquesta pàgina fins que acabi.',
    pr_export: 'Exportant la còpia', pr_prepare: 'Preparant les dades…', pr_prepare_enc: 'Preparant i xifrant les dades…', pr_download: 'Descarregant el fitxer…', pr_check: 'Comprovant la còpia', pr_upload: 'Pujant el fitxer…', pr_read: 'Llegint la còpia…', pr_restore: 'Restaurant la còpia', pr_restoring: 'Substituint les dades…', pr_step: 'Pas {n} de {total}', pr_left: 'Queden uns {t}', pr_elapsed: '{t} en curs', pr_leave: 'Hi ha una còpia de seguretat en curs.',
    bk_encrypt: 'Protegeix amb contrasenya (recomanat)', bk_encrypt_d: 'La còpia es xifra amb AES-256 i només es pot obrir amb aquesta contrasenya.', bk_pw: 'Contrasenya de la còpia', bk_pw2: 'Repeteix la contrasenya', bk_pw_lost: 'Desa-la en un lloc segur: si la perds, no hi haurà manera de restaurar aquesta còpia.', bk_plain_warn: 'Sense contrasenya, qualsevol que tingui el fitxer podrà llegir totes les dades.', bk_pw_t: 'Còpia protegida', bk_pw_d: 'Aquesta còpia està protegida amb contrasenya. Escriu-la per veure què conté.', bk_unlock: 'Obre', bk_enc_yes: 'Protegida amb contrasenya', err_bk_pw_short: 'La contrasenya de la còpia ha de tenir almenys 10 caràcters.', err_backup_password: 'La contrasenya no és correcta o el fitxer està malmès.', err_backup_password_required: 'Aquesta còpia està protegida amb contrasenya.',
    grp_data: 'Dades', grp_data_d: 'Còpies de seguretat i restauració', set_data: 'Còpies de seguretat', set_data_sub: 'Exporta totes les dades o restaura una còpia anterior', bk_export_h: 'Exporta una còpia', bk_export_d: 'Descarrega un fitxer .invbackup amb totes les dades i la configuració: dispositius, empleats, historial, avaries, usuaris, llistes, logotip i ajustos.', bk_export_warn: 'Conté dades personals i les contrasenyes dels usuaris (xifrades). Desa el fitxer en un lloc segur.', bk_export_btn: 'Descarrega la còpia', bk_exported: 'Còpia descarregada', bk_restore_h: 'Restaura una còpia', bk_restore_d: 'Carrega un fitxer .invbackup exportat des d’aquesta aplicació.', bk_restore_warn: 'Se substituiran totes les dades i la configuració actuals per les de la còpia i es tancarà la sessió de tots els usuaris, inclosa la teva. No es pot desfer.', bk_restore_btn: 'Restaura des d’un fitxer', bk_confirm_t: 'Restaura la còpia', bk_confirm_b: 'Còpia del {d}, feta per {by}. Conté:', bk_n_devices: '{n} dispositius', bk_n_employees: '{n} empleats', bk_n_users: '{n} usuaris', bk_n_log: '{n} entrades de l’historial', bk_first: 'Descarrega abans una còpia de les dades actuals', bk_restore_ok: 'Restaura', bk_restored: 'Còpia restaurada. Torna a iniciar sessió.', err_backup_invalid: 'Aquest fitxer no és una còpia vàlida d’aquesta aplicació.', err_backup_version: 'Aquesta còpia és d’una altra versió de l’aplicació i no es pot restaurar aquí.', err_backup_no_admin: 'La còpia no té cap administrador actiu, així que ningú no podria entrar.', err_backup_size: 'El fitxer és massa gran (màxim 50 MB).', log_backup_export: 'Còpia de seguretat exportada', log_backup_restore: 'Còpia de seguretat restaurada',
    set_brand: 'Logotip', set_brand_sub: 'Substitueix la icona de l’aplicació per la de la teva empresa.', brand_upload: 'Puja una imatge', brand_change: 'Canvia la imatge', brand_remove: 'Treu el logotip', brand_formats: 'PNG, JPG, WebP, GIF o SVG de fins a 512 KB. Millor si és quadrada i amb fons transparent.', brand_where: 'Es veurà al menú, a la pantalla d’inici de sessió i a la pestanya del navegador.', brand_saved: 'Logotip actualitzat', brand_removed: 'S’ha tornat a la icona original', err_logo_type: 'Aquest fitxer no és una imatge compatible.', err_logo_size: 'La imatge pesa més de 512 KB.', go_home: 'Ves al resum', pc_title: 'Canvia la contrasenya', pc_sub: 'Per seguretat, tria una contrasenya nova abans de continuar.', pc_current: 'Contrasenya actual', pc_new: 'Contrasenya nova', pc_repeat: 'Repeteix la contrasenya nova', pc_btn: 'Canvia', pc_done: 'Contrasenya canviada', err_pw_current: 'La contrasenya actual no és correcta.', err_pw_same: 'La contrasenya nova ha de ser diferent de l’actual.', err_must_change: 'Abans de continuar, canvia la contrasenya.', f_must_change: 'Demana que canviï la contrasenya en iniciar sessió', f_must_change_d: 'Útil quan li dones una contrasenya temporal.', chip_must_change: 'Ha de canviar la contrasenya', chip_must_change_d: 'Haurà de triar una contrasenya nova la propera vegada que iniciï sessió.', log_pwchanged: '{name} ha canviat la contrasenya',
    pw_h: 'Seguretat de les contrasenyes', pw_enforce: 'Exigeix requisits de seguretat', pw_enforce_d: 'Les contrasenyes que no els compleixin no s’acceptaran.', pw_off: 'Sense requisits: s’acceptarà qualsevol contrasenya.', pw_minlabel: 'Longitud mínima', pw_chars: 'caràcters', pw_c_upper: 'Almenys una majúscula', pw_c_number: 'Almenys un número', pw_c_symbol: 'Almenys un símbol', pw_c_min: 'Almenys {n} caràcters', pw_weak: 'Contrasenya insegura', pw_ok: 'Contrasenya acceptable', pw_strong: 'Contrasenya segura', pw_empty: 'Escriu una contrasenya per veure’n la seguretat', pw_applies: 'S’aplica a les contrasenyes noves o canviades. Les actuals continuen funcionant.', set_pwpolicy: 'Contrasenyes', set_pwpolicy_sub: 'Tria quins requisits han de complir les contrasenyes.', err_pw_minlen: 'La longitud mínima ha de ser un número entre 1 i 128.',
    su_title: 'Configuració inicial', su_sub: 'Deixa l’aplicació a punt en tres passos.', su_step: 'Pas {n} de 3', su_org_h: 'La teva organització', su_org: 'Nom de l’organització', su_prefix: 'Prefix de les etiquetes', su_date: 'Format de data', su_currency: 'Moneda', su_token: 'Codi d’instal·lació', su_token_hint: 'El defineix qui ha desplegat l’aplicació (DJANGO_SETUP_TOKEN).', su_places_h: 'Oficines i departaments', su_locs: 'Ubicacions', su_locs_hint: 'On són els equips. Marca’n una com a magatzem perquè els equips retornats hi tornin.', su_depts: 'Departaments', su_depts_hint: 'Opcional: també els pots afegir després a Configuració.', su_add_loc: 'Afegeix una ubicació', su_add_dept: 'Afegeix un departament', su_name: 'Nom', su_remove: 'Treu', su_admin_h: 'El teu compte d’administrador', su_admin_sub: 'Amb aquest compte entraràs i podràs crear els de la resta de l’equip.', su_fullname: 'Nom complet', su_email: 'Correu electrònic', su_pass: 'Contrasenya', su_pass2: 'Repeteix la contrasenya', su_back: 'Enrere', su_next: 'Següent', su_finish: 'Acaba', su_blocked_t: 'Falta el codi d’instal·lació', su_blocked_b: 'La instal·lació encara no es pot completar: defineix la variable DJANGO_SETUP_TOKEN al servidor i recarrega aquesta pàgina.', su_done: 'Tot a punt! Ja pots afegir els teus dispositius.', err_su_org: 'Indica el nom de l’organització.', err_su_loc: 'Afegeix almenys una ubicació amb nom.', err_su_admin: 'Omple el teu nom i un correu vàlid.', err_su_mismatch: 'Les contrasenyes no coincideixen.', err_setup_token: 'El codi d’instal·lació no és correcte.', err_setup_done: 'L’aplicació ja està configurada. Inicia sessió.', log_setup: 'Instal·lació inicial completada',
    err_network: 'No s’ha pogut connectar amb el servidor. Torna-ho a provar.', err_forbidden: 'No tens permís per fer això.', err_invalid: 'Hi ha dades no vàlides. Revisa el formulari.', err_conflict: 'El dispositiu ha canviat. Recarrega la pàgina i torna-ho a provar.', err_not_found: 'Aquest registre ja no existeix.', err_dates: 'La data de fi no pot ser anterior a la d’inici.', err_asg_dates: 'La data de lliurament no pot ser anterior a l’última devolució d’aquest equip.', err_fix_dates: 'La data de resolució no pot ser anterior a la de l’avaria.', err_serial_dup: 'Ja hi ha un altre dispositiu amb aquest número de sèrie.', err_auth: 'La sessió ha caducat. Torna a iniciar sessió.', err_pass_weak: 'La contrasenya no compleix els requisits de seguretat.', login_locked: 'Massa intents. Espera 15 minuts i torna-ho a provar.',
    brand: 'Inventari d’equips', nav_summary: 'Resum', nav_devices: 'Dispositius', nav_people: 'Empleats',
    cancel: 'Cancel·la', save: 'Desa', close: 'Tanca', lang_group: 'Idioma', theme_group: 'Tema', theme_auto: 'Fes servir el tema del sistema', theme_light: 'Tema clar', theme_dark: 'Tema fosc',
    yes: 'Sí', no: 'No', none: 'Cap', plus_aria: 'Afegeix {x}',
    st_uso: 'En ús', st_disponible: 'Disponible', st_reparacion: 'En reparació', st_averiado: 'Avariat', st_descartado: 'Retirat', st_perdido: 'Perdut / robat',
    it_fault: 'Avaria', it_repair: 'Reparació', it_part: 'Canvi de peça', it_maint: 'Manteniment', it_loss: 'Pèrdua / robatori',
    cd_good: 'Bo', cd_worn: 'Desgastat', cd_damaged: 'Malmès',
    ds_recycle: 'Reciclat', ds_sale: 'Venda', ds_donation: 'Donació', ds_lease: 'Retornat a l’empresa que el llogava',
    lk_office: 'Oficina', lk_remote: 'Teletreball', lk_storage: 'Magatzem',
    age_lt: 'menys d’1 mes', age_y: n => n === 1 ? '1 any' : n + ' anys', age_m: n => n === 1 ? '1 mes' : n + ' mesos', age_and: ' i ',

    login_title: 'Inicia la sessió', login_sub: 'Inventari d’equips de {org}', f_email: 'Correu electrònic', f_pass: 'Contrasenya', login_btn: 'Entra',
    login_err: 'El correu, el nom d’usuari o la contrasenya no són correctes.', login_off: 'Aquest compte està desactivat. Demana a un administrador que l’activi.',
    logout: 'Tanca la sessió', settings: 'Configuració', no_perm: 'Només els administradors poden obrir la configuració.',
    role_admin: 'Administrador', role_tech: 'Tècnic IT', role_read: 'Només lectura',
    role_admin_d: 'Tot, inclosos la configuració i els usuaris', role_tech_d: 'Gestiona equips, empleats i avaries', role_read_d: 'Consulta l’inventari sense canviar res',

    summary_title: 'Resum', summary_sub: '{n} equips actius · valor de compra {v}', new_device: 'Dispositiu nou', retired_stat: 'Retirats o perduts',
    attention: 'Requereix atenció', nothing: 'No hi ha res pendent.',
    al_recover: 'Recupera {tag}', al_recover_s: '{name} va deixar l’empresa el {date} i encara el té assignat',
    al_inc: 'Incidència oberta a {tag}', al_inc_s: '{desc} · des del {date}',
    al_war: 'La garantia de {tag} venç d’aquí a {n} dies', al_enc: '{tag} sense xifratge de disc', al_enc_s: 'Activa el xifratge (BitLocker, FileVault o LUKS) abans que surti de l’oficina',
    by_dept: 'Equips en ús per departament', activity: 'Activitat recent',

    devices_title: 'Dispositius', devices_sub: 'Equips de l’empresa',
    search_dev: 'Cerca per etiqueta, nom, núm. de sèrie, MAC, model o persona', lbl_search_in: 'Cerca a', search_in: 'Cerca a «{x}»', sf_all: 'Totes les dades', sf_tag: 'Etiqueta', sf_name: 'Nom de l’equip', sf_serial: 'Núm. de sèrie', sf_model: 'Model', sf_cpu: 'Processador', sf_ram: 'Memòria', sf_disk: 'Emmagatzematge', sf_gpu: 'Gràfics', sf_os: 'Sistema', sf_mac: 'MAC', sf_person: 'Assignat a', lbl_search: 'Cerca', lbl_status: 'Estat', lbl_dept: 'Departament', lbl_type: 'Tipus',
    f_active: 'Tots els actius', f_all: 'Tots', f_alldepts: 'Tots els departaments', f_alltypes: 'Tots els tipus',
    th_tag: 'Etiqueta', th_device: 'Equip', th_assigned: 'Assignat a', th_status: 'Estat', th_warranty: 'Garantia',
    left_badge: 'ha deixat l’empresa', no_match_dev: 'Cap dispositiu no coincideix amb els filtres.',
    w_expired: 'Vençuda', w_expired_on: 'Vençuda el {d}', w_soon: 'Venç d’aquí a {n} dies',

    back_devices: '← Dispositius', not_found_dev: 'Aquest dispositiu no existeix.', back_list: 'Torna a la llista', serial_no: 'Núm. de sèrie',
    btn_return: 'Registra la devolució', btn_assign: 'Assigna',
    health_ok: 'Estat correcte', health_warning: 'Amb avisos', health_failing: 'Fallant', wear_pct: 'Desgast {n} %', hours_on: '{n} h d’ús', disk_checked: 'Llegit per l’app de registre el {d}', disk_prev: 'abans: {x}', bat_cycles: '{n} cicles',
    al_places_lost: 'Cap empleat no té departament ni ubicació', al_places_lost_s: 'Restaurar una còpia feta amb les versions 1.10.0 a 1.15.0 els perdia. Si en vas restaurar una, torna a assignar-los o restaura una còpia nova.',
    al_faulty: '{tag} està avariat', al_faulty_s: 'No es pot fer servir: envia’l a reparar, substitueix-lo o retira’l.',
    al_disk_fail: '{tag}: disc fallant', al_disk_fail_s: '{x}: el mateix disc informa que falla. Fes una còpia de les dades i substitueix-lo.', al_disk_warn: '{tag}: disc amb avisos', al_disk_warn_s: '{x}: el disc informa de problemes; vigila’l.', al_disk_wear: '{tag}: SSD desgastat al {n} %', al_disk_wear_s: '{x}: s’acosta al final de la seva vida útil.',
    chk_head: n => n === 1 ? '1 dada a revisar' : n + ' dades a revisar', chk_fix_app: 'Per corregir-ho, torna a passar l’app de registre (0.9.0 o posterior) en aquest equip.', chk_fix_edit: 'Corregeix-ho amb Edita.',
    chk_ignore: 'Ignora', chk_ignore_title: 'Ignora aquest avís', chk_ignore_body: 'L’avís deixarà de mostrar-se per a {tag}, per a tot l’equip d’IT. Fes-ho només si has comprovat que la dada és correcta.', chk_ignored_done: 'Avís ignorat',
    chk_show_ignored: n => n === 1 ? 'Torna a mostrar 1 avís ignorat' : 'Torna a mostrar ' + n + ' avisos ignorats', f_review: 'Amb dades a revisar', al_check: '{tag}: {n} dades a revisar',
    log_check_ignored: '{tag}: avís de dades ignorat', log_check_reset: '{tag}: avisos de dades ignorats, mostrats de nou',
    chk_screen_missing: 'Falta la mida de la pantalla', chk_screen_missing_h: 'Les versions anteriors de l’app no la llegien als Mac ni en alguns portàtils amb Windows.',
    chk_battery_missing: 'Falta la salut de la bateria', chk_battery_missing_h: 'En molts portàtils amb Windows, les versions anteriors de l’app no la llegien.',
    chk_eth_model_missing: 'Falta el model de la targeta Ethernet', chk_eth_model_missing_h: 'Als Mac, les versions anteriors de l’app no el llegien.',
    chk_dup_serial: 'Número de sèrie repetit', chk_dup_serial_h: 'Un altre dispositiu té el mateix número de sèrie; l’app de registre actualitzaria el primer que trobi.',
    chk_dup_mac: 'Adreça MAC repetida', chk_dup_mac_h: 'Un altre dispositiu té una targeta de xarxa amb la mateixa MAC; una de les dues és incorrecta.',
    chk_usb_nic: 'Possible adaptador USB: {x}', chk_usb_nic_h: 'Sembla un adaptador o una base USB, que passa d’un equip a un altre, no la targeta del mateix equip. Les versions anteriors de l’app el registraven.',
    chk_card_number: 'Xip Wi-Fi dubtós: {x}', chk_card_number_h: 'En Mac antics, aquest número és el de la targeta d’Apple, no el del xip.',
    chk_eth_speed: 'Velocitat d’Ethernet impossible', chk_eth_speed_h: 'Més de 100 Gbps: segurament es van escriure megabits amb la unitat en Gbps.',
    chk_disk_size: 'Capacitat de disc exacta: {x}', chk_disk_size_h: 'Segurament és el model de {y}; les versions anteriors guardaven la capacitat exacta en lloc de la que es ven.',
    chk_raid_conn: 'Connector «RAID»', chk_raid_conn_h: 'A Windows, un disc NVMe darrere del controlador d’Intel apareixia com a RAID.',
    chk_conn_missing: 'Disc sense connector', chk_conn_missing_h: 'Un disc no reemplaçable perdia el connector en editar l’equip.',
    chk_mac_dimm: 'Memòria «DIMM» en un Mac', chk_mac_dimm_h: 'Els Mac fan servir SO-DIMM (excepte el Mac Pro); les versions anteriors de l’app hi posaven DIMM.',
    chk_soldered_modules: 'Mòduls en memòria soldada', chk_soldered_modules_h: 'La memòria és soldada però conserva dades de mòduls d’un registre anterior.',
    chk_lpddr_replaceable: 'LPDDR marcada com a reemplaçable', chk_lpddr_replaceable_h: 'La memòria LPDDR va soldada; alguns equips l’anunciaven com a SO-DIMM.',
    chk_arc_dedicated: 'Gràfica integrada marcada com a dedicada', chk_arc_dedicated_h: 'Intel Arc dels Core Ultra va dins del processador, sense memòria pròpia.',
    chk_vram_4: 'Memòria de vídeo de 4 GB', chk_vram_4_h: 'Windows no deia més de 4 GB; si la targeta en té més, la xifra és incorrecta.',
    chk_model_type: 'Model d’un altre tipus', chk_model_type_h: 'El model pertany a un tipus de dispositiu diferent del de l’equip.',
    chk_in_use_nobody: 'En ús sense assignar', chk_in_use_nobody_h: 'És en ús, però no està assignat a ningú.',
    chk_assigned_idle: 'Assignat sense estar en ús', chk_assigned_idle_h: 'Té una assignació oberta, però el seu estat no és «En ús».',
    chk_asg_overlap: 'Assignacions encavalcades', chk_asg_overlap_h: 'Hi ha assignacions que s’encavalquen o que acaben abans de començar; l’historial de qui el tenia no és fiable.',
    chk_fix_before: 'Avaria resolta abans de registrar-se', chk_fix_before_h: 'Una avaria té data de resolució anterior a la de registre.',
    chk_warranty_before: 'Garantia anterior a la compra', chk_warranty_before_h: 'La garantia acaba abans de la data de compra.',
    chk_battery_range: 'Salut de la bateria per sobre del 100 %', chk_battery_range_h: 'Una lectura de bateria de més del 100 % no és possible.', gen_n: n => n + 'a gen.', ultra_s: n => 'Sèrie ' + n, ryzen_s: n => 'sèrie ' + n, reload: 'Actualitza', reloaded: 'Dades actualitzades', mi_to_emp: 'A un empleat', mi_to_emp_d: 'El farà servir una persona', mi_to_dept: 'A un departament', mi_to_dept_d: 'Equip compartit per tot el departament', assign_title_dept: 'Assigna {tag} a un departament', btn_fault: 'Registra una avaria', btn_status: 'Canvia l’estat', btn_edit: 'Edita',
    n_left: '{name} va deixar l’empresa el {date}. Recupera aquest equip i registra’n la devolució.', n_noenc: 'El disc no està xifrat.',
    current: 'Assignació actual', since: 'Des del {d} ({age})', delivered_with: 'Lliurat amb: {x}', out_service: 'Fora de servei.', unassigned_at: 'Sense assignar. És a {loc}.',
    hw: 'Maquinari i programari', k_type: 'Tipus', cores: n => n === 1 ? '1 nucli' : n + ' nuclis', k_cpu: 'Processador', k_ram: 'Memòria', k_disk: 'Emmagatzematge', k_os: 'Sistema', k_enc: 'Xifratge', k_loc: 'Ubicació',
    net: 'Xarxa', k_wifi_chip: 'Xip Wi-Fi', k_wifi_gen: 'Generació', k_mac_wifi: 'MAC Wi-Fi', k_mac_eth: 'MAC Ethernet', no_wifi: 'Sense xip Wi-Fi', no_eth: 'Sense port Ethernet',
    purchase: 'Compra i garantia', k_bought: 'Data de compra', k_age: 'Antiguitat', k_wend: 'Fi de la garantia', k_supplier: 'Proveïdor', k_invoice: 'Factura', k_price: 'Preu', k_repcost: 'Despesa en reparacions',
    notes: 'Notes', user_hist: 'Historial d’usuaris', th_person: 'Persona', th_from: 'Des de', th_to: 'Fins a', th_dur: 'Durada', th_handover: 'Lliurament i devolució',
    current_lbl: 'Actual', returned_cond: 'Retornat en estat: {c}', never_assigned: 'No s’ha assignat mai.',
    inc_hist: 'Avaries, reparacions i canvis de peces', th_date: 'Data', th_kind: 'Tipus', th_desc: 'Descripció', th_parts: 'Peces', th_cost: 'Cost',
    open: 'Oberta', resolved: 'Resolta', mark_resolved: 'Marca com a resolta', no_inc: 'No hi ha incidències registrades.',

    people_title: 'Empleats', people_sub: 'Persones a qui s’assignen equips', new_person: 'Empleat nou', search_people: 'Cerca per nom, correu o departament',
    lbl_situation: 'Situació', f_staff: 'Actius', f_left: 'De baixa', th_name: 'Nom', th_loc: 'Ubicació', th_curdev: 'Equips actuals', th_sit: 'Situació',
    left_on: 'Baixa {d}', no_match_people: 'Ningú no coincideix amb la cerca.',
    back_people: '← Empleats', not_found_person: 'Aquesta persona no existeix.', btn_leave: 'Dona de baixa', left_since: 'Baixa des del {d}',
    n_person_left: n => `Aquesta persona ja no és a l’empresa i té ${n} equip${n > 1 ? 's' : ''} sense retornar.`,
    cur_devices: 'Equips assignats ara', th_handed: 'Lliurat amb', no_cur: 'No té equips assignats.', past_devices: 'Equips anteriors', no_hist: 'Sense historial.',
    data: 'Dades', k_hired: 'Data d’alta', k_tenure: 'Antiguitat', k_email: 'Correu electrònic',

    fd_tag: 'Etiqueta d’inventari', fd_host: 'Nom de l’equip (hostname)', fd_serial: 'Núm. de sèrie', fd_model: 'Model', sect_hw: 'Maquinari i programari',
    fd_cpu: 'Model de processador', fd_cpu_ph: 'Intel Core Ultra 7 155U', fd_cores: 'Nuclis', fd_cpu_speed: 'Freqüència màxima', fd_ram: 'Capacitat de RAM', fd_ram_gen: 'Generació de memòria', fd_ram_speed: 'Freqüència de memòria',
    fd_disk: 'Capacitat d’emmagatzematge', fd_disk_type: 'Tipus d’emmagatzematge', hw_hint: 'Totes les dades de maquinari són opcionals. Deixa «Sense definir» el que no sàpigues.',
    fd_cpu_rep: 'Processador substituïble', fd_ram_rep: 'Memòria substituïble', fd_disk_rep: 'Emmagatzematge substituïble',
    fd_ram_form: 'Format de memòria', fd_disk_form: 'Format', fd_m2: 'Mida M.2',
    undef: 'Sense definir', rp_yes: 'Sí, substituïble', rp_no: 'No, soldat a la placa', rp_yes_s: 'Substituïble', rp_no_s: 'Soldat',
    ff_onboard: 'Soldada a la placa', ffd_onboard: 'Soldat a la placa', ffd_25: '2,5 polzades', ffd_35: '3,5 polzades', ffd_prop: 'Propietari',
    unit_aria: 'Unitat', not_set: 'Sense indicar', fd_os: 'Sistema operatiu', fd_loc: 'Ubicació', fd_enc: 'Disc xifrat',
    sect_net: 'Xarxa', fd_wifi: 'Xip Wi-Fi', fd_mac_wifi: 'MAC Wi-Fi', fd_mac_eth: 'MAC Ethernet', mac_ph: 'AA:BB:CC:DD:EE:FF', err_mac: 'Les adreces MAC han de tenir el format AA:BB:CC:DD:EE:FF',
    sect_purchase: 'Compra i garantia', fd_bought: 'Data de compra', fd_wend: 'Fi de la garantia', fd_supplier: 'Proveïdor', fd_invoice: 'Núm. de factura', fd_price: 'Preu ({c})', fd_notes: 'Notes',
    err_required: 'L’etiqueta i el número de sèrie són obligatoris', err_dup: 'Ja hi ha un dispositiu amb aquesta etiqueta o aquest número identificador', f_numbering: 'Numeració de les etiquetes', num_type: 'Per tipus de dispositiu', num_global: 'Global, per a tots els dispositius', num_type_hint: 'Cada codi compta pel seu compte: {a} i {b} poden conviure.', num_global_hint: 'Un sol número per a tot: si existeix {a}, el següent MacBook serà {c} i no {b}.',
created: '{tag} afegit', edit_title: 'Edita {tag}', saved: 'Canvis desats',
    fe_name: 'Nom complet', fe_email: 'Correu corporatiu', fe_dept: 'Departament', fe_depts: 'Departaments', fe_locs: 'Ubicacions', no_dept: 'Sense departament', no_loc: 'Sense ubicació', add_dept: 'Afegeix un altre departament', add_loc: 'Afegeix una altra ubicació', fe_loc: 'Ubicació', fe_hired: 'Data d’alta', k_contract: 'Contracte', ct_indefinido: 'Indefinit', ct_temporal: 'Temporal', ct_practicas: 'Pràctiques', ct_all: 'Tots els contractes', ct_unset: 'Sense definir', err_person: 'El nom i el correu són obligatoris',
    assign_title: 'Assigna {tag}', fa_dept: 'Departament', err_dept: 'Tria un departament', shared_dept: 'Equip compartit del departament', fa_emp: 'Empleat', already_has: '(ja en té {n})', fa_date: 'Data de lliurament', fa_acc: 'Accessoris lliurats', fa_acc_ph: 'Carregador, dock, ratolí…', assign_btn: 'Assigna', assigned_to: 'Assignat a {name}',
    return_title: 'Devolució de {tag}', return_intro: 'El retorna {name}, que el té des del {d}.', fr_date: 'Data de devolució', fr_cond: 'Estat físic', fr_next: 'Després de la devolució',
    next_avail: 'Disponible al magatzem', next_rep: 'Envia a reparar', next_faulty: 'Avariat, no es pot fer servir', next_disc: 'Retira', fr_notes_ph: 'Falta el carregador, esborrat de dades fet…', return_prefix: 'Devolució: ', return_done: 'Devolució registrada',
    fault_title: 'Registra una avaria a {tag}', fi_date: 'Data', fi_type: 'Tipus', fi_desc: 'Descripció del problema', fi_parts: 'Peces canviades', fi_cost: 'Cost ({c})', fi_tech: 'Servei tècnic',
    in_war: 'En garantia fins al {d}', out_war: 'Fora de garantia', fi_rep: 'Envia l’equip a reparar ara', err_desc: 'Descriu el problema',fault_done: 'Incidència registrada',
    resolve_title: 'Tanca la incidència', fs_date: 'Data de resolució', fs_cost: 'Cost final ({c})', resolve_done: 'Incidència tancada',
    status_title: 'Canvia l’estat de {tag}', fc_new: 'Estat nou', fc_warn: 'Si el passes a disponible, retirat o perdut, es tancarà l’assignació a {name}.',
    sect_disposal: 'Només si es retira', fc_dest: 'Destinació', fc_cert: 'Certificat de destrucció de dades', fc_reason: 'Motiu o notes',
    disc_note: a => `Retirat el ${a.d}. Destinació: ${a.m}.${a.c ? ' Certificat de destrucció de dades ' + a.c + '.' : ''}`, status_done: 'Estat actualitzat',
    add: 'Afegeix', person_added: '{name} afegit', edit_person: 'Edita {name}',
    leave_title: 'Dona de baixa {name}', fl_date: 'Data de baixa', fl_pending: a => `Té ${a.n} equip${a.n > 1 ? 's' : ''} per recuperar: ${a.tags}. Continuaran assignats fins que en registris la devolució.`, leave_done: 'Baixa registrada',

    set_title: 'Configuració', set_sub: 'Configuració de {org}', set_home: 'Tota la configuració',
    grp_general: 'General', grp_general_d: 'Nom de l’organització, dates, moneda i avisos',
    grp_access: 'Accés i seguretat', grp_access_d: 'Qui pot entrar i amb quins permisos',
    grp_org: 'Organització', grp_org_d: 'Estructura de l’empresa i les seves seus',
    grp_catalog: 'Catàleg d’equips', grp_catalog_d: 'Quins tipus d’equips teniu i de quins fabricants',
    grp_parts: 'Components', grp_parts_d: 'Processadors, gràfiques, memòria i emmagatzematge registrats per reutilitzar-los',
    set_users: 'Usuaris de la plataforma', set_users_sub: 'Qui pot entrar a l’inventari i què hi pot fer',
    set_region: 'Regió i format', set_region_sub: 'Dates, moneda i opcions generals',
    set_depts: 'Departaments', set_depts_sub: 'S’assignen a cada empleat',
    set_locs: 'Oficines i ubicacions', set_locs_sub: 'On són els equips i on treballa cada persona',
    set_types: 'Tipus de dispositiu', set_types_sub: 'Categories d’equips i si tenen pantalla integrada o bateria',
    set_models: 'Models', set_models_sub: 'Fabricant, model i tipus de cada equip',
    set_wifi: 'Xips Wi-Fi', set_wifi_sub: 'Targetes de xarxa sense fil i la generació Wi-Fi que admeten',
    set_ram: 'Generacions de memòria', set_ram_sub: 'Generacions de RAM, com ara DDR4, DDR5 o LPDDR5X', set_disk: 'Tipus d’emmagatzematge', set_disk_sub: 'Tecnologies de disc, com ara SSD, HDD o eMMC',
    item_ram: 'generació de memòria', item_disk: 'tipus d’emmagatzematge', f_simple_name: 'Nom',
    menu_lang: 'Idioma', menu_theme: 'Tema', menu_ui: 'Disseny', ui_classic: 'Clàssic', ui_glass: 'Vidre', add_menu: 'Afegeix', add_device_d: 'Portàtil, sobretaula, monitor…', add_person_d: 'Persona a qui assignar equips', account_menu: 'Menú del compte',
    item_dept: 'departament', item_loc: 'ubicació', item_type: 'tipus de dispositiu', item_model: 'model', item_wifi: 'xip Wi-Fi', item_user: 'usuari',
    add_x: 'Afegeix {x}', edit_x: 'Edita {x}', delete: 'Elimina', delete_title: 'Elimina {name}', delete_body: 'S’eliminarà «{name}». No es pot desfer.', deleted: 'Eliminat',
    in_use_cant: 'No es pot eliminar perquè està en ús', added_x: '{x} afegit',
    th_usage: 'En ús', u_people: n => n === 1 ? '1 empleat' : n + ' empleats', u_devices: n => n === 1 ? '1 equip' : n + ' equips', u_models: n => n === 1 ? '1 model' : n + ' models', u_none: 'Sense ús',
    f_name_es: 'Nom en castellà', f_name_en: 'Nom en anglès', f_name_ca: 'Nom en català', f_name_hint: 'Si en deixes algun de buit, s’hi farà servir un dels altres noms.', err_name: 'Escriu un nom',
    f_loc_kind: 'Tipus d’ubicació', f_address: 'Adreça', th_address: 'Adreça',
    f_maker: 'Fabricant', f_model_name: 'Model', f_type: 'Tipus de dispositiu', th_maker: 'Fabricant', th_model: 'Model', err_model: 'El fabricant i el model són obligatoris',
    f_chip: 'Nom del xip', f_chip_ph: 'Intel Wi-Fi 7 BE200', f_gen: 'Generació Wi-Fi', th_chip: 'Xip', th_gen: 'Generació', f_bt: 'Bluetooth', th_bt: 'Bluetooth',
    th_role: 'Rol', th_last: 'Últim accés', never: 'Mai', f_role: 'Rol', f_pass_tmp: 'Contrasenya inicial', f_pass_new: 'Contrasenya nova', f_pass_hint: 'Deixa-la buida per no canviar-la.',
    u_active: 'Actiu', u_inactive: 'Desactivat', deactivate: 'Desactiva', activate: 'Activa', you: '(tu)',
    err_self: 'No pots desactivar el teu propi compte', err_last_admin: 'Hi ha d’haver almenys un administrador actiu', err_email_dup: 'Ja hi ha un usuari amb aquest correu', err_username: 'El nom d’usuari només pot tenir lletres minúscules, números, punts, guions i guions baixos (com a mínim 2)', err_username_dup: 'Ja hi ha un usuari amb aquest nom d’usuari', f_login_id: 'Correu o nom d’usuari', f_username: 'Nom d’usuari', f_username_hint: 'Serveix per iniciar sessió igual que el correu. Deixa’l buit per entrar només amb el correu.', f_username_hint_new: 'Serveix per iniciar sessió igual que el correu. Si el deixes buit, es crea a partir del correu.', err_pass: 'Escriu una contrasenya', err_user: 'El nom i el correu són obligatoris',
    user_on: 'Compte activat', user_off: 'Compte desactivat',
    f_org: 'Nom de l’organització', f_prefix: 'Prefix de les etiquetes d’inventari', f_prefix_hint: 'Les etiquetes són el prefix, el codi del tipus de dispositiu i un número, com ara {x}',
    f_datefmt: 'Format de data', f_currency: 'Moneda', f_wdays: 'Avisa de les garanties que vencen en els propers (dies)',
    df_dmy: 'Dia/mes/any', df_mdy: 'Mes/dia/any', df_ymd: 'Any-mes-dia (ISO)', df_dmydot: 'Dia.mes.any', region_saved: 'Configuració desada', region_preview: 'Previsualització: {d} · {m}',

    log_created: '{tag} donat d’alta a l’inventari', log_edited: '{tag}: dades actualitzades', log_assigned: '{tag} assignat a {name}', log_loan: '{tag} assignat a {name} (préstec)',
    log_returned: '{name} ha retornat {tag} ({cond})', log_incident: 'Incidència registrada a {tag}: {desc}', log_repair: '{tag} enviat a reparar: {desc}', log_resolved: 'Incidència de {tag} resolta',
    log_status: a => `${a.tag} passa a «${a.st}»${a.reason ? ': ' + a.reason : ''}`, log_left: a => `${a.name} ha deixat l’empresa${a.tags ? '. Pendent de recuperar ' + a.tags : ''}`,
    log_disposed: '{tag} retirat i lliurat a un gestor de RAEE', log_setting: 'Configuració: {x}',
    es_activo: 'Actiu',
    es_baja: 'Baixa temporal',
    es_salida: 'Ha deixat l’empresa',
    btn_situation: 'Canvia la situació',
    sit_title: 'Situació de {name}',
    fs_state: 'Situació',
    fs_since: 'Des de',
    sit_done: 'Situació actualitzada',
    since_d: 'des del {d}',
    n_onleave: '{name} és de baixa temporal des del {d}.',
    log_onleave: '{name} és de baixa temporal',
    log_back: '{name} torna a estar actiu',
    sect_screen: 'Pantalla i bateria',
    fd_screen: 'Mida de pantalla (polzades)',
    fd_touch: 'Pantalla tàctil',
    fd_bat: 'Salut de la bateria (%)',
    fd_bat_date: 'Data de la mesura',
    k_screen: 'Pantalla',
    k_battery: 'Bateria',
    touch_s: 'Tàctil',
    notouch_s: 'No tàctil',
    bat_measured: 'mesurada el {d}',
    bat_prev: 'Mesures anteriors: {x}',
    al_bat: '{tag}: bateria al {p} %',
    al_bat_s: 'Per sota del 80 %: valora canviar-la',
    set_cpus: 'Processadors',
    set_cpus_sub: 'Models de processador amb els nuclis i la freqüència màxima',
    item_cpu: 'processador',
    th_cores: 'Nuclis',
    th_freq: 'Freqüència màx.',
    cpu_hint: 'Els nuclis i la freqüència es desen amb el model i es mostren a cada equip que el faci servir.',
    fd_ram_modules: 'Nombre de mòduls',
    fd_ram_modsize: 'Capacitat de cada mòdul',
    ram_mismatch: '{n} × {s} = {t}, que no coincideix amb la capacitat total',
    set_ramforms: 'Formats de memòria',
    set_ramforms_sub: 'Formats de mòdul, com ara SO-DIMM, DIMM o CAMM2',
    item_ramform: 'format de memòria',
    fd_disk_conn: 'Connector',
    set_diskforms: 'Formats d’emmagatzematge',
    set_diskforms_sub: 'Mides d’unitat, com ara M.2 2280 o 2,5 polzades',
    item_diskform: 'format d’emmagatzematge',
    set_conns: 'Connectors d’emmagatzematge',
    set_conns_sub: 'Interfície de la unitat, com ara NVMe PCIe 4.0 o SATA',
    item_conn: 'connector',
    sect_gpu: 'Gràfics',
    k_gpu: 'Gràfics',
    fd_gpu: 'Model de gràfica',
    fd_gpu_kind: 'Integrada o dedicada',
    gpu_integrated: 'Integrada',
    gpu_dedicated: 'Dedicada',
    sect_sw: 'Programari i ubicació',
    grp_network: 'Xarxa',
    grp_network_d: 'Models de targeta, generacions Wi-Fi i versions de Bluetooth',
    set_wifigens: 'Generacions Wi-Fi',
    set_wifigens_sub: 'Estàndards sense fil, com ara Wi-Fi 6E o Wi-Fi 7',
    item_wifigen: 'generació Wi-Fi',
    set_bt: 'Versions de Bluetooth',
    set_bt_sub: 'Versions com ara Bluetooth 5.3',
    item_bt: 'versió de Bluetooth',
    nic_add: 'Afegeix una targeta de xarxa',
    nic_remove: 'Treu',
    nic_type: 'Tipus de targeta',
    nic_model: 'Model (opcional)',
    nic_mac: 'Adreça MAC',
    nic_gen: 'Generació Wi-Fi',
    nic_bt: 'Bluetooth',
    nic_speed: 'Velocitat màxima',
    no_nics: 'No hi ha targetes de xarxa registrades.',
    fd_wext: 'Garantia ampliada',
    fd_wended: 'La garantia ja ha acabat, però no se’n sap la data',
    w_ended_unknown: 'Vençuda (data desconeguda)',
    w_ext_chip: 'Ampliada',
    w_left: 'en queden {x}',
    th_faults: 'Avaries',
    th_holder: 'El tenia',
    nobody: 'Ningú',
    k_dest: 'Destinació',
    disk_add: 'Afegeix un disc',
    disk_n: 'Disc {n}',
    fd_capacity: 'Capacitat',
    host_same: 'També es fa servir com a nom de l’equip (hostname). Ho pots canviar a la configuració.',
    f_hosttag: 'El nom de l’equip (hostname) és el mateix que l’etiqueta d’inventari',
    f_hosttag_hint: 'Si ho actives, no cal escriure el hostname: cada equip fa servir la seva etiqueta, per exemple {x}.',
    no_cert: 'sense certificat',
    w_ext_hint: 'Amb garantia ampliada, indica la data en què acaba l’ampliació.',
    type_screen: 'Té pantalla integrada',
    type_battery: 'Té bateria',
    fd_customname: 'Nom (opcional)',
    fd_customname_ph: 'Workstation de vídeo',
    type_usesname: 'S’identifica amb un nom en lloc d’un model (muntatge propi)',
    type_code: 'Codi per a les etiquetes', type_code_hint: 'Va després del prefix i abans del número, com LAP a {x}. Sense codi, els equips es numeren sense.', th_code: 'Codi', type_auto: 'Assignar també tots els', auto_none: 'Cap', auto_laptop: 'Portàtils', auto_desktop: 'Sobretaules', auto_aio: 'Tot en un', auto_any: 'Equips de qualsevol forma', auto_brand: 'De quines marques', auto_allbrands: 'Totes', auto_onlyapple: 'Només Apple', auto_notapple: 'Totes excepte Apple', type_auto_hint: 'Per als equips que no coincideixen amb cap paraula ni nom de tipus. Per exemple: tots els portàtils excepte els d’Apple, o tots els equips d’Apple. Una forma concreta guanya a «qualsevol forma».', type_match: 'Assignar automàticament a l’app de registre', type_match_ph: 'MacBook, ThinkPad', type_match_hint: 'Paraules separades per comes. Un equip el fabricant o model del qual en contingui una rep aquest tipus. Si en coincideixen diverses, guanya la més llarga.',
    err_model_req: 'Tria un model, o afegeix-ne un amb +',
    no_models: 'Encara no hi ha models d’aquest tipus',
    fd_osver: 'Versió',
    fd_osed: 'Edició',
    fd_distro: 'Distribució',
    fd_oclp: 'Pedaçat amb OCLP',
    fd_ad: 'Unit al directori actiu',
    k_ad: 'Directori actiu',
    chip_oclp: 'Pedaçat (OCLP)', chip_oclp_v: 'Pedaçat (OCLP {v})', fd_oclp_ver: 'Versió d’OCLP',
    grp_software: 'Programari',
    grp_software_d: 'Versions de sistema operatiu, edicions, distribucions i les seves versions',
    set_macver: 'Versions de macOS',
    set_macver_sub: 'Com ara 15 Sequoia o 26 Tahoe',
    item_macver: 'versió de macOS',
    set_winver: 'Versions de Windows',
    set_winver_sub: 'Com ara 10 o 11 24H2',
    item_winver: 'versió de Windows',
    set_wined: 'Edicions de Windows',
    set_wined_sub: 'Com ara Pro, Home o Enterprise',
    item_wined: 'edició de Windows',
    set_distros: 'Distribucions de Linux',
    set_distros_sub: 'Com ara Ubuntu, Debian o Fedora',
    item_distro: 'distribució de Linux',
    set_linuxver: 'Versions de Linux',
    set_linuxver_sub: 'Cada versió pertany a una distribució, com ara Ubuntu 24.04 LTS',
    item_linuxver: 'versió de Linux',
    pick_distro_first: 'Tria primer una distribució',
    err_linuxver: 'Tria la distribució i escriu la versió',
    u_versions: n => n === 1 ? '1 versió' : n + ' versions',
    set_gpus: 'Gràfiques',
    set_gpus_sub: 'Models de gràfica, si són integrades o dedicades i la seva VRAM',
    item_gpu: 'gràfica',
    gpu_hint: 'Si és integrada o dedicada i la VRAM es desen amb el model i es mostren a cada equip que el faci servir.',
    th_vram: 'VRAM',
    set_nicmodels: 'Models de targeta de xarxa',
    set_nicmodels_sub: 'Targetes Wi-Fi i Ethernet, com ara Intel AX211 o Realtek RTL8125',
    item_nicmodel: 'model de targeta de xarxa',
    ok_record: 'Registra',
    ok_resolve: 'Resol',
  },
};

const PREF_KEY = 'inventario-prefs';
let prefs = { lang: null, theme: 'auto', ui: 'glass', uiChosen: false };
try { Object.assign(prefs, JSON.parse(localStorage.getItem(PREF_KEY) || '{}')); } catch (e) {}
// Glass is the default design; Classic stays available and is kept only for people who picked it themselves
if (!prefs.uiChosen) prefs.ui = 'glass';
const LANGS = ['es', 'ca', 'en'];
let lang = LANGS.includes(prefs.lang) ? prefs.lang : (l => l.startsWith('ca') ? 'ca' : l.startsWith('es') ? 'es' : 'en')((navigator.language || 'es').toLowerCase());
const savePrefs = () => { try { localStorage.setItem(PREF_KEY, JSON.stringify({ lang, theme: prefs.theme, ui: prefs.ui, uiChosen: prefs.uiChosen })); } catch (e) {} };

function t(k, a) {
  const v = I18N[lang][k] ?? I18N.es[k] ?? k;
  return typeof v === 'function' ? v(a) : v.replace(/\{(\w+)\}/g, (_, x) => a?.[x] ?? '');
}
const T = (k, a) => esc(t(k, a));
const tx = v => v && typeof v === 'object' ? (v[lang] || v.es || v.en || '') : (v ?? '');
const L = (es, en, ca) => ({ es, en, ca: ca ?? es });
const ST = ['uso', 'disponible', 'reparacion', 'averiado', 'descartado', 'perdido'];
const TIPOS_INC = ['fault', 'repair', 'part', 'maint', 'loss'];
const CONDS = ['good', 'worn', 'damaged'];
const DISPOSAL = ['recycle', 'sale', 'donation', 'lease'];
const EMP_STATES = ['activo', 'baja', 'salida'];
const LOC_KINDS = ['office', 'remote', 'storage'];
const ROLES = ['admin', 'tech', 'read'];
const RAM_FORMS = ['sodimm', 'dimm', 'camm', 'camm2', 'lpcamm2', 'onboard'];
const DISK_FORMS = ['m2', '25', '35', 'msata', 'u2', 'prop', 'onboard'];
const M2_SIZES = ['2230', '2242', '2260', '2280', '22110'];
const FF_FIXED = { sodimm: 'SO-DIMM', dimm: 'DIMM', camm: 'CAMM', camm2: 'CAMM2', lpcamm2: 'LPCAMM2', m2: 'M.2', msata: 'mSATA', u2: 'U.2' };
const ramFormLabel = k => FF_FIXED[k] || (k === 'onboard' ? t('ff_onboard') : '');
const diskFormLabel = k => FF_FIXED[k] || (k ? t('ffd_' + k) : '');
const m2Label = k => `${k} (${k.slice(0, 2)} × ${k.slice(2)} mm)`;
const repOpts = sel => opts([['', t('undef')], ['yes', t('rp_yes')], ['no', t('rp_no')]], sel || '');
const UNITS = { cpu: ['GHz', 'MHz'], ram: ['GB', 'MB', 'TB'], ramSpeed: ['MT/s', 'MHz'], disk: ['GB', 'TB'] };
const WIFI_GENS = [['wifi4', 'Wi-Fi 4 (802.11n)'], ['wifi5', 'Wi-Fi 5 (802.11ac)'], ['wifi6', 'Wi-Fi 6 (802.11ax)'], ['wifi6e', 'Wi-Fi 6E (802.11ax · 6 GHz)'], ['wifi7', 'Wi-Fi 7 (802.11be)']];
const BT_VERS = ['', '4.2', '5.0', '5.1', '5.2', '5.3', '5.4'];
const DATE_FMTS = ['dmy', 'mdy', 'ymd', 'dmydot'];
const CURRENCIES = ['EUR', 'USD', 'GBP', 'CHF', 'MXN', 'COP', 'ARS', 'CLP'];
const st = k => t('st_' + k), itp = k => t('it_' + k), cd = k => t('cd_' + k), dsp = k => t('ds_' + k), lk = k => t('lk_' + k), rl = k => t('role_' + k);
const genLabel = g => (WIFI_GENS.find(x => x[0] === g) || ['', '—'])[1];
const genShort = g => genLabel(g).split(' (')[0];

/* theme */
const hostTheme = document.documentElement.getAttribute('data-theme');
function applyUi() {
  const glass = prefs.ui === 'glass';
  if (glass) document.documentElement.setAttribute('data-ui', 'glass'); else document.documentElement.removeAttribute('data-ui');
  // Glass: the add button floats in the bottom-right corner; Classic: it sits next to the tabs
  const w = $('#addWrap'); w.classList.toggle('fab', glass);
  if (glass) document.body.appendChild(w); else $('#tabs').appendChild(w);
  document.querySelectorAll('#uiSeg button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.uiSet === (prefs.ui === 'glass' ? 'glass' : 'classic'))));
}
function applyTheme() {
  const r = document.documentElement;
  if (prefs.theme === 'light' || prefs.theme === 'dark') r.setAttribute('data-theme', prefs.theme);
  else if (hostTheme) r.setAttribute('data-theme', hostTheme);
  else r.removeAttribute('data-theme');
  document.querySelectorAll('#themeSeg button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.themeSet === prefs.theme)));
}

/* ================= data ================= */
const COLLECTIONS = ['users', 'types', 'depts', 'locations', 'models', 'cpus', 'gpus', 'ramGens', 'ramForms', 'diskTypes', 'diskForms', 'diskConns', 'wifiGens', 'btVers',
  'macVersions', 'winVersions', 'winEditions', 'linuxDistros', 'linuxVersions', 'nicModels', 'employees', 'devices', 'assignments', 'incidents', 'log'];
function emptyState(settings) { const out = { settings: settings || { orgName: '', tagPrefix: '', dateFmt: 'dmy', currency: 'EUR', warrantyDays: 90, hostnameIsTag: false } }; COLLECTIONS.forEach(c => out[c] = []); return out; }
let S = emptyState();

/* ================= server ================= */
class ApiFail extends Error { constructor(code, status) { super(code); this.code = code; this.status = status; } }
const csrfToken = () => (document.cookie.split('; ').find(c => c.startsWith('csrftoken=')) || '').split('=')[1] || '';
async function api(method, url, body, opts = {}) {
  const form = body instanceof FormData;   // file uploads go as a form, everything else as JSON
  let r;
  try {
    r = await fetch('/api/' + url, { method, credentials: 'same-origin',
      headers: form ? { 'X-CSRFToken': csrfToken() } : { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken() },
      body: body === undefined ? undefined : form ? body : JSON.stringify(body) });
  } catch (e) { throw new ApiFail('err_network', 0); }
  if (r.ok && opts.file) return { blob: await r.blob(), name: ((r.headers.get('Content-Disposition') || '').match(/filename="([^"]+)"/) || [])[1] || 'download' };
  if (!(r.headers.get('Content-Type') || '').includes('json')) throw new ApiFail('err_network', 0);   // e.g. the web server's maintenance page during an update
  const data = await r.json().catch(() => ({}));
  if (!r.ok) {
    if (r.status === 401 && cur) signedOut();   // the session expired while the page was open
    if (r.status === 503 && data.error === 'maintenance') enterMaintenance(data.maintenance);
    if (data.error === 'err_must_change' && cur && !cur.mustChange) { cur.mustChange = true; document.querySelectorAll('dialog[open]').forEach(x => x.close()); applyChrome(); route(); }
    throw new ApiFail(data.error || 'err_invalid', r.status);
  }
  return data;
}
function adopt(d) { S = d.state || emptyState(d.settings || S.settings); cur = d.me; }
function signedOut() { cur = null; S = emptyState(S.settings); document.querySelectorAll('dialog[open]').forEach(x => x.close()); applyChrome(); route(); }
async function reload() { adopt(await api('GET', 'state')); }
/* a button for the pages that show inventory data: fetches it again, to see what others (or the device app) changed */
const reloadBtn = () => `<button class="iconbtn reloadbtn" type="button" data-reload aria-label="${T('reload')}" title="${T('reload')}"><svg class="i" viewBox="0 0 24 24"><path d="M20 12a8 8 0 1 1-2.34-5.66"/><path d="M20 4v5h-5"/></svg></button>`;
function ignoreCheck(id, key) {
  const d = dev(id), c = dataChecks(d).find(x => x.k === key);
  if (!c) return;
  openDialog(t('chk_ignore_title'), `<p style="margin:0 0 8px"><b>${T('chk_' + key, c.args)}</b></p><p class="muted" style="margin:0">${T('chk_ignore_body', { tag: d.tag })}</p>`, async () => {
    await mutate('POST', `devices/${id}/checks`, { key }); return t('chk_ignored_done');
  }, t('chk_ignore'));
}
async function reloadNow(btn) {
  if (btn.classList.contains('busy')) return;
  btn.classList.add('busy'); btn.disabled = true;
  try { await reload(); applyChrome(); route(); toast(t('reloaded'), true); }
  catch (err) { if (!(err instanceof ApiFail)) throw err; if (err.status !== 401) toast(t(err.code)); }
  finally { btn.classList.remove('busy'); btn.disabled = false; }
}
/* send a change, then show what the server now holds; a failed refresh must not look like a failed save */
async function mutate(method, url, body) { const d = await api(method, url, body); await reload().catch(() => {}); return d; }

/* ================= session ================= */
let cur = null;
const can = p => !!cur && (p === 'admin' ? cur.rol === 'admin' : p === 'edit' ? cur.rol !== 'read' : true);
const initials = n => n.split(/\s+/).filter(Boolean).slice(0, 2).map(w => w[0]).join('').toUpperCase();

/* ================= helpers ================= */
const $ = s => document.querySelector(s);
function esc(v) { return String(v ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])); }
const today = () => { const d = new Date(); return new Date(d.getTime() - d.getTimezoneOffset() * 6e4).toISOString().slice(0, 10); };
function fmt(d, f = S.settings.dateFmt) {
  if (!d) return '—';
  const [y, m, dd] = d.split('-');
  return f === 'mdy' ? `${m}/${dd}/${y}` : f === 'ymd' ? `${y}-${m}-${dd}` : f === 'dmydot' ? `${dd}.${m}.${y}` : `${dd}/${m}/${y}`;
}
const daysUntil = d => Math.round((new Date(d + 'T00:00:00') - new Date(today() + 'T00:00:00')) / 864e5);
const locale = () => ({ es: 'es-ES', ca: 'ca-ES', en: 'en-GB' })[lang] || 'es-ES';
const money = (n, c = S.settings.currency) => { try { return (Number(n) || 0).toLocaleString(locale(), { style: 'currency', currency: c, maximumFractionDigits: 0 }); } catch (e) { return n + ' ' + c; } };
const curSym = () => { try { return new Intl.NumberFormat(locale(), { style: 'currency', currency: S.settings.currency }).formatToParts(0).find(p => p.type === 'currency').value; } catch (e) { return S.settings.currency; } };
const byId = (coll, id) => S[coll].find(x => x.id === id);
const model = id => byId('models', id) || { fabricante: '', nombre: '—', typeId: '' };
const modelName = m => `${m.fabricante} ${m.nombre}`.trim();
const typeName = id => tx(byId('types', id)?.nombre) || '—';
const deptName = id => tx(byId('depts', id)?.nombre) || '—';
const locName = id => tx(byId('locations', id)?.nombre) || '—';
/* an employee's departments and offices (each can be several) */
const deptNames = e => (e.depts || []).map(deptName).join(', ') || '—';
/* who has a device under an assignment: a person, or a whole department (a shared device) */
/* the device page's Assign button: a menu to give it to a person or to a whole department */
const assignMenu = d => `<div class="menuwrap"><button class="btn primary" type="button" id="assignBtn" data-menu="assignMenu" aria-haspopup="true" aria-expanded="false">${T('btn_assign')}<svg class="i chev" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg></button>
  <div class="menu" id="assignMenu" hidden>
    <button class="mi" type="button" data-act="asignar" data-id="${d.id}"><svg class="i" viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7"/></svg><span class="txt"><span>${T('mi_to_emp')}</span><small>${T('mi_to_emp_d')}</small></span></button>
    <button class="mi" type="button" data-act="asignarDepto" data-id="${d.id}"><svg class="i" viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14c2.2.6 3.5 2.6 3.5 6"/></svg><span class="txt"><span>${T('mi_to_dept')}</span><small>${T('mi_to_dept_d')}</small></span></button>
  </div></div>`;
const holderName = a => !a ? '' : a.deptId ? deptName(a.deptId) : (emp(a.employeeId)?.nombre || '—');
const holderCell = a => {
  if (!a) return '';
  if (a.deptId) return `<b>${esc(deptName(a.deptId))}</b><span class="t2">${T('shared_dept')}</span>`;
  const p = emp(a.employeeId);
  return p ? `<a href="#empleado-${p.id}">${esc(p.nombre)}</a><span class="t2">${esc(deptNames(p))}</span>` : '—';
};
const locNames = e => (e.locs || []).map(locName).join(', ') || '—';
const emp = id => byId('employees', id);
const dev = id => byId('devices', id);
const openAsg = devId => S.assignments.find(a => a.deviceId === devId && !a.hasta);
const isRetired = d => d.estado === 'descartado' || d.estado === 'perdido';
const storageLoc = () => S.locations.find(l => l.tipo === 'storage')?.id;
const pill = (k, label) => `<span class="pill st-${k}">${esc(label || st(k))}</span>`;
const tagLink = d => `<a class="tag" href="#dispositivo-${d.id}">${esc(d.tag)}</a>`;
const logText = l => { const a = { ...l.a }; for (const x in a) a[x] = tx(a[x]); if (a.xKey) a.x = t(a.xKey); if (a.cond) a.cond = cd(a.cond).toLowerCase(); if (a.st) a.st = st(a.st); return t(l.k, a); };
const nf = v => Number(v).toLocaleString(locale(), { maximumFractionDigits: 2, useGrouping: false });
const has = v => v !== '' && v !== null && v !== undefined && !isNaN(Number(v)) && Number(v) > 0;
const withUnit = (v, u) => has(v) ? `${nf(v)} ${u}` : '';
const listName = (coll, id) => byId(coll, id)?.nombre || '';
/* a drive's own health data, as the device app read it: state, SSD wear, hours on, and its earlier readings */
const driveLabel = k => [has(k.size) ? `${String(Number(k.size))} ${k.unit}` : '', listName('diskTypes', k.type)].filter(Boolean).join(' ');
function diskHealth(d, k) {
  const cls = { ok: 'yes', warning: 'warn', failing: 'bad' }[k.health];
  const wear = k.wear !== null && k.wear !== undefined ? `<span class="chip ${k.wear >= 80 ? 'warn' : ''}">${T('wear_pct', { n: nf(k.wear) })}</span>` : '';
  const line = [k.health ? `<span class="chip ${cls}">${T('health_' + k.health)}</span>` : '', wear, has(k.hours) ? `<span class="chip">${T('hours_on', { n: nf(k.hours) })}</span>` : ''];
  const prev = (d.diskLog || []).filter(r => r.drive === driveLabel(k)).map(r => [r.health ? t('health_' + r.health) : '', r.wear !== null ? t('wear_pct', { n: nf(r.wear) }) : '', r.fecha ? `(${fmt(r.fecha)})` : ''].filter(Boolean).join(' '));
  if (!line.some(Boolean)) return '';
  return `${chips(line)}${k.checked ? `<span class="muted" style="display:block;font-size:12.5px">${T('disk_checked', { d: fmt(k.checked) })}${prev.length ? ' · ' + T('disk_prev', { x: prev.join(', ') }) : ''}</span>` : ''}`;
}
const repChip = v => v === 'yes' ? `<span class="chip yes">${T('rp_yes_s')}</span>` : v === 'no' ? `<span class="chip no">${T('rp_no_s')}</span>` : '';
const chips = list => { const h = list.filter(Boolean).join(''); return h ? `<span class="chips">${h}</span>` : ''; };
const cpuOf = d => byId('cpus', d.cpuId);
/* when the setting is on, the hostname is the asset tag, so it is not shown twice */
const hostOf = d => S.settings.hostnameIsTag ? d.tag : d.nombre;
const hostExtra = d => S.settings.hostnameIsTag ? '' : esc(d.nombre);
function cpuDetail(c) { return c ? [has(c.cores) ? t('cores', Number(c.cores)) : '', withUnit(c.speed, c.speedUnit)].filter(Boolean).join(' · ') : ''; }
function ramDetail(d) { return [listName('ramGens', d.ramGen), withUnit(d.ramSpeed, d.ramSpeedUnit)].filter(Boolean).join(' · '); }
const OS_FAMILIES = [['mac', 'macOS'], ['win', 'Windows'], ['linux', 'Linux']];
/* the disk encryption tool depends on the operating system */
const encLabel = fam => fam === 'win' ? 'BitLocker' : fam === 'mac' ? 'FileVault' : fam === 'linux' ? 'LUKS' : t('fd_enc');
function osText(d) {
  if (d.osFamily === 'mac') return ['macOS', listName('macVersions', d.osVerId)].filter(Boolean).join(' ');
  if (d.osFamily === 'win') { const [major, ...rest] = listName('winVersions', d.osVerId).split(' '); return ['Windows', major, listName('winEditions', d.osEditionId), rest.join(' ')].filter(Boolean).join(' '); }
  if (d.osFamily === 'linux') return [listName('linuxDistros', d.osDistroId) || 'Linux', listName('linuxVersions', d.osVerId)].filter(Boolean).join(' ');
  return d.osVersion || '';
}
/* Linux versions belong to a distribution: only that distribution's versions are offered */
const linuxVerOpts = (distroId, selId) => { if (!distroId) return opts([['', t('pick_distro_first')]]); const vs = S.linuxVersions.filter(v => v.distroId === distroId); return opts([['', t('not_set')], ...vs.map(v => [v.id, v.nombre])], selId || ''); };
const gpuOf = d => byId('gpus', d.gpuId);
function gpuDetail(g) { return g ? [g.kind ? t('gpu_' + g.kind) : '', withUnit(g.vram, g.vramUnit) ? 'VRAM ' + withUnit(g.vram, g.vramUnit) : ''].filter(Boolean).join(' · ') : ''; }
const nicModelOpts = (type, selId) => opts([['', t('not_set')], ...S.nicModels.filter(m => m.type === type).map(m => [m.id, m.nombre])], selId || '');
const listOpts = (coll, selId) => opts([['', t('not_set')], ...S[coll].map(x => [x.id, x.nombre])], selId || '');
const devType = d => d.typeId || model(d.modelId).typeId;
/* what the device is called: its model, or for custom builds its own optional name */
const devTitle = d => d.modelId && byId('models', d.modelId) ? modelName(model(d.modelId)) : (d.customName || typeName(devType(d)));
const typeInfo = typeId => byId('types', typeId) || {};
const hasScreen = typeId => !!typeInfo(typeId).hasScreen;
const hasBattery = typeId => !!typeInfo(typeId).hasBattery;
const usesName = typeId => !!typeInfo(typeId).usesName;
const screenTitle = typeId => hasBattery(typeId) && hasScreen(typeId) ? t('sect_screen') : hasBattery(typeId) ? t('k_battery') : t('k_screen');
const modelOpts = (typeId, selId) => { const ms = S.models.filter(m => m.typeId === typeId); return ms.length ? opts(ms.map(m => [m.id, modelName(m)]), selId) : opts([['', t('no_models')]]); };
const triOpts = sel => opts([['', t('undef')], ['yes', t('yes')], ['no', t('no')]], sel || '');
const toGB = (v, u) => u === 'TB' ? v * 1024 : u === 'MB' ? v / 1024 : v;
/* a processor's generation, from its model name: Intel Core i5-8250U -> 8th, i7-1165G7 -> 11th, i9-14900K -> 14th,
   Core Ultra 7 155H -> series 1, AMD Ryzen 5 5600U -> 5000 series; '' when the name does not say (Apple M3...) */
function cpuGen(name) {
  const n = name || '';
  let m = n.match(/Core\s*(?:\(TM\)\s*)?i[3579]-(\d{4,5})/i);
  if (m) { const num = m[1]; return t('gen_n', num.length === 5 || num[0] === '1' ? Number(num.slice(0, 2)) : Number(num[0])); }
  if ((m = n.match(/Core\s*Ultra\s*[3579]\s*(\d)\d{2}/i))) return t('ultra_s', Number(m[1]));
  if ((m = n.match(/Ryzen\s*(?:\d\s*)?(?:PRO\s*)?(\d)\d{3}/i))) return t('ryzen_s', m[1] + '000');
  return '';
}
/* ---- data checks: details that may be wrong because of an earlier bug, or that contradict each other ----
   Each says how it is fixed: 'app' (running the device app 0.9.0 or later on the computer again rewrites it) or 'edit'
   (a person corrects it). Someone can also ignore one for a device, after confirming; it is then hidden for everyone. */
const SOLD_GB = [8, 16, 32, 60, 64, 80, 120, 128, 160, 180, 240, 250, 256, 320, 400, 480, 500, 512, 640, 750, 960, 1000, 1200, 1500, 1920, 2000, 3000, 3840, 4000, 5000, 6000, 8000, 10000, 12000, 16000, 20000, 24000];
const gbLabel = gb => gb >= 1000 ? `${nf(gb / 1000)} TB` : `${nf(gb)} GB`;
function dataChecks(d, all) {
  const out = [], add = (k, fix, args = {}) => { if (!out.some(c => c.k === k)) out.push({ k, fix, args }); };
  const mdl = byId('models', d.modelId), title = devTitle(d);
  const apple = /apple/i.test(mdl?.fabricante || '') || /\b(i?mac|macbook)/i.test(title);
  const nics = d.nics || [], disks = d.disks || [];
  const nicName = n => listName('nicModels', n.modelId);
  // the same serial number or MAC address on another device
  if (d.serial && S.devices.some(x => x !== d && (x.serial || '').toLowerCase() === d.serial.toLowerCase())) add('dup_serial', 'edit');
  if (nics.some(n => n.mac && S.devices.some(x => x !== d && (x.nics || []).some(o => o.mac === n.mac)))) add('dup_mac', 'edit');
  // network: USB adapters and docks saved as the computer's own card, Apple card numbers saved as chips, megabits saved as Gbps
  nics.filter(n => /\busb\b/i.test(nicName(n))).forEach(n => add('usb_nic', 'app', { x: nicName(n) }));
  nics.filter(n => n.type === 'wifi' && /^broadcom bcm[0-9a-f]{1,3}$/i.test(nicName(n))).forEach(n => add('card_number', 'app', { x: nicName(n) }));
  if (nics.some(n => n.type === 'eth' && has(n.speed) && n.speedUnit === 'Gbps' && Number(n.speed) > 100)) add('eth_speed', 'edit');
  // drives: exact sizes instead of the size sold ("1.02 TB", Apple's 500 GB), the old "RAID", a connection erased by editing
  disks.forEach(k => {
    if (!has(k.size)) return;
    const gb = k.unit === 'TB' ? Number(k.size) * 1000 : k.unit === 'MB' ? Number(k.size) / 1000 : Number(k.size);
    const appleSsd = apple && /ssd/i.test(listName('diskTypes', k.type));
    const sizes = appleSsd ? [64, 128, 256, 512, 1000, 2000, 4000, 8000] : SOLD_GB, margin = appleSsd ? 0.06 : 0.03;
    const near = sizes.reduce((b, x) => Math.abs(x - gb) < Math.abs(b - gb) ? x : b, sizes[0]);
    if (Math.abs(near - gb) > 0.5 && Math.abs(near - gb) <= near * margin) add('disk_size', 'app', { x: withUnit(k.size, k.unit), y: gbLabel(near) });
    if (/^raid$/i.test(listName('diskConns', k.conn))) add('raid_conn', 'app');
    if (k.rep === 'no' && !k.conn && d.osFamily) add('conn_missing', 'app');
  });
  // memory: the old "DIMM" for Macs, module details on soldered memory, LPDDR marked replaceable
  if (apple && listName('ramForms', d.ramForm) === 'DIMM' && !/mac ?pro/i.test(title)) add('mac_dimm', 'app');
  if (d.ramRep === 'no' && (has(d.ramModules) || has(d.ramModSize) || d.ramForm)) add('soldered_modules', 'app');
  if (d.ramRep === 'yes' && /^lp/i.test(listName('ramGens', d.ramGen))) add('lpddr_replaceable', 'app');
  // graphics: Intel's built-in Arc saved as a card, video memory capped at 4 GB by Windows
  const g = gpuOf(d);
  if (g && g.kind === 'dedicated' && /\bintel\b.*\barc\b/i.test(g.nombre) && !/\barc\s+(pro\s+)?[ab]\d{2,3}/i.test(g.nombre)) add('arc_dedicated', 'app');
  else if (g && g.kind === 'dedicated' && Number(g.vram) === 4 && g.vramUnit === 'GB' && d.osFamily === 'win') add('vram_4', 'app');
  // details earlier versions of the device app failed to read on some computers (left empty)
  if (d.osFamily && hasScreen(devType(d)) && !has(d.screen) && (d.osFamily === 'mac' || d.osFamily === 'win')) add('screen_missing', 'app');
  if (d.osFamily === 'win' && hasBattery(devType(d)) && !has(d.batHealth)) add('battery_missing', 'app');
  if (d.osFamily === 'mac' && nics.some(n => n.type === 'eth' && !n.modelId)) add('eth_model_missing', 'app');
  // records that contradict each other
  if (mdl && mdl.typeId !== d.typeId) add('model_type', 'edit');
  const a = openAsg(d.id);
  if (d.estado === 'uso' && !a) add('in_use_nobody', 'edit');
  if (a && (d.estado === 'disponible' || isRetired(d))) add('assigned_idle', 'edit');
  const hist = S.assignments.filter(x => x.deviceId === d.id).sort((x, y) => x.desde.localeCompare(y.desde));
  if (hist.some((x, i) => (x.hasta && x.hasta < x.desde) || (i > 0 && (!hist[i - 1].hasta || hist[i - 1].hasta > x.desde)))) add('asg_overlap', 'edit');
  if (S.incidents.some(i => i.deviceId === d.id && i.resuelta && i.resuelta < i.fecha)) add('fix_before', 'edit');
  if (d.compra && d.garantia && d.garantia < d.compra) add('warranty_before', 'edit');
  if (has(d.batHealth) && Number(d.batHealth) > 100) add('battery_range', 'app');
  return all ? out : out.filter(c => !(d.checksIgnored || []).includes(c.k));
}
/* the device page's box: each check, how to fix it, and Ignore (asks first); ignored ones can be shown again */
function checksBox(d) {
  const open = dataChecks(d), ignored = (d.checksIgnored || []).length, ed = can('edit');
  if (!open.length && !ignored) return '';
  const fix = c => c.fix === 'app' ? T('chk_fix_app') : T('chk_fix_edit');
  return `<div class="notice checks">${open.length ? `<b>${T('chk_head', open.length)}</b><ul>${open.map(c => `<li><span><b>${T('chk_' + c.k, c.args)}</b> ${T('chk_' + c.k + '_h', c.args)} <em>${fix(c)}</em></span>${ed ? `<button class="btn small" type="button" data-ignore="${c.k}" data-id="${d.id}">${T('chk_ignore')}</button>` : ''}</li>`).join('')}</ul>` : ''}
    ${ignored && ed ? `<button class="linkbtn" type="button" data-unignore="${d.id}">${T('chk_show_ignored', ignored)}</button>` : ''}</div>`;
}

/* what a device mostly is: processor (and generation), memory, and total storage with its kind */
function specParts(d) {
  const c = cpuOf(d), gen = c ? cpuGen(c.nombre) : '';
  const cpu = c ? c.nombre + (gen ? ` (${gen})` : '') : '';
  const ram = has(d.ramSize) ? `${withUnit(d.ramSize, d.ramUnit)} RAM` : '';
  const disks = (d.disks || []).filter(k => has(k.size));
  const total = disks.reduce((sum, k) => sum + toGB(Number(k.size), k.unit), 0);
  const kinds = [...new Set(disks.map(k => listName('diskTypes', k.type)).filter(Boolean))].join(' + ');
  const disk = total ? [total >= 1024 ? `${nf(Math.round(total / 1024 * 10) / 10)} TB` : `${nf(Math.round(total))} GB`, kinds].filter(Boolean).join(' ') : '';
  return [cpu, ram, disk].filter(Boolean);
}
const specLine = d => specParts(d).join(' · ');
/* the same as HTML that wraps onto more lines only between the parts, never inside one ("8th gen", "1 TB SSD") */
const specHtml = d => { const ps = specParts(d); return ps.map((p, i) => `<span class="nw">${esc(p)}${i < ps.length - 1 ? ' ·' : ''}</span>`).join(' '); };
/* who had the device on a given day, and the faults logged while someone had it */
const holderAt = (devId, date) => S.assignments.find(a => a.deviceId === devId && a.desde <= date && (!a.hasta || a.hasta >= date));
const faultsIn = (devId, from, to) => S.incidents.filter(i => i.deviceId === devId && i.fecha >= from && (!to || i.fecha <= to));
/* employees: activo | baja (temporary leave) | salida (dismissed or resigned) */
const empState = e => e.estado || 'activo';
const hasLeft = e => empState(e) === 'salida';
function empPill(e) {
  const s = empState(e);
  if (s === 'activo') return pill('disponible', t('es_activo'));
  if (s === 'baja') return pill('reparacion', t('es_baja'));
  return pill('descartado', t('es_salida'));
}
const normMac = v => v.trim().toUpperCase().replace(/-/g, ':');
const validMac = v => !v || /^([0-9A-F]{2}:){5}[0-9A-F]{2}$/.test(v);
/* the next asset tag for a device type, as the server suggests it (inventory/tags.py): the prefix, the type's code
   and one more than the highest number in use, counted for that code alone or for every device (Z + LAP + 001) */
const tagCodeType = () => S.types.find(x => x.code) || S.types[0];
const tagParts = (tag, p) => { if (!tag.toLowerCase().startsWith(p.toLowerCase())) return null; const m = tag.slice(p.length).match(/^([A-Za-z]*)(\d+)$/); return m ? [m[1].toUpperCase(), Number(m[2])] : null; };
const nextTag = (typeId = tagCodeType()?.id, p = S.settings.tagPrefix || '', scope = S.settings.tagNumbering || 'type') => {
  const code = typeInfo(typeId).code || '';
  const used = S.devices.map(d => tagParts(d.tag, p)).filter(x => x && (scope === 'global' || x[0] === code));
  return p + code + String(Math.max(0, ...used.map(x => x[1])) + 1).padStart(code ? 3 : 4, '0');
};

function age(from, to) {
  const a = new Date(from + 'T00:00:00'), b = new Date((to || today()) + 'T00:00:00');
  let m = (b.getFullYear() - a.getFullYear()) * 12 + b.getMonth() - a.getMonth();
  if (b.getDate() < a.getDate()) m--;
  if (m < 1) return t('age_lt');
  const y = Math.floor(m / 12), r = m % 12;
  return [y ? t('age_y', y) : '', r ? t('age_m', r) : ''].filter(Boolean).join(t('age_and'));
}
function warranty(d, long) {
  const ext = long && d.garantiaExt === 'yes' ? ` <span class="chip">${T('w_ext_chip')}</span>` : '';
  if (!d.garantia) return d.garantiaEnded ? `<span class="${isRetired(d) ? 'muted' : 'w-past'}">${T('w_ended_unknown')}</span>` : '—';
  const n = daysUntil(d.garantia);
  if (isRetired(d)) return `<span class="muted">${fmt(d.garantia)}</span>${ext}`;
  if (n < 0) return long ? `<span class="w-past">${T('w_expired_on', { d: fmt(d.garantia) })}</span>${ext}` : `<span class="w-past">${T('w_expired')}</span><span class="t2">${fmt(d.garantia)}</span>`;
  if (n <= S.settings.warrantyDays) return `<span class="w-soon">${T('w_soon', { n })}</span>${long ? ` (${fmt(d.garantia)})${ext}` : `<span class="t2">${fmt(d.garantia)}</span>`}`;
  return long ? `${fmt(d.garantia)} <span class="muted">· ${T('w_left', { x: age(today(), d.garantia) })}</span>${ext}` : fmt(d.garantia);
}

let toastT;
const motionOK = () => !matchMedia('(prefers-reduced-motion: reduce)').matches;
function toast(msg, ok) {
  const el = $('#toast');
  el.innerHTML = (ok ? '<svg class="i" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>' : '') + '<span></span>';
  el.lastChild.textContent = msg;
  el.classList.remove('out'); el.hidden = true; void el.offsetWidth; el.hidden = false;   // restart the entrance
  // shown as a popover so it sits above open forms and their blurred backdrop; re-showing puts it on top
  if (el.showPopover) { try { if (el.matches(':popover-open')) el.hidePopover(); el.showPopover(); } catch (e) {} }
  const hide = () => { el.hidden = true; el.classList.remove('out'); if (el.hidePopover) { try { el.hidePopover(); } catch (e) {} } };
  clearTimeout(toastT);
  toastT = setTimeout(() => { if (!motionOK()) { hide(); return; } el.classList.add('out'); setTimeout(hide, 240); }, 2600);
}
function shake(sel) { const el = typeof sel === 'string' ? $(sel) : sel; if (!el) return; el.classList.remove('shake'); void el.offsetWidth; el.classList.add('shake'); setTimeout(() => el.classList.remove('shake'), 520); }
function closeDlg(sel) {
  const d = $(sel); if (!d.open) return;
  if (!motionOK()) { d.close(); return; }
  d.classList.add('closing');
  setTimeout(() => { d.classList.remove('closing'); d.close(); }, 190);
}
/* stagger the new view in, like a sheet of cards settling */
function enter() {
  if (!motionOK()) return;
  const els = [];
  [...view.children].forEach(c => { if (c.matches('.stats, .grid2, .grid3, .setcards, .settings')) els.push(...c.children); else els.push(c); });
  els.slice(0, 14).forEach((el, i) => el.animate([{ opacity: 0, transform: 'translateY(14px) scale(0.985)' }, { opacity: 1, transform: 'none' }],
    { duration: 560, delay: i * 40, easing: 'cubic-bezier(0.22, 1, 0.36, 1)', fill: 'backwards' }));
  view.querySelectorAll('.stat b').forEach(b => {
    const end = Number(b.textContent); if (!end) return;
    const t0 = performance.now(), dur = 700;
    const step = now => { const k = Math.min(1, (now - t0) / dur); b.textContent = Math.round(end * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(step); };
    b.textContent = '0'; requestAnimationFrame(step);
  });
}
/* sliding highlight behind the active tab (Glass design) */
function moveTabInd() {
  const nav = $('#tabs'); let ind = nav.querySelector('.tabind');
  if (!ind) { ind = document.createElement('span'); ind.className = 'tabind'; nav.prepend(ind); }
  const on = nav.querySelector('a.on');
  nav.classList.toggle('has-ind', !!on);
  if (!on || nav.hidden) { ind.style.opacity = 0; return; }
  ind.style.opacity = 1; ind.style.width = on.offsetWidth + 'px'; ind.style.height = on.offsetHeight + 'px';
  ind.style.transform = `translate(${on.offsetLeft}px, ${on.offsetTop}px)`;
  if (!ind.classList.contains('live')) requestAnimationFrame(() => requestAnimationFrame(() => ind.classList.add('live')));
}
/* scrollbar width, so floating buttons can keep an even gap to the window edge */
function measureScrollbar() { document.documentElement.style.setProperty('--sbw', Math.max(0, window.innerWidth - document.documentElement.clientWidth) + 'px'); }
new ResizeObserver(measureScrollbar).observe(document.body);
window.addEventListener('resize', measureScrollbar);
window.addEventListener('resize', () => { const i = $('#tabs .tabind'); if (i) { i.classList.remove('live'); moveTabInd(); } });

/* ================= dialogs ================= */
let dlgSubmit = null, dlg2Submit = null;
function openDialog(title, body, onSubmit, okLabel, danger = false) {
  $('#dlgTitle').textContent = title;
  $('#dlgBody').innerHTML = body;
  $('#dlgOk').textContent = okLabel || t('save');
  $('#dlgOk').hidden = !onSubmit;
  $('#dlgCancel').textContent = onSubmit ? t('cancel') : t('close');
  $('#dlgOk').className = 'btn primary' + (danger ? ' danger' : '');
  dlgSubmit = onSubmit;
  $('#dlg').showModal();
  const first = $('#dlgBody').querySelector('input, select, textarea');
  if (first) first.focus();
}
$('#dlgCancel').onclick = () => closeDlg('#dlg');
$('#dlg').addEventListener('cancel', e => { if (dlgBusy) e.preventDefault(); });
let dlgBusy = false;
$('#dlgForm').addEventListener('submit', async e => {
  e.preventDefault();
  if (dlgBusy) return;
  if (!dlgSubmit) { closeDlg('#dlg'); return; }
  const fd = new FormData(e.target);
  let res;
  dlgBusy = true; $('#dlgOk').disabled = true; $('#dlgCancel').disabled = true;
  try { res = await dlgSubmit(Object.fromEntries(fd), fd); }
  catch (err) { if (!(err instanceof ApiFail)) throw err; if (err.status !== 401) toast(t(err.code)); res = false; }
  finally { dlgBusy = false; $('#dlgOk').disabled = false; $('#dlgCancel').disabled = false; }
  if (res === null) return;   // the dialog moved on to its next step
  if (res === false) { shake('#dlgForm'); return; }
  closeDlg('#dlg'); route();
  if (typeof res === 'string') toast(res, true);
});
$('#dlg2Cancel').onclick = () => closeDlg('#dlg2');
let dlg2Busy = false;
$('#dlg2Form').addEventListener('submit', async e => {
  e.preventDefault();
  if (dlg2Busy) return;
  const fd = new FormData(e.target);
  let res;
  dlg2Busy = true; $('#dlg2Ok').disabled = true;
  try { res = dlg2Submit ? await dlg2Submit(Object.fromEntries(fd), fd) : undefined; }
  catch (err) { if (!(err instanceof ApiFail)) throw err; if (err.status !== 401) toast(t(err.code)); res = false; }
  finally { dlg2Busy = false; $('#dlg2Ok').disabled = false; }
  if (res === false) { shake('#dlg2Form'); return; }
  closeDlg('#dlg2');
});
const opts = (list, sel) => list.map(o => { const [val, lab] = Array.isArray(o) ? o : [o, o]; return `<option value="${esc(val)}"${val === sel ? ' selected' : ''}>${esc(lab)}</option>`; }).join('');
const kopts = (keys, fn, sel) => opts(keys.map(k => [k, fn(k)]), sel);
const PLUS_SVG = '<svg class="i" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>';
/* a select with a + button that opens a quick-add form for that list */
function selPlus(kind, name, id, optionsHtml, nested) {
  const sel = `<select name="${name}" id="${id}">${optionsHtml}</select>`;
  if (nested || !can('edit')) return sel;
  return `<div class="selplus">${sel}<button type="button" class="plus" data-quick="${kind}" data-target="${id}" aria-label="${T('plus_aria', { x: t(LISTS[kind].single) })}" title="${T('plus_aria', { x: t(LISTS[kind].single) })}">${PLUS_SVG}</button></div>`;
}
document.addEventListener('click', e => {
  const b = e.target.closest('[data-quick]');
  if (b) quickAdd(b.dataset.quick, b.dataset.target);
});
function quickAdd(kind, targetId) {
  const C = LISTS[kind];
  $('#dlg2Title').textContent = t('add_x', { x: t(C.single) });
  $('#dlg2Body').innerHTML = C.form(null, true, 'q');
  $('#dlg2Ok').textContent = t('add'); $('#dlg2Cancel').textContent = t('cancel');
  dlg2Submit = async (v, fd) => {
    const r = C.read(v, fd, null); if (!r) return false;
    const { item } = await api('POST', 'lists/' + C.coll, r); S[C.coll].push(item);
    const sel = document.getElementById(targetId);
    if (kind === 'modelos' && targetId === 'f-modelId' && $('#f-typeId')) {
      // the device form lists models by type: switch to the new model's type and select it
      if ($('#f-typeId').value !== item.typeId) { $('#f-typeId').value = item.typeId; $('#f-typeId').dispatchEvent(new Event('change', { bubbles: true })); }
      sel.innerHTML = modelOpts(item.typeId, item.id);
    } else if (kind === 'tarjetas' && sel?.closest('[data-nic]')) {
      const ts = sel.closest('[data-nic]').querySelector('.nic-type');
      if (ts.value !== item.type) { ts.value = item.type; ts.dispatchEvent(new Event('change', { bubbles: true })); }
      sel.innerHTML = nicModelOpts(item.type, item.id);
    } else if (kind === 'linuxver' && targetId === 'f-osVerLinux' && $('#f-osDistro')) {
      if ($('#f-osDistro').value !== item.distroId) $('#f-osDistro').value = item.distroId;
      sel.innerHTML = linuxVerOpts(item.distroId, item.id);
    } else if (sel) { sel.insertAdjacentHTML('beforeend', `<option value="${esc(item.id)}">${esc((C.optLabel || C.label)(item))}</option>`); sel.value = item.id; sel.dispatchEvent(new Event('change', { bubbles: true })); }
    toast(t('added_x', { x: C.label(item) }), true);
  };
  if (kind === 'modelos' && $('#f-typeId') && $('#q-type')) $('#q-type').value = $('#f-typeId').value;
  if (kind === 'linuxver' && $('#f-osDistro')?.value && $('#q-distro')) $('#q-distro').value = $('#f-osDistro').value;
  if (kind === 'tarjetas' && $('#q-type')) { const row = document.getElementById(targetId)?.closest('[data-nic]'); if (row) $('#q-type').value = row.querySelector('.nic-type').value; }
  $('#dlg2').showModal();
  $('#dlg2Body').querySelector('input, select')?.focus();
}

/* ================= editable lists (settings + quick add) ================= */
const biForm = (x, px) => `
  <label>${T('f_name_es')}<input name="es" id="${px}-es" value="${esc(x ? (typeof x.nombre === 'object' ? x.nombre.es : x.nombre) : '')}"></label>
  <label>${T('f_name_en')}<input name="en" id="${px}-en" value="${esc(x ? (typeof x.nombre === 'object' ? x.nombre.en : x.nombre) : '')}"></label>
  <label class="full">${T('f_name_ca')}<input name="ca" id="${px}-ca" value="${esc(x ? (typeof x.nombre === 'object' ? (x.nombre.ca ?? '') : x.nombre) : '')}"></label>
  <span class="hint full">${T('f_name_hint')}</span>`;
const biRead = v => { const es = (v.es || '').trim(), en = (v.en || '').trim(), ca = (v.ca || '').trim(); if (!es && !en && !ca) { toast(t('err_name')); return null; } return { es: es || ca || en, en: en || es || ca, ca: ca || es || en }; };
const usage = (n, key) => n ? t(key, n) : t('u_none');
function simpleList(coll, prefix, title, sub, single, field, uses) {
  const C = { coll, prefix, title, sub, single, label: x => x.nombre, cols: [['th_name', x => `<b>${esc(x.nombre)}</b>`]],
    count: x => S.devices.filter(d => uses ? uses(d, x) : d[field] === x.id).length, usageText: x => usage(C.count(x), 'u_devices'),
    form: (x, nested, px) => `<div class="fields"><label class="full">${T('f_simple_name')}<input name="nombre" id="${px}-nombre" value="${esc(x?.nombre)}"></label></div>`,
    read: v => { if (!v.nombre.trim()) { toast(t('err_name')); return null; } return { nombre: v.nombre.trim() }; } };
  return C;
}
const nicUses = key => (d, x) => (d.nics || []).some(n => n[key] === x.id);
const diskUses = key => (d, x) => (d.disks || []).some(k => k[key] === x.id);
const LISTS = {
  departamentos: { coll: 'depts', prefix: 'dp', title: 'set_depts', sub: 'set_depts_sub', single: 'item_dept',
    label: x => tx(x.nombre), cols: [['th_name', x => esc(tx(x.nombre))]],
    count: x => S.employees.filter(e => (e.depts || []).includes(x.id)).length + S.assignments.filter(a => a.deptId === x.id).length,
    usageText: x => { const p = S.employees.filter(e => (e.depts || []).includes(x.id)).length, d = new Set(S.assignments.filter(a => a.deptId === x.id).map(a => a.deviceId)).size; return p || d ? [p ? t('u_people', p) : '', d ? t('u_devices', d) : ''].filter(Boolean).join(' · ') : t('u_none'); },
    form: (x, nested, px) => `<div class="fields">${biForm(x, px)}</div>`,
    read: v => { const n = biRead(v); return n && { nombre: n }; } },
  ubicaciones: { coll: 'locations', prefix: 'l', title: 'set_locs', sub: 'set_locs_sub', single: 'item_loc',
    label: x => tx(x.nombre), cols: [['th_name', x => esc(tx(x.nombre))], ['th_kind', x => `<span class="chip">${esc(lk(x.tipo))}</span>`], ['th_address', x => esc(tx(x.direccion)) || '<span class="muted">—</span>']],
    count: x => S.devices.filter(d => d.loc === x.id).length + S.employees.filter(e => (e.locs || []).includes(x.id)).length,
    usageText: x => { const d = S.devices.filter(z => z.loc === x.id).length, p = S.employees.filter(z => (z.locs || []).includes(x.id)).length; return d || p ? [d ? t('u_devices', d) : '', p ? t('u_people', p) : ''].filter(Boolean).join(' · ') : t('u_none'); },
    form: (x, nested, px) => `<div class="fields">${biForm(x, px)}
      <label>${T('f_loc_kind')}<select name="tipo" id="${px}-tipo">${kopts(LOC_KINDS, lk, x?.tipo || 'office')}</select></label>
      <label>${T('f_address')}<input name="direccion" id="${px}-dir" value="${esc(tx(x?.direccion))}"></label></div>`,
    read: (v, fd, x) => { const n = biRead(v); return n && { nombre: n, tipo: v.tipo, direccion: x && tx(x.direccion) === v.direccion ? x.direccion : v.direccion.trim() }; } },
  tipos: { coll: 'types', prefix: 't', title: 'set_types', sub: 'set_types_sub', single: 'item_type',
    label: x => tx(x.nombre), cols: [['th_name', x => esc(tx(x.nombre))], ['th_code', x => x.code ? `<span class="tag">${esc(x.code)}</span>` : '<span class="muted">—</span>'], ['k_screen', x => x.hasScreen ? `<span class="chip yes">${T('yes')}</span>` : `<span class="chip no">${T('no')}</span>`], ['k_battery', x => x.hasBattery ? `<span class="chip yes">${T('yes')}</span>` : `<span class="chip no">${T('no')}</span>`]],
    count: x => S.models.filter(m => m.typeId === x.id).length + S.devices.filter(d => d.typeId === x.id).length,
    usageText: x => { const m = S.models.filter(z => z.typeId === x.id).length, d = S.devices.filter(z => z.typeId === x.id).length; return m || d ? [m ? t('u_models', m) : '', d ? t('u_devices', d) : ''].filter(Boolean).join(' · ') : t('u_none'); },
    form: (x, nested, px) => `<div class="fields">${biForm(x, px)}<label class="full">${T('type_code')}<input name="code" id="${px}-code" value="${esc(x?.code)}" maxlength="10" autocapitalize="characters" spellcheck="false" style="text-transform:uppercase"><span class="hint">${T('type_code_hint', { x: (S.settings.tagPrefix || '') + 'LAP001' })}</span></label><label class="full">${T('type_match')}<input name="match" id="${px}-match" value="${esc(x?.match)}" maxlength="300" spellcheck="false" placeholder="${T('type_match_ph')}"><span class="hint">${T('type_match_hint')}</span></label><label>${T('type_auto')}<select name="autoChassis" id="${px}-auto">${opts([['', t('auto_none')], ['any', t('auto_any')], ['laptop', t('auto_laptop')], ['desktop', t('auto_desktop')], ['all_in_one', t('auto_aio')]], x?.autoChassis || '')}</select></label><label>${T('auto_brand')}<select name="autoApple" id="${px}-apple">${opts([['', t('auto_allbrands')], ['only', t('auto_onlyapple')], ['except', t('auto_notapple')]], x?.autoApple || '')}</select></label><span class="hint full" style="margin-top:-8px">${T('type_auto_hint')}</span><label class="check full"><input type="checkbox" name="hasScreen" id="${px}-screen"${x?.hasScreen ? ' checked' : ''}> ${T('type_screen')}</label><label class="check full"><input type="checkbox" name="hasBattery" id="${px}-battery"${x?.hasBattery ? ' checked' : ''}> ${T('type_battery')}</label><label class="check full"><input type="checkbox" name="usesName" id="${px}-usesname"${x?.usesName ? ' checked' : ''}> ${T('type_usesname')}</label></div>`,
    read: (v, fd) => { const n = biRead(v); return n && { nombre: n, code: (v.code || '').toUpperCase().replace(/[^A-Z0-9]/g, ''), match: (v.match || '').split(',').map(w => w.trim()).filter(Boolean).join(', '), autoChassis: v.autoChassis || '', autoApple: v.autoApple || '', hasScreen: fd.has('hasScreen'), hasBattery: fd.has('hasBattery'), usesName: fd.has('usesName') }; } },
  modelos: { coll: 'models', prefix: 'm', title: 'set_models', sub: 'set_models_sub', single: 'item_model',
    label: x => modelName(x), optLabel: x => `${modelName(x)} (${typeName(x.typeId)})`,
    cols: [['th_maker', x => esc(x.fabricante)], ['th_model', x => `<b>${esc(x.nombre)}</b>`], ['th_kind', x => `<span class="chip">${esc(typeName(x.typeId))}</span>`]],
    count: x => S.devices.filter(d => d.modelId === x.id).length, usageText: x => usage(LISTS.modelos.count(x), 'u_devices'),
    form: (x, nested, px) => `<div class="fields">
      <label>${T('f_maker')}<input name="fabricante" id="${px}-fab" value="${esc(x?.fabricante)}" list="makers"></label>
      <label>${T('f_model_name')}<input name="nombre" id="${px}-nom" value="${esc(x?.nombre)}"></label>
      <label class="full">${T('f_type')}${selPlus('tipos', 'typeId', px + '-type', opts(S.types.map(y => [y.id, tx(y.nombre)]), x?.typeId), nested)}</label>
      <datalist id="makers">${[...new Set(S.models.map(m => m.fabricante))].map(m => `<option value="${esc(m)}">`).join('')}</datalist></div>`,
    read: v => { if (!v.nombre.trim()) { toast(t('err_name')); return null; } return { fabricante: v.fabricante.trim(), nombre: v.nombre.trim(), typeId: v.typeId }; } },
  graficas: { coll: 'gpus', prefix: 'g', title: 'set_gpus', sub: 'set_gpus_sub', single: 'item_gpu',
    label: x => x.nombre, cols: [['th_name', x => `<b>${esc(x.nombre)}</b>`], ['fd_gpu_kind', x => x.kind ? `<span class="chip">${T('gpu_' + x.kind)}</span>` : '<span class="muted">—</span>'], ['th_vram', x => esc(withUnit(x.vram, x.vramUnit)) || '<span class="muted">—</span>']],
    count: x => S.devices.filter(d => d.gpuId === x.id).length, usageText: x => usage(LISTS.graficas.count(x), 'u_devices'),
    form: (x, nested, px) => `<div class="fields">
      <label class="full">${T('f_simple_name')}<input name="nombre" id="${px}-nombre" value="${esc(x?.nombre)}" placeholder="NVIDIA GeForce RTX 4070"></label>
      <label>${T('fd_gpu_kind')}<select name="kind" id="${px}-kind">${opts([['', t('undef')], ['integrated', t('gpu_integrated')], ['dedicated', t('gpu_dedicated')]], x?.kind || '')}</select></label>
      <label>VRAM<span class="numunit"><input name="vram" id="${px}-vram" type="number" min="0" step="any" value="${esc(x?.vram ?? '')}"><select name="vramUnit" id="${px}-vramUnit" aria-label="${T('unit_aria')}">${opts(['GB', 'MB'], x?.vramUnit || 'GB')}</select></span></label>
      <span class="hint full">${T('gpu_hint')}</span></div>`,
    read: v => { if (!v.nombre.trim()) { toast(t('err_name')); return null; } return { nombre: v.nombre.trim(), kind: v.kind, vram: numOrNull(v.vram), vramUnit: v.vramUnit }; } },
  tarjetas: { coll: 'nicModels', prefix: 'nm', title: 'set_nicmodels', sub: 'set_nicmodels_sub', single: 'item_nicmodel',
    label: x => x.nombre, cols: [['th_name', x => `<b>${esc(x.nombre)}</b>`], ['nic_type', x => `<span class="chip">${x.type === 'wifi' ? 'Wi-Fi' : 'Ethernet'}</span>`]],
    count: x => S.devices.filter(d => (d.nics || []).some(n => n.modelId === x.id)).length, usageText: x => usage(LISTS.tarjetas.count(x), 'u_devices'),
    form: (x, nested, px) => `<div class="fields">
      <label class="full">${T('f_simple_name')}<input name="nombre" id="${px}-nombre" value="${esc(x?.nombre)}" placeholder="Intel Wi-Fi 7 BE200"></label>
      <label class="full">${T('nic_type')}<select name="type" id="${px}-type">${opts([['wifi', 'Wi-Fi'], ['eth', 'Ethernet']], x?.type || 'wifi')}</select></label></div>`,
    read: v => { if (!v.nombre.trim()) { toast(t('err_name')); return null; } return { nombre: v.nombre.trim(), type: v.type }; } },
  procesadores: { coll: 'cpus', prefix: 'c', title: 'set_cpus', sub: 'set_cpus_sub', single: 'item_cpu',
    label: x => x.nombre, cols: [['th_name', x => `<b>${esc(x.nombre)}</b>`], ['th_cores', x => has(x.cores) ? esc(x.cores) : '<span class="muted">—</span>'], ['th_freq', x => esc(withUnit(x.speed, x.speedUnit)) || '<span class="muted">—</span>']],
    count: x => S.devices.filter(d => d.cpuId === x.id).length, usageText: x => usage(LISTS.procesadores.count(x), 'u_devices'),
    form: (x, nested, px) => `<div class="fields">
      <label class="full">${T('f_simple_name')}<input name="nombre" id="${px}-nombre" value="${esc(x?.nombre)}" placeholder="${T('fd_cpu_ph')}"></label>
      <label>${T('fd_cores')}<input name="cores" id="${px}-cores" type="number" min="1" step="1" value="${esc(x?.cores ?? '')}"></label>
      <label>${T('fd_cpu_speed')}<span class="numunit"><input name="speed" id="${px}-speed" type="number" min="0" step="any" value="${esc(x?.speed ?? '')}"><select name="speedUnit" id="${px}-speedUnit" aria-label="${T('unit_aria')}">${opts(UNITS.cpu, x?.speedUnit || 'GHz')}</select></span></label>
      <span class="hint full">${T('cpu_hint')}</span></div>`,
    read: v => { if (!v.nombre.trim()) { toast(t('err_name')); return null; } return { nombre: v.nombre.trim(), cores: numOrNull(v.cores), speed: numOrNull(v.speed), speedUnit: v.speedUnit }; } },
  memoria: simpleList('ramGens', 'rg', 'set_ram', 'set_ram_sub', 'item_ram', 'ramGen'),
  formatosram: simpleList('ramForms', 'rf', 'set_ramforms', 'set_ramforms_sub', 'item_ramform', 'ramForm'),
  almacenamiento: simpleList('diskTypes', 'dt', 'set_disk', 'set_disk_sub', 'item_disk', null, diskUses('type')),
  formatosdisco: simpleList('diskForms', 'df', 'set_diskforms', 'set_diskforms_sub', 'item_diskform', null, diskUses('form')),
  conectores: simpleList('diskConns', 'cn', 'set_conns', 'set_conns_sub', 'item_conn', null, diskUses('conn')),
  macos: simpleList('macVersions', 'mv', 'set_macver', 'set_macver_sub', 'item_macver', null, (d, x) => d.osFamily === 'mac' && d.osVerId === x.id),
  winver: simpleList('winVersions', 'wv', 'set_winver', 'set_winver_sub', 'item_winver', null, (d, x) => d.osFamily === 'win' && d.osVerId === x.id),
  winedition: simpleList('winEditions', 'we', 'set_wined', 'set_wined_sub', 'item_wined', null, (d, x) => d.osFamily === 'win' && d.osEditionId === x.id),
  distros: { ...simpleList('linuxDistros', 'ld', 'set_distros', 'set_distros_sub', 'item_distro', null, (d, x) => d.osFamily === 'linux' && d.osDistroId === x.id),
    // a distribution with versions cannot be deleted either
    count: x => S.devices.filter(d => d.osFamily === 'linux' && d.osDistroId === x.id).length + S.linuxVersions.filter(v => v.distroId === x.id).length,
    usageText: x => { const d = S.devices.filter(z => z.osFamily === 'linux' && z.osDistroId === x.id).length, v = S.linuxVersions.filter(z => z.distroId === x.id).length; return d || v ? [v ? t('u_versions', v) : '', d ? t('u_devices', d) : ''].filter(Boolean).join(' · ') : t('u_none'); } },
  linuxver: { coll: 'linuxVersions', prefix: 'lv', title: 'set_linuxver', sub: 'set_linuxver_sub', single: 'item_linuxver',
    label: x => [listName('linuxDistros', x.distroId), x.nombre].filter(Boolean).join(' '), optLabel: x => x.nombre,
    cols: [['fd_distro', x => `<span class="chip">${esc(listName('linuxDistros', x.distroId) || '—')}</span>`], ['fd_osver', x => `<b>${esc(x.nombre)}</b>`]],
    count: x => S.devices.filter(d => d.osFamily === 'linux' && d.osVerId === x.id).length, usageText: x => usage(LISTS.linuxver.count(x), 'u_devices'),
    form: (x, nested, px) => `<div class="fields">
      <label>${T('fd_distro')}${selPlus('distros', 'distroId', px + '-distro', opts(S.linuxDistros.map(y => [y.id, y.nombre]), x?.distroId), nested)}</label>
      <label>${T('fd_osver')}<input name="nombre" id="${px}-nombre" value="${esc(x?.nombre)}" placeholder="24.04 LTS"></label></div>`,
    read: v => { if (!v.nombre.trim() || !v.distroId) { toast(t('err_linuxver')); return null; } return { nombre: v.nombre.trim(), distroId: v.distroId }; } },
  wifigen: simpleList('wifiGens', 'wg', 'set_wifigens', 'set_wifigens_sub', 'item_wifigen', null, nicUses('wifiGen')),
  bluetooth: simpleList('btVers', 'bt', 'set_bt', 'set_bt_sub', 'item_bt', null, nicUses('btVer')),
};

/* ================= views ================= */
function viewLogin(err) {
  return `<div class="login"><div class="card">
    <div class="loginhead">${appIcon()}<h1>${T('login_title')}</h1><p class="sub">${T('login_sub', { org: S.settings.orgName })}</p></div>
    <form id="loginForm" novalidate>
      <label>${T('f_login_id')}<input type="text" name="email" id="login-email" autocomplete="username" autocapitalize="none" spellcheck="false" required></label>
      <label>${T('f_pass')}<input type="password" name="pass" id="login-pass" autocomplete="current-password" required></label>
      ${err ? `<p class="err" role="alert">${esc(err)}</p>` : ''}
      <button class="btn primary" type="submit">${T('login_btn')}</button>
    </form>
  </div></div>`;
}
function bindLogin() {
  $('#loginForm').addEventListener('submit', async e => {
    e.preventDefault();
    const v = Object.fromEntries(new FormData(e.target));
    try { adopt(await api('POST', 'login', { email: v.email.trim(), password: v.pass })); }
    catch (err) { if (!(err instanceof ApiFail)) throw err; renderLogin(t(err.code), v.email); shake('.login .card'); return; }
    route(); applyChrome(); enter();
  });
}
/* ================= passwords ================= */
const PW_DEFAULT = { enforce: true, minOn: true, minLen: 10, upper: true, number: true, symbol: true };
const PW_YES = '<svg class="i" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>', PW_NO = '<svg class="i" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg>';
/* the rules the policy currently asks for, each with whether this password meets it (same rules as the server) */
function pwChecks(pw, p) {
  if (!p.enforce) return [];
  const out = [];
  if (p.minOn) out.push([t('pw_c_min', { n: p.minLen }), pw.length >= Number(p.minLen)]);
  if (p.upper) out.push([t('pw_c_upper'), /\p{Lu}/u.test(pw)]);
  if (p.number) out.push([t('pw_c_number'), /\p{Nd}/u.test(pw)]);
  if (p.symbol) out.push([t('pw_c_symbol'), /[^\p{L}\p{N}\s]/u.test(pw)]);
  return out;
}
const pwMeets = (pw, p) => !!pw && pwChecks(pw, p).every(c => c[1]);
const validMinLen = p => !p.enforce || !p.minOn || (Number.isInteger(Number(p.minLen)) && Number(p.minLen) >= 1 && Number(p.minLen) <= 128);
/* 0 insecure, 1 acceptable, 2 secure; a password that breaks an enforced rule is always insecure */
function pwLevel(pw, p) {
  if (!pwMeets(pw, p) || /password|contrase|qwerty|123456|abc123|letmein|admin/i.test(pw) || /^(.)\1*$/.test(pw)) return 0;
  const classes = [/\p{Ll}/u, /\p{Lu}/u, /\p{Nd}/u, /[^\p{L}\p{N}\s]/u].filter(r => r.test(pw)).length;
  const score = [pw.length >= 8, pw.length >= 12, pw.length >= 16, classes >= 2, classes >= 3, classes >= 4].filter(Boolean).length;
  return score >= 5 ? 2 : score >= 3 ? 1 : 0;
}
function drawMeter(el, pw, p) {
  if (!el) return;
  const level = pw ? pwLevel(pw, p) : -1, checks = pwChecks(pw, p);
  el.className = 'pw-meter' + (level >= 0 ? ' l' + level : '');
  el.innerHTML = `<div class="pw-bars" aria-hidden="true"><i></i><i></i><i></i></div>
    <div class="pw-label" role="status">${level < 0 ? T('pw_empty') : T(['pw_weak', 'pw_ok', 'pw_strong'][level])}</div>
    ${checks.length ? `<ul class="pw-list">${checks.map(([label, ok]) => `<li class="${pw ? (ok ? 'yes' : 'no') : ''}">${ok ? PW_YES : PW_NO}${esc(label)}</li>`).join('')}</ul>` : `<p class="pw-d" style="margin:0">${T('pw_off')}</p>`}`;
}
function pwPolicyFields(p) {
  const rule = (key, label) => `<label class="check"><input type="checkbox" data-pw="${key}"${p[key] ? ' checked' : ''}> ${T(label)}</label>`;
  return `<div class="pw-policy">
    <h2>${T('pw_h')}</h2>
    <label class="check"><input type="checkbox" data-pw="enforce"${p.enforce ? ' checked' : ''}> ${T('pw_enforce')}</label>
    <p class="pw-d">${T('pw_enforce_d')}</p>
    <div class="pw-rules"${p.enforce ? '' : ' hidden'}>
      <div class="pw-minrow">${rule('minOn', 'pw_minlabel')}<input type="number" min="1" max="128" step="1" data-pw="minLen" value="${esc(p.minLen)}" aria-label="${T('pw_minlabel')}"${p.minOn ? '' : ' disabled'}><span>${T('pw_chars')}</span></div>
      ${rule('upper', 'pw_c_upper')}${rule('number', 'pw_c_number')}${rule('symbol', 'pw_c_symbol')}
    </div></div>`;
}
function bindPolicy(root, p, onChange) {
  root.addEventListener('input', e => {
    const key = e.target.dataset.pw; if (!key) return;
    p[key] = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    root.querySelector('.pw-rules').hidden = !p.enforce;
    root.querySelector('[data-pw="minLen"]').disabled = !p.minOn;
    if (onChange) onChange();
  });
}
let pwDraft = null;
function settingsPasswords() {
  pwDraft = { ...PW_DEFAULT, ...S.settings.pwPolicy };
  return `<section class="panel"><div class="head"><div><h2>${T('set_pwpolicy')}</h2><p class="sub">${T('set_pwpolicy_sub')}</p></div></div>
    <form id="pwForm" class="regionform" novalidate>${pwPolicyFields(pwDraft)}<p class="muted" style="margin:0;font-size:13px">${T('pw_applies')}</p>
    <div><button class="btn primary" type="submit">${T('save')}</button></div></form></section>`;
}
function bindPwForm() {
  const f = $('#pwForm'); if (!f) return;
  bindPolicy(f, pwDraft);
  f.addEventListener('submit', async e => {
    e.preventDefault();
    if (!validMinLen(pwDraft)) { toast(t('err_pw_minlen')); shake('#pwForm'); return; }
    try { await mutate('PUT', 'settings/password-policy', { ...pwDraft, minLen: Number(pwDraft.minLen) }); } catch (err) { if (err.status !== 401) toast(t(err.code)); return; }
    route(); toast(t('saved'), true);
  });
}

/* ================= first-run setup ================= */
let setupInfo = null, SU = null;
function setupDefaults() {
  return { step: 0, token: '', orgName: '', tagPrefix: 'INV-', dateFmt: 'dmy', currency: 'EUR',
    locations: [{ nombre: '', tipo: 'office' }], depts: [''], policy: { ...PW_DEFAULT }, admin: { nombre: '', email: '', pass: '', pass2: '' } };
}
const TRASH_SVG = '<svg class="i" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg>';
function setupStep() {
  const h = (k, sub) => `<div><h1>${T(k)}</h1>${sub ? `<p class="sub">${T(sub)}</p>` : ''}</div>`;
  if (SU.step === 0) return h('su_title', 'su_sub') + `<h2>${T('su_org_h')}</h2><div class="fields">
    ${setupInfo.tokenRequired ? `<label class="full">${T('su_token')}<input type="password" data-su="token" value="${esc(SU.token)}" autocomplete="off"><span class="hint">${T('su_token_hint')}</span></label>` : ''}
    <label class="full">${T('su_org')}<input data-su="orgName" value="${esc(SU.orgName)}" autocomplete="organization"></label>
    <label class="full">${T('su_prefix')}<input data-su="tagPrefix" value="${esc(SU.tagPrefix)}"></label>
    <label>${T('su_date')}<select data-su="dateFmt">${opts(DATE_FMTS.map(k => [k, fmt(today(), k)]), SU.dateFmt)}</select></label>
    <label>${T('su_currency')}<select data-su="currency">${opts(CURRENCIES, SU.currency)}</select></label></div>`;
  if (SU.step === 1) return h('su_places_h') + `<div class="su-group"><h2>${T('su_locs')}</h2><p class="hint">${T('su_locs_hint')}</p>
      ${SU.locations.map((l, i) => `<div class="su-row"><input data-loc="${i}" value="${esc(tx(l.nombre))}" aria-label="${T('su_name')}"><select data-loctype="${i}" aria-label="${T('su_locs')}">${kopts(LOC_KINDS, lk, l.tipo)}</select><button type="button" class="iconbtn" data-del-loc="${i}" aria-label="${T('su_remove')}" title="${T('su_remove')}">${TRASH_SVG}</button></div>`).join('')}
      <div><button type="button" class="btn small" id="suAddLoc">${T('su_add_loc')}</button></div></div>
    <div class="su-group"><h2>${T('su_depts')}</h2><p class="hint">${T('su_depts_hint')}</p>
      ${SU.depts.map((d, i) => `<div class="su-row"><input data-dept="${i}" value="${esc(d)}" aria-label="${T('su_name')}"><button type="button" class="iconbtn" data-del-dept="${i}" aria-label="${T('su_remove')}" title="${T('su_remove')}">${TRASH_SVG}</button></div>`).join('')}
      <div><button type="button" class="btn small" id="suAddDept">${T('su_add_dept')}</button></div></div>`;
  return h('su_admin_h', 'su_admin_sub') + `<div class="fields">
    <label class="full">${T('su_fullname')}<input data-admin="nombre" value="${esc(SU.admin.nombre)}" autocomplete="name"></label>
    <label class="full">${T('su_email')}<input type="email" data-admin="email" value="${esc(SU.admin.email)}" autocomplete="username"></label>
    <div class="full">${pwPolicyFields(SU.policy)}</div>
    <label>${T('su_pass')}<input type="password" data-admin="pass" value="${esc(SU.admin.pass)}" autocomplete="new-password"></label>
    <label>${T('su_pass2')}<input type="password" data-admin="pass2" value="${esc(SU.admin.pass2)}" autocomplete="new-password"></label>
    <div class="full"><div id="suMeter"></div></div></div>`;
}
function renderSetup() {
  if (setupInfo.blocked) {
    view.innerHTML = `<div class="login"><div class="card setup"><h1>${T('su_blocked_t')}</h1><p class="notice">${T('su_blocked_b')}</p></div></div>`;
    return;
  }
  SU = SU || setupDefaults();
  const last = SU.step === 2;
  view.innerHTML = `<div class="login"><div class="card setup">
    <div class="su-steps" aria-hidden="true">${[0, 1, 2].map(i => `<i class="${i <= SU.step ? 'on' : ''}"></i>`).join('')}</div>
    <p class="su-count">${T('su_step', { n: SU.step + 1 })}</p>
    <form id="setupForm" novalidate style="display:grid;gap:18px">${setupStep()}
      <div class="su-actions">${SU.step ? `<button type="button" class="btn" id="suBack">${T('su_back')}</button>` : ''}<button class="btn primary" type="submit" id="suNext">${T(last ? 'su_finish' : 'su_next')}</button></div>
    </form></div></div>`;
  const form = $('#setupForm');
  form.addEventListener('input', e => {
    const x = e.target, d = x.dataset;
    if (d.su) SU[d.su] = x.value;
    else if (d.admin) { SU.admin[d.admin] = x.value; if (d.admin === 'pass') suMeter(); }
    else if (d.loc) SU.locations[+d.loc].nombre = x.value;   // once edited, the same name is used in every language
    else if (d.loctype) SU.locations[+d.loctype].tipo = x.value;
    else if (d.dept) SU.depts[+d.dept] = x.value;
  });
  form.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    if (b.id === 'suBack') { SU.step--; renderSetup(); }
    else if (b.id === 'suAddLoc') { SU.locations.push({ nombre: '', tipo: 'office' }); renderSetup(); $(`[data-loc="${SU.locations.length - 1}"]`).focus(); }
    else if (b.id === 'suAddDept') { SU.depts.push(''); renderSetup(); $(`[data-dept="${SU.depts.length - 1}"]`).focus(); }
    else if (b.dataset.delLoc) { SU.locations.splice(+b.dataset.delLoc, 1); renderSetup(); }
    else if (b.dataset.delDept) { SU.depts.splice(+b.dataset.delDept, 1); renderSetup(); }
  });
  form.addEventListener('submit', setupNext);
  if (SU.step === 2) { bindPolicy(form.querySelector('.pw-policy'), SU.policy, suMeter); suMeter(); }
  form.querySelector('input')?.focus();
}
const suMeter = () => drawMeter($('#suMeter'), SU.admin.pass, SU.policy);
const setupError = key => { toast(t(key)); shake('.login .card'); };
async function setupNext(e) {
  e.preventDefault();
  const named = SU.locations.filter(l => tx(l.nombre).trim());
  if (SU.step === 0) {
    if (setupInfo.tokenRequired && !SU.token) return setupError('err_setup_token');
    if (!SU.orgName.trim()) return setupError('err_su_org');
  } else if (SU.step === 1) {
    if (!named.length) return setupError('err_su_loc');
  }
  if (SU.step < 2) { SU.step++; renderSetup(); return; }
  const a = SU.admin;
  if (!a.nombre.trim() || !a.email.trim()) return setupError('err_su_admin');
  if (a.pass !== a.pass2) return setupError('err_su_mismatch');
  if (!validMinLen(SU.policy)) return setupError('err_pw_minlen');
  if (!a.pass) return setupError('err_pass');
  if (!pwMeets(a.pass, SU.policy)) return setupError('err_pass_weak');
  const btn = $('#suNext'); btn.disabled = true;
  try {
    adopt(await api('POST', 'setup', { token: SU.token, orgName: SU.orgName.trim(), tagPrefix: SU.tagPrefix.trim(), dateFmt: SU.dateFmt, currency: SU.currency, warrantyDays: 90, hostnameIsTag: false, pwPolicy: { ...SU.policy, minLen: Number(SU.policy.minLen) },
      locations: named, depts: SU.depts.map(d => d.trim()).filter(Boolean), admin: { nombre: a.nombre.trim(), email: a.email.trim(), pass: a.pass } }));
  } catch (err) {
    if (!(err instanceof ApiFail)) throw err;
    if (err.code === 'err_setup_done') { setupInfo = null; SU = null; renderLogin(t(err.code)); return; }
    if (err.code === 'err_setup_token' || err.code === 'err_su_org') { SU.step = 0; renderSetup(); }
    else if (err.code === 'err_su_loc') { SU.step = 1; renderSetup(); }
    else btn.disabled = false;
    setupError(err.code);
    return;
  }
  setupInfo = null; SU = null; location.hash = 'panel'; applyChrome(); route(); enter(); toast(t('su_done'), true);
}

/* ================= progress notification ================= */
/* Real percentages and time left while bytes move between browser and server; while the server itself works
   it reports nothing, so the bar slides and shows the time elapsed instead of a guess. */
const prog = {
  start(title, steps, fullScreen = false) {
    const el = $('#prog');
    this.steps = steps; this.n = 0; this.running = true; this.full = fullScreen; clearTimeout(this.hideT); clearInterval(this.tick);
    el.className = 'prog'; el.hidden = false; $('#progTitle').textContent = title;
    $('#progNote').hidden = !fullScreen; $('#progNote').textContent = t('pr_keep_open');
    if (el.matches(':popover-open')) { try { el.hidePopover(); } catch (e) {} }
    if (fullScreen) {   // a modal cover: everything else on the page becomes unreachable, keyboard included
      $('#busyBox').appendChild(el); $('#busyBox').hidden = false; $('#maintBox').hidden = true;
      if (!$('#busy').open) $('#busy').showModal();
      el.tabIndex = -1; el.focus();
    } else if (el.showPopover) { try { el.showPopover(); } catch (e) {} }
    this.tick = setInterval(() => { this.keepCover(); this.draw(); }, 500);
    window.onbeforeunload = e => { e.preventDefault(); e.returnValue = t('pr_leave'); return t('pr_leave'); };
  },
  phase(label) {   // a new step; its progress is unknown until bytes() reports some
    this.n = Math.min(this.n + 1, this.steps); this.label = label; this.frac = null; this.eta = null; this.t0 = performance.now(); this.draw();
  },
  server(m) {   // progress the server publishes while it restores or installs an update
    if (m.kind === 'update') {   // an update is five steps whose length nobody can predict: show the step and time elapsed
      const label = t('up_ph_' + (m.phase || 'backup'));
      if (label !== this.label) { this.label = label; this.frac = null; this.eta = null; this.t0 = performance.now(); }
      this.steps = m.total || 5; this.n = Math.min((m.done || 0) + 1, this.steps); this.draw();
      return;
    }
    const label = t(m.phase === 'replacing' ? 'pr_restoring' : m.phase === 'finishing' ? 'pr_finishing' : 'pr_read');
    if (label !== this.label) { this.label = label; this.frac = null; this.eta = null; this.t0 = performance.now(); }
    if (m.phase === 'replacing' && m.total) this.bytes(m.done, m.total); else this.draw();
  },
  bytes(loaded, total) {
    if (!total) return;
    this.frac = Math.min(1, loaded / total);
    const secs = (performance.now() - this.t0) / 1000;
    this.eta = secs > 0.4 && loaded > 0 ? (total - loaded) / (loaded / secs) : null;
    this.draw();
  },
  draw() {
    const el = $('#prog'); if (el.hidden || el.classList.contains('done')) return;
    const known = this.frac !== null, secs = (performance.now() - this.t0) / 1000;
    el.classList.toggle('unknown', !known);
    $('#progStep').textContent = this.steps > 1 ? t('pr_step', { n: this.n, total: this.steps }) : '';
    $('#progLabel').textContent = this.label;
    $('#progFill').style.width = known ? (this.frac * 100).toFixed(1) + '%' : '';
    $('#progPct').textContent = known ? Math.floor(this.frac * 100) + ' %' : '';
    $('#progTime').textContent = known ? (this.eta > 1 ? t('pr_left', { t: duration(this.eta) }) : '') : (secs >= 1 ? t('pr_elapsed', { t: duration(secs) }) : '');
  },
  finish(message) {   // success: stays a moment so it can be read
    const el = $('#prog'); this.stop();
    el.classList.remove('unknown'); el.classList.add('done');
    $('#progFill').style.width = '100%'; $('#progLabel').textContent = message; $('#progPct').textContent = '100 %'; $('#progTime').textContent = '';
    $('#progNote').hidden = true;
    this.hideT = setTimeout(() => this.hide(), this.full ? 2200 : 3200);
  },
  keepCover() { if (this.running && this.full && !$('#busy').open) $('#busy').showModal(); },   // nothing may close it while working
  stop() { clearInterval(this.tick); this.running = false; window.onbeforeunload = null; },
  hide() {
    const el = $('#prog'); this.stop(); el.hidden = true;
    if (el.hidePopover) { try { el.hidePopover(); } catch (e) {} }
    if ($('#busy').open) { $('#busy').close(); document.body.appendChild(el); }
  },
};
// the cover cannot be dismissed while work is running (Escape, or the browser closing it anyway)
$('#busy').addEventListener('cancel', e => e.preventDefault());
$('#busy').addEventListener('close', () => { prog.keepCover(); if (maint && !maint.canWatch && !$('#busy').open) $('#busy').showModal(); });
function duration(secs) {
  secs = Math.max(1, Math.round(secs));
  return secs < 60 ? `${secs} s` : `${Math.floor(secs / 60)} min${secs % 60 ? ` ${secs % 60} s` : ''}`;
}
/* downloads with progress: `onBytes(loaded, total)` is called from the moment the server starts sending */
async function apiDownload(url, body, onBytes) {
  let r;
  try { r = await fetch('/api/' + url, { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken() }, body: JSON.stringify(body) }); }
  catch (e) { throw new ApiFail('err_network', 0); }
  if (!r.ok) {
    const data = await r.json().catch(() => ({}));
    if (r.status === 401 && cur) signedOut();
    throw new ApiFail(data.error || 'err_invalid', r.status);
  }
  const total = Number(r.headers.get('Content-Length')) || 0, parts = [];
  let loaded = 0;
  onBytes(0, total);
  const reader = r.body.getReader();
  try {
    for (;;) { const { done, value } = await reader.read(); if (done) break; parts.push(value); loaded += value.length; onBytes(loaded, total); }
  } catch (e) { throw new ApiFail('err_network', 0); }
  const name = ((r.headers.get('Content-Disposition') || '').match(/filename="([^"]+)"/) || [])[1] || 'download';
  return { blob: new Blob(parts), name };
}
/* uploads with progress: `onBytes` while sending, `onSent` once the server has everything and starts working */
function apiUpload(url, form, onBytes, onSent) {
  return new Promise((resolve, reject) => {
    const x = new XMLHttpRequest();
    x.open('POST', '/api/' + url); x.withCredentials = true; x.setRequestHeader('X-CSRFToken', csrfToken());
    x.upload.onprogress = e => { if (e.lengthComputable && onBytes) onBytes(e.loaded, e.total); };
    x.upload.onload = () => { if (onSent) onSent(); };
    x.onload = () => {
      let data = {}; try { data = JSON.parse(x.responseText || '{}'); } catch (e) {}
      if (x.status >= 200 && x.status < 300) { resolve(data); return; }
      if (x.status === 401 && cur) signedOut();
      if (x.status === 503 && data.error === 'maintenance') enterMaintenance(data.maintenance);
      reject(new ApiFail(data.error || 'err_invalid', x.status));
    };
    x.onerror = () => reject(new ApiFail('err_network', 0));
    x.send(form);
  });
}

/* ================= maintenance ================= */
/* While someone restores a backup the server answers everyone else with "maintenance". Administrators
   follow the restore on the full-screen progress view; everyone else sees a maintenance page. Both check
   back every couple of seconds and step aside when the restore ends. */
let maint = null, maintTimer = null;
function enterMaintenance(m) {
  if (prog.running && prog.full && !maint) return;   // this browser is the one doing the restore
  maint = m;
  document.querySelectorAll('dialog[open]').forEach(d => { if (d.id !== 'busy') d.close(); });
  if (m.canWatch) {
    const update = m.kind === 'update';
    if (!prog.running) { prog.start(t(update ? 'up_title_other' : 'pr_restore'), 1, true); prog.phase(t(update ? 'up_ph_backup' : 'pr_read')); window.onbeforeunload = null; }
    $('#progNote').hidden = false;
    $('#progNote').textContent = update ? (m.startedBy ? t('up_watch', { name: m.startedBy }) : t('up_watch_auto')) : t('mt_watch', { name: m.startedBy || '—' });
    prog.server(m);
  } else {
    $('#maintBox').innerHTML = `${appIcon()}<h1>${T('mt_title')}</h1><p class="sub">${T('mt_body', { org: S.settings.orgName })}</p>
      <p class="mt-auto"><span class="prog-icon" aria-hidden="true"></span>${T('mt_auto')}</p>`;
    $('#maintBox').hidden = false; $('#busyBox').hidden = true;
    if (!$('#busy').open) $('#busy').showModal();
  }
  if (!maintTimer) maintTimer = setInterval(pollMaintenance, 2000);
}
async function pollMaintenance() {
  let d;
  try { d = await api('GET', 'maintenance'); } catch (e) { return; }
  if (d.active) {
    maint = d;
    if (d.canWatch && prog.running) prog.server(d);
    if (!$('#busy').open) $('#busy').showModal();
    return;
  }
  clearInterval(maintTimer); maintTimer = null;
  const watched = maint && maint.canWatch, updated = maint && maint.kind === 'update'; maint = null;
  if (updated) {   // a new version may bring a new interface: load it
    if (watched) prog.finish(t('up_done_generic'));
    setTimeout(() => location.reload(), watched ? 2200 : 300);
    return;
  }
  if (watched) prog.finish(t('mt_done'));
  else { $('#busy').close(); $('#maintBox').hidden = true; $('#busyBox').hidden = false; }
  const boot = await api('GET', 'bootstrap').catch(() => null);
  if (boot && boot.me && boot.state) adopt(boot);
  else { cur = null; S = emptyState(boot ? boot.settings : S.settings); setupInfo = boot && boot.setup || null; }
  applyChrome(); route();
  if (!watched) toast(t('mt_back'), true);
}

/* ================= backups ================= */
const BK_POLICY = { enforce: true, minOn: true, minLen: 10, upper: false, number: false, symbol: false };
async function downloadBackup(btn, password) {
  if (btn) btn.disabled = true;
  prog.start(t('pr_export'), 2); prog.phase(t(password ? 'pr_prepare_enc' : 'pr_prepare'));
  try {
    let downloading = false;
    const { blob, name } = await apiDownload('backup/export', { password }, (loaded, total) => {
      if (!downloading) { downloading = true; prog.phase(t('pr_download')); }
      prog.bytes(loaded, total);
    });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 10000);
    prog.finish(t('bk_exported'));
    reload().catch(() => {});
  } catch (err) { prog.hide(); if (!(err instanceof ApiFail)) throw err; if (err.status !== 401) toast(t(err.code)); }
  finally { if (btn) btn.disabled = false; }
}
/* opens a backup on the server without changing anything; shows its own progress */
async function inspectBackup(f, password) {
  prog.start(t('pr_check'), 2); prog.phase(t('pr_upload'));
  try {
    const d = await apiUpload('backup/inspect', backupForm(f, password), (l, n) => prog.bytes(l, n), () => prog.phase(t('pr_read')));
    prog.hide();
    return d.summary;
  } catch (err) { prog.hide(); throw err; }
}
/* uses the choices in the export form; false if the password there is not usable yet */
function exportFromForm(btn) {
  let password = '';
  if ($('#bkEncrypt').checked) {
    password = $('#bk-pw1').value;
    if (password.length < 10) { toast(t('err_bk_pw_short')); shake('#bkForm'); return false; }
    if (password !== $('#bk-pw2').value) { toast(t('err_su_mismatch')); shake('#bkForm'); return false; }
  }
  downloadBackup(btn, password);
  return true;
}
function settingsData() {
  return `<section class="panel"><div><h2>${T('bk_export_h')}</h2><p class="sub">${T('bk_export_d')}</p></div>
      <form id="bkForm" class="regionform" novalidate>
        <label class="check"><input type="checkbox" id="bkEncrypt" checked> ${T('bk_encrypt')}</label>
        <div id="bkPw" style="display:grid;gap:12px"><p class="muted" style="margin:0;font-size:13px">${T('bk_encrypt_d')}</p>
          <div class="fields"><label>${T('bk_pw')}<input type="password" id="bk-pw1" autocomplete="new-password"></label><label>${T('bk_pw2')}<input type="password" id="bk-pw2" autocomplete="new-password"></label>
          <div class="full"><div id="bkMeter"></div></div></div>
          <p class="notice" style="margin:0">${T('bk_pw_lost')}</p></div>
        <p class="notice bad" id="bkPlain" style="margin:0" hidden>${T('bk_plain_warn')}</p>
        <p class="muted" style="margin:0;font-size:13px">${T('bk_export_warn')}</p>
        <div><button class="btn primary" type="submit" id="bkExport">${T('bk_export_btn')}</button></div></form></section>
    <section class="panel"><div><h2>${T('bk_restore_h')}</h2><p class="sub">${T('bk_restore_d')}</p></div>
      <p class="notice bad" style="margin:0">${T('bk_restore_warn')}</p>
      <div><button class="btn danger" type="button" id="bkRestore">${T('bk_restore_btn')}</button><input type="file" id="bkFile" accept=".invbackup" hidden></div></section>`;
}
const backupForm = (f, password) => { const fd = new FormData(); fd.append('file', f); if (password) fd.append('password', password); return fd; };
function backupSummary(s) {
  const n = k => Number((s.counts || {})[k] ?? 0).toLocaleString(locale());
  return `<div style="display:grid;gap:12px">
    <p style="margin:0">${T('bk_confirm_b', { d: fmt(String(s.created || '').slice(0, 10)), by: s.createdBy || '—' })}</p>
    <ul class="bk-sum"><li>${T('bk_n_devices', { n: n('devices') })}</li><li>${T('bk_n_employees', { n: n('employees') })}</li><li>${T('bk_n_users', { n: n('users') })}</li><li>${T('bk_n_log', { n: n('log') })}</li></ul>
    ${s.encrypted ? `<span class="chip yes" style="justify-self:start">${T('bk_enc_yes')}</span>` : ''}
    <p class="notice bad" style="margin:0">${T('bk_restore_warn')}</p>
    <button type="button" class="btn small bk-first" id="bkFirst">${T('bk_first')}</button></div>`;
}
function bindData() {
  const form = $('#bkForm'); if (!form) return;
  const enc = $('#bkEncrypt'), meter = () => drawMeter($('#bkMeter'), $('#bk-pw1').value, BK_POLICY);
  const sync = () => { $('#bkPw').hidden = !enc.checked; $('#bkPlain').hidden = enc.checked; };
  enc.onchange = sync; $('#bk-pw1').oninput = meter; sync(); meter();
  form.onsubmit = e => { e.preventDefault(); exportFromForm($('#bkExport')); };
  const file = $('#bkFile');
  $('#bkRestore').onclick = () => file.click();
  file.onchange = async () => {
    const f = file.files[0]; file.value = ''; if (!f) return;
    if (f.size > 50 * 1024 * 1024) { toast(t('err_backup_size')); return; }
    let summary = null, password = '';
    try { summary = await inspectBackup(f); }
    catch (err) {
      if (!(err instanceof ApiFail)) throw err;
      if (err.code !== 'err_backup_password_required') { if (err.status !== 401) toast(t(err.code)); return; }
    }
    const bindFirst = () => { $('#bkFirst').onclick = () => exportFromForm($('#bkFirst')); };
    // a protected backup first asks for its password, then shows what it holds
    const locked = `<div style="display:grid;gap:12px"><p style="margin:0">${T('bk_pw_d')}</p>
      <div class="fields"><label class="full">${T('bk_pw')}<input type="password" name="bkpass" id="bk-open" autocomplete="off"></label></div></div>`;
    openDialog(t(summary ? 'bk_confirm_t' : 'bk_pw_t'), summary ? backupSummary(summary) : locked, async v => {
      if (!summary) {
        password = v.bkpass || '';
        if (!password) { toast(t('err_backup_password_required')); return false; }
        summary = await inspectBackup(f, password);
        $('#dlgTitle').textContent = t('bk_confirm_t');
        $('#dlgBody').innerHTML = backupSummary(summary); bindFirst();
        $('#dlgOk').textContent = t('bk_restore_ok'); $('#dlgOk').className = 'btn primary danger';
        return null;
      }
      $('#bkFirst').disabled = true;   // nothing else may start while the data is being replaced
      prog.start(t('pr_restore'), 2, true); prog.phase(t('pr_upload'));
      let follow = null;   // once uploaded, follow the server's own progress
      const sent = () => {
        prog.phase(t('pr_read'));
        follow = setInterval(() => api('GET', 'maintenance').then(d => { if (d.active && d.canWatch) prog.server(d); }).catch(() => {}), 700);
      };
      try { await apiUpload('backup/restore', backupForm(f, password), (l, n) => prog.bytes(l, n), sent); }
      catch (err) { prog.hide(); $('#bkFirst').disabled = false; throw err; }
      finally { clearInterval(follow); }
      prog.finish(t('bk_restored'));
      // the server has signed everyone out: show the sign-in page with the restored organisation's name and logo
      cur = null;
      const boot = await api('GET', 'bootstrap').catch(() => null);
      S = emptyState(boot ? boot.settings : S.settings); setupInfo = boot && boot.setup || null;
      location.hash = ''; applyChrome();
      return true;
    }, t(summary ? 'bk_restore_ok' : 'bk_unlock'), !!summary);
    if (summary) bindFirst();
  };
}

/* ================= about ================= */
const fmtBytes = n => { const u = ['B', 'KB', 'MB', 'GB', 'TB']; let i = 0; n = Number(n) || 0; while (n >= 1024 && i < u.length - 1) { n /= 1024; i++; } return `${n.toLocaleString(locale(), { maximumFractionDigits: i ? 1 : 0 })} ${u[i]}`; };
const num = n => Number(n || 0).toLocaleString(locale());
function settingsAbout() {
  const u = logoUrl();
  return `<section class="panel"><div class="about-head"><div class="box${u ? ' logo' : ''}">${u ? `<img src="${esc(u)}" alt="">` : APP_SVG}</div>
      <div><h2>${T('brand')}</h2><p class="sub" id="abSub">${T('ab_loading')}</p></div></div>
      <dl class="kv" id="abApp"></dl></section>
    <div class="grid2"><section class="panel"><h2>${T('ab_data')}</h2><dl class="kv" id="abData"></dl></section>
      <section class="panel"><h2>${T('ab_tech')}</h2><dl class="kv" id="abTech"></dl></section></div>`;
}
function settingsUpdates() {
  return `<section class="panel"><div><h2>${T('set_updates')}</h2><p class="sub" id="abRepo">${T('ab_loading')}</p></div>
      <dl class="kv"><dt>${T('ab_current')}</dt><dd id="abCurrent">—</dd><dt>${T('ab_access')}</dt><dd id="abAccess">—</dd></dl>
      <div class="upd" id="abUpd"></div>
      <div class="row"><button class="btn" type="button" id="abCheck" disabled>${T('ab_check')}</button></div></section>
    <div id="upMore"></div>`;
}
const UP_HOURS = Array.from({ length: 24 }, (_, h) => [String(h), `${String(h).padStart(2, '0')}:00`]);
function updaterResult(u) {   // the updater's last check, in the shape drawUpdate understands
  return u.status ? { status: u.status, latest: u.latest, name: u.name, notes: u.notes, url: u.url, published: u.published, checked: u.checkedAt } : null;
}
function updatesExtra(st) {
  const jobs = st.jobs.length ? `<div class="tablebox"><table><thead><tr><th>${T('up_th_date')}</th><th>${T('up_th_version')}</th><th>${T('up_th_how')}</th><th>${T('up_th_result')}</th></tr></thead><tbody>
      ${st.jobs.map(j => `<tr><td>${fmt(j.createdAt.slice(0, 10))}<span class="t2">${esc(j.createdAt.slice(11, 16))}</span></td>
        <td>${j.from ? esc('v' + j.from.replace(/^v/, '')) : '—'} → <b>${esc(j.target)}</b></td>
        <td>${j.automatic ? T('up_how_auto') : T('up_how_manual', { name: j.by || '—' })}</td>
        <td><span class="pill st-${j.status === 'done' ? 'on' : j.status === 'rolled_back' || j.status === 'failed' ? 'perdido' : 'tech'}">${T('up_st_' + j.status)}</span>${j.message ? `<span class="t2">${esc(j.message)}</span>` : ''}</td></tr>`).join('')}
    </tbody></table></div>` : `<p class="muted" style="margin:0">${T('up_no_history')}</p>`;
  return `<section class="panel"><div><h2>${T('up_auto_h')}</h2><p class="sub">${T('up_auto_d')}</p></div>
      <form id="upAuto" class="regionform" novalidate>
        <label class="check"><input type="checkbox" id="upAutoOn"${st.auto.enabled ? ' checked' : ''}> ${T('up_auto_on')}</label>
        <label>${T('up_auto_hour')}<select id="upAutoHour">${opts(UP_HOURS, String(st.auto.hour))}</select></label>
        <div><button class="btn primary" type="submit">${T('save')}</button></div></form></section>
    <section class="panel"><h2>${T('up_history')}</h2>${jobs}</section>
    <section class="panel"><h2>${T('ab_how_h')}</h2><ol class="ab-steps"><li>${T('up_steps_1')}</li><li>${T('up_steps_2')}</li><li>${T('up_steps_3')}</li></ol></section>`;
}
async function bindUpdates() {
  if (!$('#abUpd')) return;
  let st;
  try { st = await api('GET', 'updates'); } catch (err) { if (err.status !== 401) toast(t(err.code)); return; }
  if (!$('#abUpd')) return;   // the person moved on meanwhile
  $('#abCurrent').textContent = `${st.installed}${st.commit ? ` · ${st.commit.slice(0, 7)}` : ''}`;
  if (!st.updater) return bindUpdatesWithoutUpdater();
  $('#abRepo').textContent = t('up_with_updater');
  $('#abAccess').closest('dl').querySelectorAll('dt, dd').forEach((el, i) => { if (i > 1) el.remove(); });
  const r = updaterResult(st.updater);
  drawUpdate(r, r && r.status === 'update' ? r.latest : null);
  $('#upMore').innerHTML = updatesExtra(st);
  const check = $('#abCheck'); check.disabled = false;
  check.onclick = async () => {
    check.disabled = true; check.textContent = t('ab_checking');
    const before = st.updater.checkedAt;
    try {
      await api('POST', 'updates/check', {});
      for (let i = 0; i < 20; i++) {   // the updater answers within a few seconds
        await new Promise(res => setTimeout(res, 1500));
        const now = await api('GET', 'updates');
        if (now.updater && now.updater.checkedAt !== before) { if ($('#abUpd')) { route(); } return; }
      }
      toast(t('err_no_updater'));
    } catch (err) { if (err.status !== 401) toast(t(err.code)); }
    finally { if ($('#abCheck')) { check.disabled = false; check.textContent = t('ab_check'); } }
  };
  const install = $('#upInstall'); if (install) install.onclick = () => confirmInstall(install.dataset.tag);
  $('#upAuto').onsubmit = async e => {
    e.preventDefault();
    try { await api('PUT', 'updates/auto', { enabled: $('#upAutoOn').checked, hour: Number($('#upAutoHour').value) }); toast(t('saved'), true); }
    catch (err) { if (err.status !== 401) toast(t(err.code)); }
  };
}
async function bindUpdatesWithoutUpdater() {   // no updater on this server: the app can only check, not install
  let a;
  try { a = await api('GET', 'about'); } catch (err) { if (err.status !== 401) toast(t(err.code)); return; }
  if (!$('#abUpd')) return;
  $('#abRepo').textContent = a.updates.repo ? t('ab_repo', { repo: a.updates.repo }) : t('ab_st_off');
  $('#abAccess').textContent = t('ab_access_' + (a.updates.access || 'none'));
  drawUpdate(a.updates.last);
  $('#upMore').innerHTML = `<p class="notice info" style="margin:0">${T('up_no_updater')}</p>
    <section class="panel"><h2>${T('ab_how_h')}</h2><ol class="ab-steps"><li>${T('ab_how_1')}</li><li>${T('ab_how_2')}</li><li>${T('ab_how_3')}</li></ol></section>`;
  const b = $('#abCheck'); b.disabled = !a.updates.repo;
  b.onclick = async () => {
    b.disabled = true; b.textContent = t('ab_checking');
    try { drawUpdate(await api('POST', 'about/updates', {})); }
    catch (err) { if (err.status !== 401) toast(t(err.code)); }
    finally { if ($('#abCheck')) { b.disabled = false; b.textContent = t('ab_check'); } }
  };
}
function confirmInstall(tag) {
  openDialog(t('up_confirm_t', { v: tag }), `<ul class="bk-sum" style="gap:6px"><li>${T('up_confirm_b1')}</li><li>${T('up_confirm_b2')}</li><li>${T('up_confirm_b3')}</li></ul>`, async () => {
    const { job } = await api('POST', 'updates/install', { tag });
    setTimeout(() => followUpdate(job.id, tag), 250);
    return true;
  }, t('up_confirm_ok'));
}
/* the person who asked for the update follows it until it is installed, rolled back or refused */
function followUpdate(jobId, tag) {
  prog.start(t('up_title', { v: tag }), 5, true); prog.phase(t('up_queued'));
  window.onbeforeunload = null;   // leaving is harmless: the installation carries on on the server
  $('#progNote').hidden = false; $('#progNote').textContent = t('up_note');
  const timer = setInterval(async () => {
    let m;
    try { m = await api('GET', 'maintenance'); } catch (e) { return; }   // the app is restarting: keep waiting
    if (m.active) { prog.server(m); return; }
    let st;
    try { st = await api('GET', 'updates'); } catch (e) { return; }
    const job = st.jobs.find(j => j.id === jobId);
    if (!job || job.status === 'queued' || job.status === 'running') return;
    clearInterval(timer);
    if (job.status === 'done') {
      prog.finish(t('up_done', { v: tag }));
      try { sessionStorage.setItem('inv-updated', tag); } catch (e) {}
      setTimeout(() => location.reload(), 2200);
      return;
    }
    prog.hide(); route();
    toast(t(job.status === 'rolled_back' ? 'up_result_rolled_back' : 'up_result_failed', { msg: job.message || '' }));
  }, 2000);
}
const kv = rows => rows.map(([k, v]) => `<dt>${T(k)}</dt><dd>${v}</dd>`).join('');
function drawUpdate(r, installTag) {
  const box = $('#abUpd'); if (!box) return;
  if (!r) { box.innerHTML = `<p class="muted" style="margin:0">${T('ab_never')}</p>`; return; }
  const when = r.checked ? `<p class="muted" style="margin:0;font-size:13px">${T('ab_checked', { d: fmt(r.checked.slice(0, 10)) })}</p>` : '';
  if (r.status === 'current') { box.innerHTML = `<p class="notice" style="margin:0;background:var(--ok-bg);color:var(--ok)">${T('ab_st_current', { v: r.latest })}</p>${when}`; return; }
  if (r.status === 'update') {
    box.innerHTML = `<p class="notice info" style="margin:0"><b>${T('ab_st_update', { v: r.latest })}</b>${r.published ? ` · ${T('ab_published', { d: fmt(r.published.slice(0, 10)) })}` : ''}</p>
      ${r.notes ? `<pre class="upd-notes">${esc(r.notes)}</pre>` : ''}
      ${installTag ? '' : `<p class="muted" style="margin:0;font-size:13px">${T('ab_install')}</p>`}
      <div class="row">${installTag ? `<button class="btn primary" type="button" id="upInstall" data-tag="${esc(installTag)}">${T('up_install', { v: installTag })}</button>` : ''}
        ${r.url ? `<a class="btn small" href="${esc(r.url)}" target="_blank" rel="noopener noreferrer">${T('ab_open')}</a>` : ''}</div>${when}`;
    return;
  }
  const bad = ['private', 'auth', 'error', 'app_missing', 'app_key'].includes(r.status);
  box.innerHTML = `<p class="notice${bad ? '' : ' info'}" style="margin:0">${T('ab_st_' + r.status)}</p>${when}`;
}
async function bindAbout() {
  const sub = $('#abSub'); if (!sub) return;
  let a;
  try { a = await api('GET', 'about'); } catch (err) { if (err.status !== 401) toast(t(err.code)); return; }
  if (!$('#abSub')) return;   // the person moved on meanwhile
  sub.textContent = `${t('ab_version')} ${a.version}${a.commit ? ` · ${a.commit.slice(0, 7)}` : ''}`;
  $('#abApp').innerHTML = kv([
    ['ab_version', esc(a.version)], ['ab_build', a.commit ? `<span class="mono">${esc(a.commit)}</span>` : T('ab_unknown')],
    ['ab_env', T('ab_env_' + a.environment)], ['f_org', esc(S.settings.orgName)],
    ['ab_since', a.since ? fmt(a.since) : '—'], ['ab_tz', esc(a.timeZone)]]);
  $('#abData').innerHTML = kv([['nav_devices', num(a.counts.devices)], ['nav_people', num(a.counts.employees)], ['set_users', num(a.counts.users)],
    ['bk_log_label', num(a.counts.log)], ['ab_dbsize', fmtBytes(a.dbSize)]]);
  $('#abTech').innerHTML = kv([['ab_python', esc(a.tech.python)], ['ab_django', esc(a.tech.django)], ['ab_postgres', esc(a.tech.postgres)]]);
}

/* ================= company logo ================= */
const APP_SVG = '<svg class="i" viewBox="0 0 24 24"><rect x="4" y="5" width="16" height="11" rx="2"/><path d="M2 19h20"/></svg>';
const logoUrl = () => S.settings.logo ? '/api/logo?v=' + S.settings.logo : '';
const appIcon = () => { const u = logoUrl(); return `<div class="appicon${u ? ' logo' : ''}" aria-hidden="true">${u ? `<img src="${esc(u)}" alt="">` : APP_SVG}</div>`; };
function applyBrand() {
  const u = logoUrl(), mark = $('#brandLink .mark');
  if (mark.dataset.logo !== u) { mark.dataset.logo = u; mark.classList.toggle('logo', !!u); mark.innerHTML = u ? `<img src="${esc(u)}" alt="">` : '<i></i>'; }
  $('#brandLink').title = t('go_home');
  // browser tab: the logo itself; home-screen icon: made from the logo by the server, or the app's own
  const fav = $('#favIcon'), lv = S.settings.logo || 0;
  if (u) { fav.href = u; fav.removeAttribute('type'); fav.removeAttribute('sizes'); }
  else { fav.href = `/app-icon/any-32.png?v=${lv}`; fav.type = 'image/png'; fav.setAttribute('sizes', '32x32'); }
  $('#touchIcon').href = `/app-icon/apple-180.png?v=${lv}`;
}
$('#brandLink').addEventListener('click', () => { if ((location.hash || '#panel') === '#panel') window.scrollTo({ top: 0, behavior: motionOK() ? 'smooth' : 'auto' }); });
/* ================= installable app ================= */
/* Chrome, Edge and Android offer their own install prompt; iPhone, iPad and Safari on the Mac do it from a menu. */
let installPrompt = null;
const runningInstalled = () => matchMedia('(display-mode: standalone)').matches || navigator.standalone === true;
const appleMobile = () => /iphone|ipad|ipod/i.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
const macSafari = () => /Macintosh/.test(navigator.userAgent) && /Safari\//.test(navigator.userAgent) && !/Chrome|Chromium|Edg\/|Firefox|OPR\//.test(navigator.userAgent);
function updateInstallItem() {
  const b = $('#installBtn'); if (!b) return;
  b.hidden = runningInstalled() || !window.isSecureContext || !(installPrompt || appleMobile() || macSafari());
}
window.addEventListener('beforeinstallprompt', e => { e.preventDefault(); installPrompt = e; updateInstallItem(); });
window.addEventListener('appinstalled', () => { installPrompt = null; updateInstallItem(); toast(t('install_done'), true); });
$('#installBtn').addEventListener('click', async () => {
  closeMenus();
  if (installPrompt) { const p = installPrompt; installPrompt = null; p.prompt(); try { await p.userChoice; } catch (e) {} updateInstallItem(); return; }
  const mobile = appleMobile(), steps = mobile ? ['install_ios_1', 'install_ios_2', 'install_ios_3'] : ['install_mac_1', 'install_mac_2'];
  openDialog(t(mobile ? 'install_ios_t' : 'install_mac_t'), `<ol class="ab-steps" style="color:var(--ink);font-size:14.5px;gap:10px">${steps.map(k => `<li>${T(k)}</li>`).join('')}</ol>`, null);
});
if ('serviceWorker' in navigator && window.isSecureContext) navigator.serviceWorker.register('/sw.js').catch(() => {});

function settingsBrand() {
  const u = logoUrl();
  return `<section class="panel"><div><h2>${T('set_brand')}</h2><p class="sub">${T('set_brand_sub')}</p></div>
    <div class="logoprev"><div class="box${u ? ' logo' : ''}">${u ? `<img src="${esc(u)}" alt="">` : APP_SVG}</div><div class="txt"><b>${esc(S.settings.orgName)}</b><small>${T('brand_where')}</small></div></div>
    <div class="row"><button class="btn primary" type="button" id="logoPick">${T(u ? 'brand_change' : 'brand_upload')}</button>
      <input type="file" id="logoFile" accept="image/png,image/jpeg,image/webp,image/gif,image/svg+xml" hidden>
      ${u ? `<button class="btn danger" type="button" id="logoRemove">${T('brand_remove')}</button>` : ''}</div>
    <p class="muted" style="margin:0;font-size:13px">${T('brand_formats')}</p></section>`;
}
function bindBrand() {
  const pick = $('#logoPick'); if (!pick) return;
  const file = $('#logoFile');
  const done = async (method, body, msg) => {
    try { await mutate(method, 'settings/logo', body); } catch (err) { if (err.status !== 401) { toast(t(err.code)); shake('.logoprev'); } return; }
    applyChrome(); route(); toast(t(msg), true);
  };
  pick.onclick = () => file.click();
  file.onchange = () => {
    const f = file.files[0]; file.value = ''; if (!f) return;
    if (!/^image\/(png|jpeg|webp|gif|svg\+xml)$/.test(f.type)) { toast(t('err_logo_type')); shake('.logoprev'); return; }
    if (f.size > 512 * 1024) { toast(t('err_logo_size')); shake('.logoprev'); return; }
    const r = new FileReader();
    r.onload = () => done('PUT', { data: r.result }, 'brand_saved');
    r.readAsDataURL(f);
  };
  const rm = $('#logoRemove'); if (rm) rm.onclick = () => done('DELETE', undefined, 'brand_removed');
}

/* ================= tooltips ================= */
function showTip(target) {
  const tip = $('#tip'); tip.textContent = target.dataset.tip; tip.hidden = false;
  const r = target.getBoundingClientRect(), w = tip.offsetWidth, h = tip.offsetHeight;
  tip.style.left = Math.max(8, Math.min(r.left + r.width / 2 - w / 2, innerWidth - w - 8)) + 'px';
  tip.style.top = (r.top - h - 8 < 8 ? r.bottom + 8 : r.top - h - 8) + 'px';
  target.setAttribute('aria-describedby', 'tip');
}
const hideTip = () => { $('#tip').hidden = true; };
document.addEventListener('pointerover', e => { const x = e.target.closest('[data-tip]'); if (x && e.pointerType !== 'touch') showTip(x); });
document.addEventListener('pointerout', e => { const x = e.target.closest('[data-tip]'); if (x && !x.contains(e.relatedTarget)) hideTip(); });
document.addEventListener('focusin', e => { const x = e.target.closest('[data-tip]'); if (x) showTip(x); });
document.addEventListener('focusout', hideTip);
document.addEventListener('click', e => { const x = e.target.closest('[data-tip]'); if (x) showTip(x); else hideTip(); });   // touch screens: tap to read
document.addEventListener('scroll', hideTip, true);
document.addEventListener('keydown', e => { if (e.key === 'Escape') hideTip(); });

/* ================= required password change ================= */
function renderPwChange() {
  view.innerHTML = `<div class="login"><div class="card">
    <div class="loginhead">${appIcon()}<h1>${T('pc_title')}</h1><p class="sub">${T('pc_sub')}</p></div>
    <form id="pcForm" novalidate>
      <label>${T('pc_current')}<input type="password" id="pc-cur" autocomplete="current-password"></label>
      <label>${T('pc_new')}<input type="password" id="pc-new" autocomplete="new-password"></label>
      <label>${T('pc_repeat')}<input type="password" id="pc-new2" autocomplete="new-password"></label>
      <div id="pcMeter"></div>
      <button class="btn primary" type="submit" id="pcOk">${T('pc_btn')}</button>
    </form>
    <button class="btn" type="button" id="pcLogout">${T('logout')}</button>
  </div></div>`;
  const policy = cur.pwPolicy || PW_DEFAULT, meter = () => drawMeter($('#pcMeter'), $('#pc-new').value, policy);
  $('#pc-new').oninput = meter; meter();
  $('#pcLogout').onclick = () => $('#logoutBtn').onclick();
  $('#pcForm').addEventListener('submit', async e => {
    e.preventDefault();
    const now = $('#pc-cur').value, next = $('#pc-new').value;
    const fail = key => { toast(t(key)); shake('.login .card'); };
    if (!now) return fail('err_pw_current');
    if (!next) return fail('err_pass');
    if (next !== $('#pc-new2').value) return fail('err_su_mismatch');
    if (next === now) return fail('err_pw_same');
    if (!pwMeets(next, policy)) return fail('err_pass_weak');
    $('#pcOk').disabled = true;
    try { adopt(await api('POST', 'account/password', { current: now, new: next })); }
    catch (err) { if (!(err instanceof ApiFail)) throw err; $('#pcOk').disabled = false; if (err.status !== 401) fail(err.code); return; }
    location.hash = 'panel'; applyChrome(); route(); enter(); toast(t('pc_done'), true);
  });
  $('#pc-cur').focus();
}

function renderLogin(err, email) { view.innerHTML = viewLogin(err); bindLogin(); const em = $('#login-email'); if (email) { em.value = email; $('#login-pass').focus(); } else em.focus(); }

function viewPanel() {
  const activos = S.devices.filter(d => !isRetired(d));
  const c = k => S.devices.filter(d => d.estado === k).length;
  const alerts = [], wd = S.settings.warrantyDays;
  S.assignments.filter(a => !a.hasta).forEach(a => {
    const e = emp(a.employeeId), d = dev(a.deviceId);
    if (e && hasLeft(e) && d) alerts.push({ k: 'bad', d, t: t('al_recover', { tag: d.tag }), s: t('al_recover_s', { name: e.nombre, date: fmt(e.estadoFecha) }) });
  });
  S.incidents.filter(i => i.estado === 'abierta').forEach(i => { const d = dev(i.deviceId); if (d) alerts.push({ k: 'warn', d, t: t('al_inc', { tag: d.tag }), s: t('al_inc_s', { desc: tx(i.descripcion), date: fmt(i.fecha) }) }); });
  activos.filter(d => d.garantia && daysUntil(d.garantia) >= 0 && daysUntil(d.garantia) <= wd).sort((a, b) => a.garantia.localeCompare(b.garantia))
    .forEach(d => alerts.push({ k: 'warn', d, t: t('al_war', { tag: d.tag, n: daysUntil(d.garantia) }), s: `${devTitle(d)} · ${fmt(d.garantia)}` }));
  activos.filter(d => d.enc === 'no').forEach(d => alerts.push({ k: 'bad', d, t: t('al_enc', { tag: d.tag }), s: t('al_enc_s') }));
  // restoring a backup made by 1.10.0 to 1.15.0 dropped every employee's departments and offices
  if (S.employees.length > 1 && (S.depts.length || S.locations.length) && S.employees.every(e => !(e.depts || []).length && !(e.locs || []).length))
    alerts.push({ k: 'bad', href: '#empleados', t: t('al_places_lost'), s: t('al_places_lost_s') });
  S.devices.filter(d => d.estado === 'averiado').forEach(d => alerts.push({ k: 'bad', d, t: t('al_faulty', { tag: d.tag }), s: t('al_faulty_s') }));
  activos.forEach(d => (d.disks || []).forEach(k => {
    if (k.health === 'failing') alerts.push({ k: 'bad', d, t: t('al_disk_fail', { tag: d.tag }), s: t('al_disk_fail_s', { x: driveLabel(k) }) });
    else if (k.health === 'warning') alerts.push({ k: 'warn', d, t: t('al_disk_warn', { tag: d.tag }), s: t('al_disk_warn_s', { x: driveLabel(k) }) });
    else if (k.wear !== null && k.wear !== undefined && k.wear >= 80) alerts.push({ k: 'warn', d, t: t('al_disk_wear', { tag: d.tag, n: nf(k.wear) }), s: t('al_disk_wear_s', { x: driveLabel(k) }) });
  }));
  S.devices.forEach(d => { const cs = dataChecks(d); if (cs.length) alerts.push({ k: 'warn', d, t: t('al_check', { tag: d.tag, n: cs.length }), s: t('chk_' + cs[0].k, cs[0].args) }); });
  activos.filter(d => hasBattery(devType(d)) && has(d.batHealth) && d.batHealth < 80).forEach(d => alerts.push({ k: 'warn', d, t: t('al_bat', { tag: d.tag, p: nf(d.batHealth) }), s: t('al_bat_s') }));

  const byDept = S.depts.map(x => [tx(x.nombre), S.assignments.filter(a => !a.hasta && (a.deptId === x.id || (emp(a.employeeId)?.depts || []).includes(x.id))).length]).sort((a, b) => b[1] - a[1]);
  const max = Math.max(1, ...byDept.map(x => x[1]));
  const valor = activos.reduce((s, d) => s + (Number(d.precio) || 0), 0);
  const col = { uso: 'var(--info)', disponible: 'var(--ok)', reparacion: 'var(--warn)', averiado: 'var(--bad)' };
  const uname = id => byId('users', id)?.nombre;

  return `
  <div class="head"><div><h1>${T('summary_title')}</h1><p class="sub">${T('summary_sub', { n: activos.length, v: money(valor) })}</p></div>${reloadBtn()}</div>
  <div class="stats">
    ${['uso', 'disponible', 'reparacion', 'averiado'].map(k => `<a class="stat" href="#dispositivos" data-filter="${k}"><b>${c(k)}</b><span><i class="dot" style="background:${col[k]}"></i>${esc(st(k))}</span></a>`).join('')}
    <a class="stat" href="#dispositivos" data-filter="retirados"><b>${c('descartado') + c('perdido')}</b><span><i class="dot" style="background:var(--mute)"></i>${T('retired_stat')}</span></a>
  </div>
  <div class="grid2">
    <section class="panel"><h2>${T('attention')} <span class="muted" style="font-weight:500">· ${alerts.length}</span></h2>
      <div class="alerts">${alerts.length ? alerts.map(a => `<a class="alert" href="${a.d ? '#dispositivo-' + a.d.id : a.href}"><span class="bar" style="background:var(--${a.k})"></span><span class="txt"><b>${esc(a.t)}</b><small>${esc(a.s)}</small></span>${a.d ? `<span class="tag">${esc(a.d.tag)}</span>` : ''}</a>`).join('') : `<p class="muted">${T('nothing')}</p>`}</div>
    </section>
    <div class="stack">
      <section class="panel"><h2>${T('by_dept')}</h2>
        <div class="bars">${byDept.map(([n2, n]) => `<div class="barrow"><span>${esc(n2)}</span><span class="track"><span class="fill" style="width:${n / max * 100}%"></span></span><b>${n}</b></div>`).join('')}</div>
      </section>
      <section class="panel"><h2>${T('activity')}</h2>
        <ul class="feed">${S.log.slice(0, 7).map(l => `<li><time>${fmt(l.fecha)}</time><span>${esc(logText(l))}${uname(l.by) ? ` <span class="by">· ${esc(uname(l.by))}</span>` : ''}</span></li>`).join('')}</ul>
      </section>
    </div>
  </div>`;
}

const F = { q: '', estado: 'activos', dept: '', tipo: '', campo: '' };
/* what the device search looks in: everything, or one detail (so "16" in Memory finds 16 GB, not a serial number) */
const SEARCH_IN = {
  tag: d => d.tag,
  name: d => hostOf(d),
  serial: d => d.serial,
  model: d => [devTitle(d), typeName(devType(d))].join(' '),
  cpu: d => { const c = cpuOf(d); return c ? [c.nombre, cpuGen(c.nombre), withUnit(c.speed, c.speedUnit)].join(' ') : ''; },
  ram: d => [withUnit(d.ramSize, d.ramUnit), ramDetail(d), listName('ramForms', d.ramForm)].join(' '),
  disk: d => [...(d.disks || []).map(k => [withUnit(k.size, k.unit), listName('diskTypes', k.type), listName('diskForms', k.form), listName('diskConns', k.conn)].join(' ')), specParts(d).slice(-1)[0] || ''].join(' '),
  gpu: d => gpuOf(d)?.nombre || '',
  os: d => osText(d),
  mac: d => (d.nics || []).map(n => n.mac + ' ' + listName('nicModels', n.modelId)).join(' '),
  person: d => { const a = openAsg(d.id), e = a && emp(a.employeeId); return a ? [holderName(a), e ? deptNames(e) : ''].join(' ') : ''; },
};
/* a match ignoring case, and also ignoring spaces ("16gb" finds "16 GB") */
const found = (text, q) => { const h = String(text || '').toLowerCase(); return h.includes(q) || h.replace(/\s+/g, '').includes(q.replace(/\s+/g, '')); };
function viewDevices() {
  return `
  <div class="head"><div><h1>${T('devices_title')}</h1><p class="sub">${T('devices_sub')}</p></div>
    <div class="row">${reloadBtn()}${can('edit') ? `<button class="btn primary" type="button" data-act="nuevoDispositivo">${T('new_device')}</button>` : ''}</div></div>
  <div class="toolbar">
    <input type="search" id="fq" placeholder="${F.campo ? T('search_in', { x: t('sf_' + F.campo) }) : T('search_dev')}" value="${esc(F.q)}" aria-label="${T('lbl_search')}">
    <select id="fcampo" aria-label="${T('lbl_search_in')}">${opts([['', t('sf_all')], ...Object.keys(SEARCH_IN).map(k => [k, t('sf_' + k)])], F.campo)}</select>
    <select id="festado" aria-label="${T('lbl_status')}">${opts([['activos', t('f_active')], ['', t('f_all')], ...ST.map(k => [k, st(k)]), ['retirados', t('retired_stat')], ['revisar', t('f_review')]], F.estado)}</select>
    <select id="fdept" aria-label="${T('lbl_dept')}">${opts([['', t('f_alldepts')], ...S.depts.map(x => [x.id, tx(x.nombre)])], F.dept)}</select>
    <select id="ftipo" aria-label="${T('lbl_type')}">${opts([['', t('f_alltypes')], ...S.types.map(x => [x.id, tx(x.nombre)])], F.tipo)}</select>
  </div>
  <div class="tablebox" id="devTable"></div>`;
}
function drawDeviceRows() {
  const q = F.q.trim().toLowerCase();
  const rows = S.devices.filter(d => {
    const a = openAsg(d.id), e = a && emp(a.employeeId), m = model(d.modelId);
    if (F.estado === 'activos' && isRetired(d)) return false;
    if (F.estado === 'retirados' && !isRetired(d)) return false;
    if (ST.includes(F.estado) && d.estado !== F.estado) return false;
    if (F.estado === 'revisar' && !dataChecks(d).length) return false;
    if (F.dept && a?.deptId !== F.dept && !(e?.depts || []).includes(F.dept)) return false;
    if (F.tipo && devType(d) !== F.tipo) return false;
    if (q && !(F.campo ? found(SEARCH_IN[F.campo](d), q) : found([d.tag, hostOf(d), d.serial, osText(d), cpuOf(d)?.nombre, ...(d.nics || []).map(n => n.mac + ' ' + listName('nicModels', n.modelId)), gpuOf(d)?.nombre, devTitle(d), e?.nombre, a?.deptId ? deptName(a.deptId) : '', specLine(d)].join(' '), q))) return false;
    return true;
  });
  $('#devTable').innerHTML = rows.length ? `<table><thead><tr><th>${T('th_tag')}</th><th>${T('th_device')}</th><th>${T('th_assigned')}</th><th>${T('th_status')}</th><th>${T('th_warranty')}</th></tr></thead><tbody>
    ${rows.map(d => { const a = openAsg(d.id), e = a && emp(a.employeeId), m = model(d.modelId);
      return `<tr class="click" data-go="dispositivo-${d.id}"><td>${tagLink(d)}</td>
        <td><b>${esc(devTitle(d))}</b>${specLine(d) ? `<span class="t2 spec">${specHtml(d)}</span>` : ''}<span class="t2">${[esc(typeName(devType(d))), hostExtra(d), `<span class="mono">${esc(d.serial)}</span>`].filter(Boolean).join(' · ')}</span></td>
        <td>${e ? `${esc(e.nombre)}<span class="t2">${esc(deptNames(e))}${hasLeft(e) ? ` · <span class="w-past">${T('left_badge')}</span>` : ''}</span>` : a?.deptId ? `${esc(deptName(a.deptId))}<span class="t2">${T('shared_dept')}</span>` : '<span class="muted">—</span>'}</td>
        <td>${pill(d.estado)}</td><td>${warranty(d)}</td></tr>`; }).join('')}
  </tbody></table>` : `<div class="empty">${T('no_match_dev')}</div>`;
}

function viewDevice(id) {
  const d = dev(id);
  if (!d) return `<p>${T('not_found_dev')} <a href="#dispositivos">${T('back_list')}</a></p>`;
  const m = model(d.modelId), a = openAsg(d.id), e = a && emp(a.employeeId), c = cpuOf(d), scr = hasScreen(devType(d)), batt = hasBattery(devType(d));
  const hist = S.assignments.filter(x => x.deviceId === d.id).sort((x, y) => y.desde.localeCompare(x.desde));
  const incs = S.incidents.filter(x => x.deviceId === d.id).sort((x, y) => y.fecha.localeCompare(x.fecha));
  const gasto = incs.reduce((s, i) => s + (Number(i.coste) || 0), 0);
  const retired = isRetired(d), ed = can('edit');
  const dash = '<span class="muted">—</span>';
  const chip = (txt, cls = '') => txt ? `<span class="chip ${cls}">${esc(txt)}</span>` : '';
  const sub = txt => txt ? `<span class="muted" style="display:block;font-size:12.5px">${esc(txt)}</span>` : '';
  const modules = d.ramRep === 'yes' && has(d.ramModules) && has(d.ramModSize) ? `${d.ramModules} × ${withUnit(d.ramModSize, d.ramModUnit)}` : '';
  const gp = gpuOf(d);
  const bat = has(d.batHealth) ? Number(d.batHealth) : null;
  const nics = d.nics || [];
  return `
  <div class="backrow"><a class="back" href="#dispositivos">${T('back_devices')}</a>${reloadBtn()}</div>
  <div class="devhead">
    <div class="id">
      <div class="row"><span class="tag" style="font-size:14px;padding:3px 8px">${esc(d.tag)}</span>${pill(d.estado)}</div>
      <h1>${esc(devTitle(d))}</h1>
      <p class="sub">${[esc(typeName(devType(d))), hostExtra(d), `${T('serial_no')} <span class="mono">${esc(d.serial)}</span>`].filter(Boolean).join(' · ')}</p>
    </div>
    ${ed ? `<div class="row">
      ${retired ? '' : (a ? `<button class="btn primary" type="button" data-act="devolver" data-id="${d.id}">${T('btn_return')}</button>` : d.estado === 'averiado' ? '' : assignMenu(d))}
      ${retired ? '' : `<button class="btn" type="button" data-act="incidencia" data-id="${d.id}">${T('btn_fault')}</button>`}
      <button class="btn" type="button" data-act="estado" data-id="${d.id}">${T('btn_status')}</button>
      <button class="btn" type="button" data-act="editar" data-id="${d.id}">${T('btn_edit')}</button>
    </div>` : ''}
  </div>
  ${e && hasLeft(e) ? `<div class="notice bad">${T('n_left', { name: e.nombre, date: fmt(e.estadoFecha) })}</div>` : ''}
  ${e && empState(e) === 'baja' ? `<div class="notice">${T('n_onleave', { name: e.nombre, d: fmt(e.estadoFecha) })}</div>` : ''}
  ${d.estado === 'descartado' && d.destino ? `<div class="notice info">${T('k_dest')}: ${esc(dsp(d.destino))} · ${T('fc_cert')}: ${d.wipeCert ? `<span class="mono">${esc(d.wipeCert)}</span>` : T('no_cert')}</div>` : ''}
  ${d.enc === 'no' && !retired ? `<div class="notice bad">${T('n_noenc')}</div>` : ''}
  ${checksBox(d)}
  <div class="grid3">
    <section class="panel"><h2>${T('current')}</h2>
      ${e ? `<div class="current"><b><a href="#empleado-${e.id}">${esc(e.nombre)}</a></b><span class="muted">${esc(deptNames(e))} · ${esc(locNames(e))}</span><span>${T('since', { d: fmt(a.desde), age: age(a.desde) })}</span>${tx(a.notas) ? `<span class="muted">${T('delivered_with', { x: tx(a.notas) })}</span>` : ''}</div>`
        : a?.deptId ? `<div class="current"><b>${esc(deptName(a.deptId))}</b><span class="muted">${T('shared_dept')} · ${esc(locName(d.loc))}</span><span>${T('since', { d: fmt(a.desde), age: age(a.desde) })}</span>${tx(a.notas) ? `<span class="muted">${T('delivered_with', { x: tx(a.notas) })}</span>` : ''}</div>`
        : `<p class="muted">${retired ? T('out_service') : T('unassigned_at', { loc: locName(d.loc) })}</p>`}
    </section>
    <section class="panel"><h2>${T('hw')}</h2>
      <dl class="kv">
        <dt>${T('k_cpu')}</dt><dd>${c ? esc(c.nombre) : '—'}${sub(cpuDetail(c))}${chips([repChip(d.cpuRep)])}</dd>
        <dt>${T('k_ram')}</dt><dd>${esc(withUnit(d.ramSize, d.ramUnit)) || '—'}${sub(ramDetail(d))}${chips([chip(modules), chip(listName('ramForms', d.ramForm)), repChip(d.ramRep)])}</dd>
        ${(d.disks || []).length ? d.disks.map((k, i) => `<dt>${d.disks.length > 1 ? T('disk_n', { n: i + 1 }) : T('k_disk')}</dt><dd>${esc(withUnit(k.size, k.unit)) || '—'}${chips([chip(listName('diskTypes', k.type)), chip(listName('diskForms', k.form)), chip(listName('diskConns', k.conn)), repChip(k.rep)])}${diskHealth(d, k)}</dd>`).join('') : `<dt>${T('k_disk')}</dt><dd>—</dd>`}
        <dt>${T('k_gpu')}</dt><dd>${gp ? esc(gp.nombre) : '—'}${chips([gp?.kind ? chip(t('gpu_' + gp.kind)) : '', gp && withUnit(gp.vram, gp.vramUnit) ? chip('VRAM ' + withUnit(gp.vram, gp.vramUnit)) : ''])}</dd>
        <dt>${T('k_os')}</dt><dd>${esc(osText(d)) || '—'}${chips([d.oclp === 'yes' ? chip(d.oclpVersion ? t('chip_oclp_v', { v: d.oclpVersion }) : t('chip_oclp')) : '', d.hackintosh === 'yes' ? chip('Hackintosh') : ''])}</dd>
        <dt>${esc(encLabel(d.osFamily))}</dt><dd>${d.enc === 'yes' ? T('yes') : d.enc === 'no' ? `<span class="w-past">${T('no')}</span>` : '—'}</dd>
        <dt>${T('k_ad')}</dt><dd>${d.ad === 'yes' ? T('yes') : d.ad === 'no' ? T('no') : '—'}</dd>
        <dt>${T('k_loc')}</dt><dd>${esc(locName(d.loc))}</dd></dl>
    </section>
    ${scr || batt ? `<section class="panel"><h2>${esc(screenTitle(devType(d)))}</h2>
      <dl class="kv">
        ${scr ? `<dt>${T('k_screen')}</dt><dd>${has(d.screen) ? esc(nf(d.screen) + '"') : '—'}${chips([d.touch === 'yes' ? chip(t('touch_s')) : d.touch === 'no' ? chip(t('notouch_s'), 'no') : ''])}</dd>` : ''}
        ${batt ? `<dt>${T('k_battery')}</dt><dd>${bat !== null ? `<span class="${bat < 80 ? 'w-soon' : ''}">${esc(nf(bat))} %</span>${sub(d.batDate ? t('bat_measured', { d: fmt(d.batDate) }) : '')}` : '—'}${has(d.batCycles) ? sub(t('bat_cycles', { n: nf(d.batCycles) })) : ''}${(d.batLog || []).length ? sub(t('bat_prev', { x: d.batLog.map(r => `${nf(r.salud)} %${has(r.ciclos) ? ', ' + t('bat_cycles', { n: nf(r.ciclos) }) : ''} (${fmt(r.fecha)})`).join('; ') })) : ''}</dd>` : ''}
      </dl></section>` : ''}
    <section class="panel"><h2>${T('net')}</h2>
      ${nics.length ? `<dl class="kv">${nics.map(n => `<dt>${n.type === 'wifi' ? 'Wi-Fi' : 'Ethernet'}</dt><dd>${esc(listName('nicModels', n.modelId)) || '—'}${n.mac ? `<span class="mono" style="display:block;font-size:12px">${esc(n.mac)}</span>` : ''}${chips(n.type === 'wifi' ? [chip(listName('wifiGens', n.wifiGen)), chip(listName('btVers', n.btVer))] : [chip(withUnit(n.speed, n.speedUnit))])}</dd>`).join('')}</dl>` : `<p class="muted">${T('no_nics')}</p>`}
    </section>
    <section class="panel"><h2>${T('purchase')}</h2>
      <dl class="kv"><dt>${T('k_bought')}</dt><dd>${fmt(d.compra)}</dd><dt>${T('k_age')}</dt><dd>${d.compra ? esc(age(d.compra)) : '—'}</dd><dt>${T('k_wend')}</dt><dd>${warranty(d, true)}</dd><dt>${T('fd_wext')}</dt><dd>${d.garantiaExt === 'yes' ? T('yes') : d.garantiaExt === 'no' ? T('no') : dash}</dd><dt>${T('k_supplier')}</dt><dd>${esc(tx(d.proveedor)) || '—'}</dd><dt>${T('k_invoice')}</dt><dd class="mono">${esc(d.factura) || '—'}</dd><dt>${T('k_price')}</dt><dd>${d.precio ? money(d.precio) : '—'}</dd><dt>${T('k_repcost')}</dt><dd>${money(gasto)}</dd></dl>
    </section>
  </div>
  ${tx(d.notas) ? `<section class="panel"><h2>${T('notes')}</h2><p style="margin:0;white-space:pre-line">${esc(tx(d.notas))}</p></section>` : ''}
  <section class="panel"><h2>${T('user_hist')}</h2>
    ${hist.length ? `<div class="tablebox"><table><thead><tr><th>${T('th_person')}</th><th>${T('th_from')}</th><th>${T('th_to')}</th><th>${T('th_dur')}</th><th>${T('th_faults')}</th><th>${T('th_handover')}</th></tr></thead><tbody>
      ${hist.map(h => { const fs = faultsIn(d.id, h.desde, h.hasta); return `<tr><td>${holderCell(h)}</td><td>${fmt(h.desde)}</td><td>${h.hasta ? fmt(h.hasta) : `<b>${T('current_lbl')}</b>`}</td><td>${esc(age(h.desde, h.hasta))}</td>
        <td>${fs.length ? `<b>${fs.length}</b>${fs.map(f => `<span class="t2">${fmt(f.fecha)} · ${esc(tx(f.descripcion))}</span>`).join('')}` : dash}</td>
        <td>${esc(tx(h.notas)) || dash}${h.condicion ? `<span class="t2">${T('returned_cond', { c: cd(h.condicion) })}</span>` : ''}</td></tr>`; }).join('')}
    </tbody></table></div>` : `<p class="muted">${T('never_assigned')}</p>`}
  </section>
  <section class="panel"><h2>${T('inc_hist')}</h2>
    ${incs.length ? `<div class="tablebox"><table><thead><tr><th>${T('th_date')}</th><th>${T('th_kind')}</th><th>${T('th_desc')}</th><th>${T('th_holder')}</th><th>${T('th_parts')}</th><th>${T('th_cost')}</th><th>${T('th_status')}</th></tr></thead><tbody>
      ${incs.map(i => { const h = holderAt(d.id, i.fecha), p = h && !h.deptId && emp(h.employeeId); return `<tr><td>${fmt(i.fecha)}</td><td>${esc(itp(i.tipo))}</td><td>${esc(tx(i.descripcion))}${tx(i.proveedor) ? `<span class="t2">${esc(tx(i.proveedor))}</span>` : ''}</td>
        <td>${p ? `<a href="#empleado-${p.id}">${esc(p.nombre)}</a>` : h?.deptId ? esc(deptName(h.deptId)) : `<span class="muted">${T('nobody')}</span>`}</td><td>${esc(tx(i.piezas)) || dash}</td><td>${money(i.coste)}</td>
        <td>${i.estado === 'abierta' ? `<div class="row">${pill('abierta', t('open'))}${ed ? `<button class="btn small" type="button" data-act="resolver" data-id="${i.id}">${T('mark_resolved')}</button>` : ''}</div>` : `${pill('resuelta', t('resolved'))}<span class="t2">${fmt(i.resuelta)}</span>`}</td></tr>`; }).join('')}
    </tbody></table></div>` : `<p class="muted">${T('no_inc')}</p>`}
  </section>`;
}

const FE = { q: '', activos: 'todos', contrato: 'todos' };
function viewEmployees() {
  return `
  <div class="head"><div><h1>${T('people_title')}</h1><p class="sub">${T('people_sub')}</p></div>
    <div class="row">${reloadBtn()}${can('edit') ? `<button class="btn primary" type="button" data-act="nuevoEmpleado">${T('new_person')}</button>` : ''}</div></div>
  <div class="toolbar">
    <input type="search" id="eq" placeholder="${T('search_people')}" value="${esc(FE.q)}" aria-label="${T('lbl_search')}">
    <select id="eactivos" aria-label="${T('lbl_situation')}">${opts([['todos', t('f_all')], ...EMP_STATES.map(s => [s, t('es_' + s)])], FE.activos)}</select>
    <select id="econtrato" aria-label="${T('k_contract')}">${opts([['todos', t('ct_all')], ...CONTRACTS.map(c => [c || 'unset', t(ctKey(c))])], FE.contrato)}</select>
  </div>
  <div class="tablebox" id="empTable"></div>`;
}
function drawEmpRows() {
  const q = FE.q.trim().toLowerCase();
  const rows = S.employees.filter(e => (FE.activos === 'todos' || empState(e) === FE.activos) && (FE.contrato === 'todos' || (e.contrato || 'unset') === FE.contrato) && (!q || [e.nombre, e.email, deptNames(e), locNames(e)].join(' ').toLowerCase().includes(q)))
    .sort((a, b) => a.nombre.localeCompare(b.nombre, lang));
  $('#empTable').innerHTML = rows.length ? `<table><thead><tr><th>${T('th_name')}</th><th>${T('lbl_dept')}</th><th>${T('th_loc')}</th><th>${T('th_curdev')}</th><th>${T('th_sit')}</th></tr></thead><tbody>
    ${rows.map(e => { const ds = S.assignments.filter(a => a.employeeId === e.id && !a.hasta).map(a => dev(a.deviceId)).filter(Boolean);
      return `<tr class="click" data-go="empleado-${e.id}"><td><b>${esc(e.nombre)}</b>${tempChip(e)}<span class="t2">${esc(e.email)}</span></td><td>${esc(deptNames(e))}</td><td>${esc(locNames(e))}</td>
      <td><div class="row">${ds.length ? ds.map(tagLink).join('') : `<span class="muted">${T('none')}</span>`}</div></td>
      <td>${empPill(e)}${empState(e) !== 'activo' && e.estadoFecha ? `<span class="t2">${T('since_d', { d: fmt(e.estadoFecha) })}</span>` : ''}</td></tr>`; }).join('')}
  </tbody></table>` : `<div class="empty">${T('no_match_people')}</div>`;
}

function viewEmployee(id) {
  const e = emp(id);
  if (!e) return `<p>${T('not_found_person')} <a href="#empleados">${T('back_list')}</a></p>`;
  const asg = S.assignments.filter(a => a.employeeId === e.id).sort((x, y) => y.desde.localeCompare(x.desde));
  const cur2 = asg.filter(a => !a.hasta), past = asg.filter(a => a.hasta);
  const dash = '<span class="muted">—</span>';
  const row = a => { const d = dev(a.deviceId), m = d ? model(d.modelId) : {}, fs = d ? faultsIn(d.id, a.desde, a.hasta) : [];
    return d ? `<tr class="click" data-go="dispositivo-${d.id}"><td>${tagLink(d)}</td><td><b>${esc(devTitle(d))}</b><span class="t2">${hostExtra(d) || esc(d.tag)}</span></td><td>${fmt(a.desde)}</td><td>${a.hasta ? fmt(a.hasta) : pill(d.estado)}</td>
      <td>${fs.length ? `<b>${fs.length}</b>${fs.map(f => `<span class="t2">${esc(tx(f.descripcion))}</span>`).join('')}` : dash}</td><td>${esc(tx(a.notas)) || dash}</td></tr>` : ''; };
  const head = last => `<thead><tr><th>${T('th_tag')}</th><th>${T('th_device')}</th><th>${T('th_from')}</th><th>${T(last)}</th><th>${T('th_faults')}</th><th>${T('th_handed')}</th></tr></thead>`;
  const st = empState(e);
  return `
  <div class="backrow"><a class="back" href="#empleados">${T('back_people')}</a>${reloadBtn()}</div>
  <div class="devhead">
    <div class="id"><div class="row">${empPill(e)}${tempChip(e)}</div><h1>${esc(e.nombre)}</h1><p class="sub">${esc(deptNames(e))} · ${esc(locNames(e))} · ${esc(e.email)}</p></div>
    ${can('edit') ? `<div class="row"><button class="btn" type="button" data-act="editarEmpleado" data-id="${e.id}">${T('btn_edit')}</button><button class="btn" type="button" data-act="situacion" data-id="${e.id}">${T('btn_situation')}</button></div>` : ''}
  </div>
  ${st === 'salida' && cur2.length ? `<div class="notice bad">${T('n_person_left', cur2.length)}</div>` : ''}
  ${st === 'baja' ? `<div class="notice">${T('n_onleave', { name: e.nombre, d: fmt(e.estadoFecha) })}</div>` : ''}
  <section class="panel"><h2>${T('cur_devices')}</h2>
    ${cur2.length ? `<div class="tablebox"><table>${head('th_status')}<tbody>${cur2.map(row).join('')}</tbody></table></div>` : `<p class="muted">${T('no_cur')}</p>`}
  </section>
  <section class="panel"><h2>${T('past_devices')}</h2>
    ${past.length ? `<div class="tablebox"><table>${head('th_to')}<tbody>${past.map(row).join('')}</tbody></table></div>` : `<p class="muted">${T('no_hist')}</p>`}
  </section>
  <section class="panel"><h2>${T('data')}</h2>
    <dl class="kv"><dt>${T('k_hired')}</dt><dd>${fmt(e.alta)}</dd><dt>${T('k_tenure')}</dt><dd>${esc(age(e.alta, st === 'salida' ? e.estadoFecha : null))}</dd><dt>${T('k_email')}</dt><dd>${esc(e.email)}</dd>
      <dt>${T('k_contract')}</dt><dd>${T(ctKey(e.contrato))}</dd>
      <dt>${T('th_sit')}</dt><dd>${empPill(e)}${st !== 'activo' && e.estadoFecha ? `<span class="muted" style="display:block;font-size:12.5px">${T('since_d', { d: fmt(e.estadoFecha) })}</span>` : ''}</dd></dl>
  </section>`;
}

/* ================= settings ================= */
const SET_GROUPS = [
  { id: 'general', items: [['acerca', 'set_about', null], ['actualizaciones', 'set_updates', null], ['region', 'set_region', null], ['marca', 'set_brand', null]] },
  { id: 'access', items: [['usuarios', 'set_users', () => S.users.filter(u => u.activo).length], ['contrasenas', 'set_pwpolicy', null]] },
  { id: 'org', items: [['departamentos', 'set_depts', () => S.depts.length], ['ubicaciones', 'set_locs', () => S.locations.length]] },
  { id: 'catalog', items: [['tipos', 'set_types', () => S.types.length], ['modelos', 'set_models', () => S.models.length]] },
  { id: 'parts', items: [['procesadores', 'set_cpus', () => S.cpus.length], ['graficas', 'set_gpus', () => S.gpus.length], ['memoria', 'set_ram', () => S.ramGens.length], ['formatosram', 'set_ramforms', () => S.ramForms.length],
    ['almacenamiento', 'set_disk', () => S.diskTypes.length], ['formatosdisco', 'set_diskforms', () => S.diskForms.length], ['conectores', 'set_conns', () => S.diskConns.length]] },
  { id: 'software', items: [['macos', 'set_macver', () => S.macVersions.length], ['winver', 'set_winver', () => S.winVersions.length], ['winedition', 'set_wined', () => S.winEditions.length], ['distros', 'set_distros', () => S.linuxDistros.length], ['linuxver', 'set_linuxver', () => S.linuxVersions.length]] },
  { id: 'network', items: [['tarjetas', 'set_nicmodels', () => S.nicModels.length], ['wifigen', 'set_wifigens', () => S.wifiGens.length], ['bluetooth', 'set_bt', () => S.btVers.length]] },
  { id: 'data', items: [['datos', 'set_data', null]] },
];
const SET_SECTIONS = SET_GROUPS.flatMap(g => g.items.map(i => [...i, g.id]));
const GROUP_ICONS = {
  general: '<path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/><circle cx="12" cy="12" r="9"/>',
  access: '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
  org: '<path d="M4 21V5a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v16M14 9h5a1 1 0 0 1 1 1v11M3 21h18M8 8h2M8 12h2M8 16h2"/>',
  catalog: '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20"/>',
  software: '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M7 6.5h.01M10 6.5h.01"/>',
  network: '<path d="M2 9a15 15 0 0 1 20 0M5.5 12.5a10 10 0 0 1 13 0M9 16a5 5 0 0 1 6 0"/><circle cx="12" cy="19.5" r="1"/>',
  data: '<ellipse cx="12" cy="5.5" rx="7.5" ry="2.5"/><path d="M4.5 5.5v13c0 1.4 3.4 2.5 7.5 2.5s7.5-1.1 7.5-2.5v-13M4.5 12c0 1.4 3.4 2.5 7.5 2.5s7.5-1.1 7.5-2.5"/>',
  parts: '<rect x="6" y="6" width="12" height="12" rx="1.5"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
};
const gIcon = id => `<svg class="i" viewBox="0 0 24 24">${GROUP_ICONS[id]}</svg>`;
function viewSettings(sec) {
  if (!can('admin')) return `<div class="notice info">${T('no_perm')}</div>`;
  const found = SET_SECTIONS.find(x => x[0] === sec);
  const nav = `<a href="#ajustes" class="home${found ? '' : ' on'}"><svg class="i" viewBox="0 0 24 24"><rect x="4" y="4" width="7" height="7" rx="1"/><rect x="13" y="4" width="7" height="7" rx="1"/><rect x="4" y="13" width="7" height="7" rx="1"/><rect x="13" y="13" width="7" height="7" rx="1"/></svg>${T('set_home')}</a>` + SET_GROUPS.map(g => `<div class="setgroup" role="group" aria-label="${T('grp_' + g.id)}"><span class="setglabel" data-g="${g.id}">${gIcon(g.id)}${T('grp_' + g.id)}</span>
    ${g.items.map(([k, lab, n]) => `<a href="#ajustes-${k}" class="${k === sec ? 'on' : ''}">${T(lab)}${n ? `<span>${n()}</span>` : ''}</a>`).join('')}</div>`).join('');
  let body;
  if (!found) body = settingsHome();
  else if (sec === 'usuarios') body = settingsUsers();
  else if (sec === 'region') body = settingsRegion();
  else if (sec === 'contrasenas') body = settingsPasswords();
  else if (sec === 'marca') body = settingsBrand();
  else if (sec === 'datos') body = settingsData();
  else if (sec === 'acerca') body = settingsAbout();
  else if (sec === 'actualizaciones') body = settingsUpdates();
  else body = settingsList(sec);
  const crumb = found ? `<p class="crumb"><a href="#ajustes">${T('set_title')}</a> <span>/</span> ${T('grp_' + found[3])}</p>` : '';
  return `<div class="head"><div><h1>${T('set_title')}</h1><p class="sub">${T('set_sub', { org: S.settings.orgName })}</p></div></div>
    <div class="settings"><nav class="setnav" aria-label="${T('set_title')}">${nav}</nav><div class="stack">${crumb}${body}</div></div>`;
}
function settingsHome() {
  return `<div class="setcards">${SET_GROUPS.map(g => `<section class="panel setcard">
    <div class="sethead" data-g="${g.id}">${gIcon(g.id)}<div><h2>${T('grp_' + g.id)}</h2><p class="sub">${T('grp_' + g.id + '_d')}</p></div></div>
    <div class="setlinks">${g.items.map(([k, lab, n]) => `<a href="#ajustes-${k}"><span class="txt"><b>${T(lab)}</b><small>${T(lab + '_sub')}</small></span>${n ? `<span class="count">${n()}</span>` : '<span class="count">›</span>'}</a>`).join('')}</div>
  </section>`).join('')}</div>`;
}
function settingsList(key) {
  const C = LISTS[key], items = S[C.coll];
  return `<section class="panel">
    <div class="head"><div><h2>${T(C.title)}</h2><p class="sub">${T(C.sub)}</p></div><button class="btn primary" type="button" data-set="add" data-list="${key}">${T('add_x', { x: t(C.single) })}</button></div>
    <div class="tablebox"><table><thead><tr>${C.cols.map(c => `<th>${T(c[0])}</th>`).join('')}<th>${T('th_usage')}</th><th></th></tr></thead><tbody>
      ${items.map(x => { const n = C.count(x); return `<tr>${C.cols.map(c => `<td>${c[1](x)}</td>`).join('')}<td class="muted">${esc(C.usageText(x))}</td>
        <td class="act"><div class="row" style="justify-content:flex-end"><button class="btn small" type="button" data-set="edit" data-list="${key}" data-id="${x.id}">${T('btn_edit')}</button>
        <button class="btn small danger" type="button" data-set="del" data-list="${key}" data-id="${x.id}"${n ? ` disabled title="${T('in_use_cant')}"` : ''}>${T('delete')}</button></div></td></tr>`; }).join('')}
    </tbody></table></div></section>`;
}
function settingsUsers() {
  return `<section class="panel">
    <div class="head"><div><h2>${T('set_users')}</h2><p class="sub">${T('set_users_sub')}</p></div><button class="btn primary" type="button" data-set="addUser">${T('add_x', { x: t('item_user') })}</button></div>
    <div class="tablebox"><table><thead><tr><th>${T('th_name')}</th><th>${T('th_role')}</th><th>${T('th_status')}</th><th>${T('th_last')}</th><th></th></tr></thead><tbody>
      ${S.users.map(u => `<tr><td><b>${esc(u.nombre)}</b> ${u.id === cur.id ? `<span class="muted">${T('you')}</span>` : ''}<span class="t2">${esc(u.email)}${u.username ? ' · ' + esc(u.username) : ''}</span></td>
        <td><span class="pill st-${esc(u.rol)}" tabindex="0" data-tip="${T('role_' + u.rol + '_d')}">${esc(rl(u.rol))}</span></td><td>${u.activo ? pill('on', t('u_active')) : pill('off', t('u_inactive'))}${u.mustChange ? ` <span class="chip" tabindex="0" data-tip="${T('chip_must_change_d')}">${T('chip_must_change')}</span>` : ''}</td><td>${u.last ? fmt(u.last) : `<span class="muted">${T('never')}</span>`}</td>
        <td class="act"><div class="row" style="justify-content:flex-end"><button class="btn small" type="button" data-set="editUser" data-id="${u.id}">${T('btn_edit')}</button>
        <button class="btn small${u.activo ? ' danger' : ''}" type="button" data-set="toggleUser" data-id="${u.id}"${u.id === cur.id ? ' disabled' : ''}>${u.activo ? T('deactivate') : T('activate')}</button></div></td></tr>`).join('')}
    </tbody></table></div>
  </section>`;
}
function settingsRegion() {
  const s = S.settings, sample = today();
  return `<section class="panel">
    <div><h2>${T('set_region')}</h2><p class="sub">${T('set_region_sub')}</p></div>
    <form class="regionform" id="regionForm" novalidate>
      <label>${T('f_org')}<input name="orgName" id="r-org" value="${esc(s.orgName)}"></label>
      <label>${T('f_prefix')}<input name="tagPrefix" id="r-prefix" value="${esc(s.tagPrefix)}" maxlength="10"><span class="hint" id="r-prefix-hint">${T('f_prefix_hint', { x: nextTag() })}</span></label>
      <label>${T('f_numbering')}<select name="tagNumbering" id="r-numbering">${opts([['type', t('num_type')], ['global', t('num_global')]], s.tagNumbering || 'type')}</select><span class="hint" id="r-numbering-hint"></span></label>
      <label>${T('f_datefmt')}<select name="dateFmt" id="r-date">${opts(DATE_FMTS.map(f => [f, `${t('df_' + f)} · ${fmt(sample, f)}`]), s.dateFmt)}</select></label>
      <label>${T('f_currency')}<select name="currency" id="r-cur">${opts(CURRENCIES.map(c => [c, `${c} · ${money(1234.5, c)}`]), s.currency)}</select></label>
      <label>${T('f_wdays')}<input name="warrantyDays" id="r-wdays" type="number" min="0" max="730" step="1" value="${esc(s.warrantyDays)}"></label>
      <label class="check"><input type="checkbox" name="hostnameIsTag" id="r-hosttag"${s.hostnameIsTag ? ' checked' : ''}> ${T('f_hosttag')}</label>
      <span class="hint" style="margin-top:-8px">${T('f_hosttag_hint', { x: nextTag() })}</span>
      <p class="muted" id="r-preview" style="margin:0"></p>
      <div><button class="btn primary" type="submit">${T('save')}</button></div>
    </form></section>`;
}
function bindRegion() {
  const f = $('#regionForm'); if (!f) return;
  const prev = () => { const v = Object.fromEntries(new FormData(f)); $('#r-preview').textContent = t('region_preview', { d: fmt(today(), v.dateFmt), m: money(1149, v.currency) }); $('#r-prefix-hint').textContent = t('f_prefix_hint', { x: nextTag(undefined, v.tagPrefix || '', v.tagNumbering) });
    const p = v.tagPrefix || ''; $('#r-numbering-hint').textContent = t(v.tagNumbering === 'global' ? 'num_global_hint' : 'num_type_hint', { a: p + 'LAP001', b: p + 'MB001', c: p + 'MB002' }); };
  f.addEventListener('input', prev); prev();
  f.addEventListener('submit', async e => {
    e.preventDefault();
    const v = Object.fromEntries(new FormData(f));
    const body = { orgName: v.orgName.trim() || S.settings.orgName, tagPrefix: v.tagPrefix.trim(), tagNumbering: v.tagNumbering, dateFmt: v.dateFmt, currency: v.currency, warrantyDays: Math.max(0, parseInt(v.warrantyDays, 10) || 0), hostnameIsTag: v.hostnameIsTag === 'on' };
    try { await mutate('PUT', 'settings', body); } catch (err) { if (err.status !== 401) toast(t(err.code)); return; }
    applyChrome(); route(); toast(t('region_saved'), true);
  });
}
const activeAdmins = () => S.users.filter(u => u.activo && u.rol === 'admin').length;
function userForm(u) {
  return `<div class="fields">
    <label class="full">${T('th_name')}<input name="nombre" id="u-nombre" value="${esc(u?.nombre)}"></label>
    <label class="full">${T('f_email')}<input name="email" id="u-email" type="email" value="${esc(u?.email)}"></label>
    <label class="full">${T('f_username')}<input name="username" id="u-username" value="${esc(u?.username)}" maxlength="150" autocapitalize="none" spellcheck="false"><span class="hint">${T(u ? 'f_username_hint' : 'f_username_hint_new')}</span></label>
    <label>${T('f_role')}<select name="rol" id="u-rol">${kopts(ROLES, rl, u?.rol || 'tech')}</select></label>
    <label>${u ? T('f_pass_new') : T('f_pass_tmp')}<input name="pass" id="u-pass" type="password" autocomplete="new-password">${u ? `<span class="hint">${T('f_pass_hint')}</span>` : ''}</label>
    <div class="full"><div id="u-meter"></div></div>
    ${u && u.id === cur.id ? '' : `<label class="check full"><input type="checkbox" name="mustChange" id="u-must"${u ? (u.mustChange ? ' checked' : '') : ' checked'}> ${T('f_must_change')}</label><span class="hint full" style="margin-top:-6px">${T('f_must_change_d')}</span>`}
    <div class="full" id="u-roledesc"></div></div>`;
}
function readUser(v, u) {
  const nombre = v.nombre.trim(), email = v.email.trim().toLowerCase();
  if (!nombre || !email) { toast(t('err_user')); return null; }
  if (S.users.some(x => x.email.toLowerCase() === email && x !== u)) { toast(t('err_email_dup')); return null; }
  const username = (v.username || '').trim().toLowerCase();
  if (username && !/^[a-z0-9._-]{2,150}$/.test(username)) { toast(t('err_username')); return null; }
  if (username && S.users.some(x => (x.username || '') === username && x !== u)) { toast(t('err_username_dup')); return null; }
  if (!u && !v.pass) { toast(t('err_pass')); return null; }
  if (v.pass && !pwMeets(v.pass, S.settings.pwPolicy)) { toast(t('err_pass_weak')); return null; }
  if (u && u.rol === 'admin' && v.rol !== 'admin' && u.activo && activeAdmins() === 1) { toast(t('err_last_admin')); return null; }
  return { nombre, email, username, rol: v.rol, mustChange: v.mustChange === 'on', ...(v.pass ? { pass: v.pass } : {}) };
}
const SET_ACTIONS = {
  add(list) { const C = LISTS[list]; openDialog(t('add_x', { x: t(C.single) }), C.form(null, false, 's'), async (v, fd) => { const r = C.read(v, fd, null); if (!r) return false; const { item } = await mutate('POST', 'lists/' + C.coll, r); return t('added_x', { x: C.label(item) }); }, t('add')); },
  edit(list, id) { const C = LISTS[list], x = byId(C.coll, id); openDialog(t('edit_x', { x: t(C.single) }), C.form(x, false, 's'), async (v, fd) => { const r = C.read(v, fd, x); if (!r) return false; await mutate('PUT', `lists/${C.coll}/${id}`, r); return t('saved'); }); },
  del(list, id) {
    const C = LISTS[list], x = byId(C.coll, id);
    if (C.count(x)) { toast(t('in_use_cant')); return; }
    openDialog(t('delete_title', { name: C.label(x) }), `<p style="margin:0">${T('delete_body', { name: C.label(x) })}</p>`, async () => { await mutate('DELETE', `lists/${C.coll}/${id}`); return t('deleted'); }, t('delete'), true);
  },
  addUser() {
    openDialog(t('add_x', { x: t('item_user') }), userForm(), async v => { const r = readUser(v, null); if (!r) return false; await mutate('POST', 'users', r); return t('added_x', { x: r.nombre }); }, t('add')); bindRoleDesc();
    // the username follows the start of the email until someone types their own (ana.lopez@… -> ana.lopez)
    const mail = $('#u-email'), name = $('#u-username'); let auto = '';
    mail.addEventListener('input', () => { if (name.value === auto) name.value = auto = mail.value.split('@')[0].toLowerCase().replace(/[^a-z0-9._-]/g, ''); });
  },
  editUser(_, id) { const u = byId('users', id); openDialog(t('edit_x', { x: u.nombre }), userForm(u), async v => { const r = readUser(v, u); if (!r) return false; await mutate('PUT', 'users/' + id, r); applyChrome(); return t('saved'); }); bindRoleDesc(); },
  async toggleUser(_, id) {
    const u = byId('users', id);
    if (u.id === cur.id) { toast(t('err_self')); return; }
    if (u.activo && u.rol === 'admin' && activeAdmins() === 1) { toast(t('err_last_admin')); return; }
    let d; try { d = await mutate('POST', `users/${id}/toggle`, {}); } catch (err) { if (err.status !== 401) toast(t(err.code)); return; }
    route(); toast(d.activo ? t('user_on') : t('user_off'), true);
  },
};
function bindRoleDesc() { const pw = $('#u-pass'), m = () => drawMeter($('#u-meter'), pw.value, S.settings.pwPolicy); pw.oninput = m; m(); const s = $('#u-rol'), o = $('#u-roledesc'); const f = () => o.innerHTML = `<p class="muted" style="margin:0;font-size:13px">${T('role_' + s.value + '_d')}</p>`; s.onchange = f; f(); }

/* ================= inventory actions ================= */
function deviceForm(d) {
  d = d || { tag: nextTag(S.types[0]?.id), loc: storageLoc(), osFamily: 'win', enc: 'yes', compra: today(), typeId: S.types[0]?.id, modelId: S.models.find(m => m.typeId === S.types[0]?.id)?.id, nics: [{ type: 'wifi' }], disks: [{ unit: 'GB' }] };
  const ty = devType(d), named = usesName(ty);
  const f = (n, l, type = 'text', a, extra = '') => `<label>${T(l, a)}<input name="${n}" id="f-${n}" type="${type}" value="${esc(tx(d[n]))}"${type === 'number' ? ' step="1" min="0"' : ''}${extra}></label>`;
  const scr = hasScreen(ty), batt = hasBattery(ty);
  const ended = d.garantiaEnded && !d.garantia;
  return `<div class="fields">
    ${S.settings.hostnameIsTag ? `<label>${T('fd_tag')}<input name="tag" id="f-tag" value="${esc(d.tag)}"><span class="hint">${T('host_same')}</span></label>` : f('tag', 'fd_tag') + f('nombre', 'fd_host')}
    ${f('serial', 'fd_serial')}
    <label>${T('f_type')}${selPlus('tipos', 'typeId', 'f-typeId', opts(S.types.map(x => [x.id, tx(x.nombre)]), ty))}</label>
    <label class="full" id="f-modelwrap"${named ? ' hidden' : ''}>${T('fd_model')}${selPlus('modelos', 'modelId', 'f-modelId', modelOpts(ty, d.modelId))}</label>
    <label class="full" id="f-namewrap"${named ? '' : ' hidden'}>${T('fd_customname')}<input name="customName" id="f-customName" value="${esc(d.customName)}" placeholder="${T('fd_customname_ph')}"></label>

    <div class="fields full" id="f-portable"${scr || batt ? '' : ' hidden'}>
      <div class="sect" id="f-scrtitle">${esc(screenTitle(ty))}</div>
      <label class="f-scr"${scr ? '' : ' hidden'}>${T('fd_screen')}<input name="screen" id="f-screen" type="number" min="0" step="0.1" value="${esc(d.screen ?? '')}"></label>
      <label class="f-scr"${scr ? '' : ' hidden'}>${T('fd_touch')}<select name="touch" id="f-touch">${triOpts(d.touch)}</select></label>
      <label class="f-bat"${batt ? '' : ' hidden'}>${T('fd_bat')}<input name="batHealth" id="f-batHealth" type="number" min="0" max="100" step="1" value="${esc(d.batHealth ?? '')}"></label>
      <label class="f-bat"${batt ? '' : ' hidden'}>${T('fd_bat_date')}<input name="batDate" id="f-batDate" type="date" value="${esc(d.batDate || '')}"></label>
    </div>

    <div class="sect">${T('sect_hw')}</div>
    <span class="hint full">${T('hw_hint')}</span>
    <label class="full">${T('fd_cpu')}${selPlus('procesadores', 'cpuId', 'f-cpuId', opts([['', t('not_set')], ...S.cpus.map(c => [c.id, c.nombre])], d.cpuId || ''))}<span class="hint" id="f-cpuinfo"></span></label>
    <label class="full">${T('fd_cpu_rep')}<select name="cpuRep" id="f-cpuRep">${repOpts(d.cpuRep)}</select></label>

    <label>${T('fd_ram')}${numUnit('ramSize', d.ramSize, d.ramUnit, UNITS.ram)}</label>
    <label>${T('fd_ram_gen')}${selPlus('memoria', 'ramGen', 'f-ramGen', opts([['', t('not_set')], ...S.ramGens.map(x => [x.id, x.nombre])], d.ramGen || ''))}</label>
    <label>${T('fd_ram_speed')}${numUnit('ramSpeed', d.ramSpeed, d.ramSpeedUnit, UNITS.ramSpeed)}</label>
    <label>${T('fd_ram_rep')}<select name="ramRep" id="f-ramRep">${repOpts(d.ramRep)}</select></label>
    <div class="subfields full" id="f-ramsub"${d.ramRep === 'yes' ? '' : ' hidden'}>
      <label>${T('fd_ram_modules')}<input name="ramModules" id="f-ramModules" type="number" min="1" step="1" value="${esc(d.ramModules ?? '')}"></label>
      <label>${T('fd_ram_modsize')}${numUnit('ramModSize', d.ramModSize, d.ramModUnit, ['GB', 'MB'])}</label>
      <label class="full">${T('fd_ram_form')}${selPlus('formatosram', 'ramForm', 'f-ramForm', opts([['', t('not_set')], ...S.ramForms.map(x => [x.id, x.nombre])], d.ramForm || ''))}</label>
      <span class="hint full w-soon" id="f-rammis" hidden></span>
    </div>

    <div class="sect">${T('k_disk')}</div>
    <div class="full niclist" id="f-disks">${(d.disks || []).map(k => diskRow(k)).join('')}</div>
    <div class="full"><button type="button" class="btn small" id="f-diskadd">${T('disk_add')}</button></div>

    <div class="sect">${T('sect_gpu')}</div>
    <label class="full">${T('fd_gpu')}${selPlus('graficas', 'gpuId', 'f-gpuId', listOpts('gpus', d.gpuId))}<span class="hint" id="f-gpuinfo"></span></label>

    <div class="sect">${T('sect_sw')}</div>
    <label>${T('fd_os')}<select name="osFamily" id="f-osFamily">${opts([['', t('not_set')], ...OS_FAMILIES], d.osFamily || '')}</select></label>
    <label class="os-f" data-os="mac"${d.osFamily === 'mac' ? '' : ' hidden'}>${T('fd_osver')}${selPlus('macos', 'osVerMac', 'f-osVerMac', listOpts('macVersions', d.osFamily === 'mac' ? d.osVerId : ''))}</label>
    <label class="os-f" data-os="win"${d.osFamily === 'win' ? '' : ' hidden'}>${T('fd_osver')}${selPlus('winver', 'osVerWin', 'f-osVerWin', listOpts('winVersions', d.osFamily === 'win' ? d.osVerId : ''))}</label>
    <label class="os-f" data-os="win"${d.osFamily === 'win' ? '' : ' hidden'}>${T('fd_osed')}${selPlus('winedition', 'osEditionId', 'f-osEdition', listOpts('winEditions', d.osEditionId))}</label>
    <label class="os-f" data-os="linux"${d.osFamily === 'linux' ? '' : ' hidden'}>${T('fd_distro')}${selPlus('distros', 'osDistroId', 'f-osDistro', listOpts('linuxDistros', d.osDistroId))}</label>
    <label class="os-f" data-os="linux"${d.osFamily === 'linux' ? '' : ' hidden'}>${T('fd_osver')}${selPlus('linuxver', 'osVerLinux', 'f-osVerLinux', linuxVerOpts(d.osDistroId, d.osFamily === 'linux' ? d.osVerId : ''))}</label>
    <label class="os-f" data-os="mac"${d.osFamily === 'mac' ? '' : ' hidden'}>${T('fd_oclp')}<select name="oclp" id="f-oclp">${triOpts(d.oclp)}</select></label>
    <label class="os-f" data-os="mac" id="f-oclpverwrap"${d.osFamily === 'mac' && d.oclp === 'yes' ? '' : ' hidden'}>${T('fd_oclp_ver')}<input name="oclpVersion" id="f-oclpver" value="${esc(d.oclpVersion)}" maxlength="20" placeholder="2.1.0"></label>
    <label class="os-f" data-os="mac"${d.osFamily === 'mac' ? '' : ' hidden'}>Hackintosh<select name="hackintosh" id="f-hackintosh">${triOpts(d.hackintosh)}</select></label>
    <label><span id="f-enclabel">${esc(encLabel(d.osFamily))}</span><select name="enc" id="f-enc">${triOpts(d.enc)}</select></label>
    <label>${T('fd_ad')}<select name="ad" id="f-ad">${triOpts(d.ad)}</select></label>
    <label>${T('fd_loc')}${selPlus('ubicaciones', 'loc', 'f-loc', opts(S.locations.map(l => [l.id, tx(l.nombre)]), d.loc))}</label>

    <div class="sect">${T('sect_net')}</div>
    <div class="full niclist" id="f-nics">${(d.nics || []).map(n => nicRow(n)).join('')}</div>
    <div class="full"><button type="button" class="btn small" id="f-nicadd">${T('nic_add')}</button></div>

    <div class="sect">${T('sect_purchase')}</div>
    ${f('compra', 'fd_bought', 'date')}${f('precio', 'fd_price', 'number', { c: curSym() })}
    ${f('proveedor', 'fd_supplier')}${f('factura', 'fd_invoice')}
    ${f('garantia', 'fd_wend', 'date', null, ended ? ' disabled' : '')}
    <label>${T('fd_wext')}<select name="garantiaExt" id="f-garantiaExt">${triOpts(d.garantiaExt)}</select></label>
    <span class="hint full" id="f-wexthint"${d.garantiaExt === 'yes' ? '' : ' hidden'}>${T('w_ext_hint')}</span>
    <label class="check full"><input type="checkbox" name="garantiaEnded" id="f-wended"${ended ? ' checked' : ''}> ${T('fd_wended')}</label>
    <label class="full">${T('fd_notes')}<textarea name="notas" id="f-notas">${esc(tx(d.notas))}</textarea></label>
  </div>`;
}
let nicSeq = 0;
function diskRow(k) {
  k = k || {};
  const i = ++nicSeq;
  return `<div class="nic" data-disk>
    <div class="nichead"><b class="disk-title">${T('k_disk')}</b><button type="button" class="btn small danger disk-del">${T('nic_remove')}</button></div>
    <label>${T('fd_capacity')}${numUnitN('disk_size', `f-disksize-${i}`, k.size, k.unit, UNITS.disk)}</label>
    <label>${T('fd_disk_type')}${selPlus('almacenamiento', 'disk_type', `f-disktype-${i}`, opts([['', t('not_set')], ...S.diskTypes.map(x => [x.id, x.nombre])], k.type || ''))}</label>
    <label>${T('fd_disk_conn')}${selPlus('conectores', 'disk_conn', `f-diskconn-${i}`, opts([['', t('not_set')], ...S.diskConns.map(x => [x.id, x.nombre])], k.conn || ''))}</label>
    <label>${T('fd_disk_rep')}<select name="disk_rep" id="f-diskrep-${i}" class="disk-rep">${repOpts(k.rep)}</select></label>
    <div class="subfields full disk-sub"${k.rep === 'yes' ? '' : ' hidden'}>
      <label class="full">${T('fd_disk_form')}${selPlus('formatosdisco', 'disk_form', `f-diskform-${i}`, opts([['', t('not_set')], ...S.diskForms.map(x => [x.id, x.nombre])], k.form || ''))}</label>
    </div>
  </div>`;
}
function numUnitN(name, id, val, unit, units) {
  return `<span class="numunit"><input name="${name}" id="${id}" type="number" min="0" step="any" value="${esc(val ?? '')}"><select name="${name}Unit" id="${id}-unit" aria-label="${T('unit_aria')}">${opts(units, unit || units[0])}</select></span>`;
}
/* number the drive cards when there is more than one */
function renumberDisks() { const rows = [...document.querySelectorAll('#f-disks [data-disk]')]; rows.forEach((r, i) => r.querySelector('.disk-title').textContent = rows.length > 1 ? t('disk_n', { n: i + 1 }) : t('k_disk')); }
function nicRow(n) {
  n = n || { type: 'wifi' };
  const i = ++nicSeq, wifi = n.type !== 'eth';
  return `<div class="nic" data-nic>
    <div class="nichead"><select name="nic_type" id="f-nictype-${i}" class="nic-type" aria-label="${T('nic_type')}">${opts([['wifi', 'Wi-Fi'], ['eth', 'Ethernet']], n.type || 'wifi')}</select>
      <button type="button" class="btn small danger nic-del">${T('nic_remove')}</button></div>
    <label>${T('nic_model')}${selPlus('tarjetas', 'nic_model', `f-nicmodel-${i}`, nicModelOpts(n.type || 'wifi', n.modelId))}</label>
    <label>${T('nic_mac')}<input name="nic_mac" id="f-nicmac-${i}" class="mono" value="${esc(n.mac)}" placeholder="${T('mac_ph')}" maxlength="17"></label>
    <label class="nic-w"${wifi ? '' : ' hidden'}>${T('nic_gen')}${selPlus('wifigen', 'nic_gen', `f-nicgen-${i}`, opts([['', t('not_set')], ...S.wifiGens.map(x => [x.id, x.nombre])], n.wifiGen || ''))}</label>
    <label class="nic-w"${wifi ? '' : ' hidden'}>${T('nic_bt')}${selPlus('bluetooth', 'nic_bt', `f-nicbt-${i}`, opts([['', t('not_set')], ...S.btVers.map(x => [x.id, x.nombre])], n.btVer || ''))}</label>
    <label class="nic-e full"${wifi ? ' hidden' : ''}>${T('nic_speed')}<span class="numunit"><input name="nic_speed" id="f-nicspeed-${i}" type="number" min="0" step="any" value="${esc(n.speed ?? '')}"><select name="nic_speedUnit" id="f-nicunit-${i}" aria-label="${T('unit_aria')}">${opts(['Gbps', 'Mbps'], n.speedUnit || 'Gbps')}</select></span></label>
  </div>`;
}
function bindHwForm() {
  const sel = id => $(id);
  // the type decides: model list (filtered) or a free name, and whether screen / battery fields apply
  sel('#f-typeId').addEventListener('change', e => {
    const ty = e.target.value, sc = hasScreen(ty), bt = hasBattery(ty), named = usesName(ty), ms = sel('#f-modelId'), keep = ms.value;
    // a new device's suggested tag follows its type, until someone types their own
    const tag = sel('#f-tag'); if (tag && tag.dataset.auto !== undefined && tag.value === tag.dataset.auto) tag.value = tag.dataset.auto = nextTag(ty);
    ms.innerHTML = modelOpts(ty, keep);
    sel('#f-modelwrap').hidden = named; sel('#f-namewrap').hidden = !named;
    sel('#f-portable').hidden = !sc && !bt; sel('#f-scrtitle').textContent = screenTitle(ty);
    document.querySelectorAll('#f-portable .f-scr').forEach(x => x.hidden = !sc); document.querySelectorAll('#f-portable .f-bat').forEach(x => x.hidden = !bt);
  });
  sel('#f-osDistro').addEventListener('change', e => { sel('#f-osVerLinux').innerHTML = linuxVerOpts(e.target.value, ''); });
  // operating system: show only the fields for the chosen family
  sel('#f-osFamily').addEventListener('change', e => {
    const fam = e.target.value;
    document.querySelectorAll('.os-f').forEach(x => x.hidden = !x.dataset.os.split(' ').includes(fam));
    sel('#f-enclabel').textContent = encLabel(fam);
    oclpVer();
  });
  // the OCLP version only when it is patched
  const oclpVer = () => { sel('#f-oclpverwrap').hidden = sel('#f-osFamily').value !== 'mac' || sel('#f-oclp').value !== 'yes'; };
  sel('#f-oclp').addEventListener('change', oclpVer);
  const gpuInfo = () => { sel('#f-gpuinfo').textContent = gpuDetail(byId('gpus', sel('#f-gpuId').value)); };
  sel('#f-gpuId').addEventListener('change', gpuInfo); gpuInfo();
  const cpuInfo = () => { sel('#f-cpuinfo').textContent = cpuDetail(byId('cpus', sel('#f-cpuId').value)); };
  sel('#f-cpuId').addEventListener('change', cpuInfo); cpuInfo();
  sel('#f-ramRep').addEventListener('change', e => { sel('#f-ramsub').hidden = e.target.value !== 'yes'; ramCheck(); });
  const disks = sel('#f-disks');
  disks.onclick = e => { const b = e.target.closest('.disk-del'); if (b) { b.closest('[data-disk]').remove(); renumberDisks(); } };
  disks.onchange = e => { if (e.target.matches('.disk-rep')) e.target.closest('[data-disk]').querySelector('.disk-sub').hidden = e.target.value !== 'yes'; };
  sel('#f-diskadd').onclick = () => { disks.insertAdjacentHTML('beforeend', diskRow({ unit: 'GB' })); renumberDisks(); disks.lastElementChild.querySelector('input').focus(); };
  renumberDisks();
  // modules × size should add up to the total
  const ramCheck = () => {
    const tot = numOrNull(sel('#f-ramSize').value), n = numOrNull(sel('#f-ramModules').value), each = numOrNull(sel('#f-ramModSize').value), hint = sel('#f-rammis');
    const off = sel('#f-ramRep').value === 'yes' && tot && n && each && Math.abs(toGB(tot, sel('#f-ramSizeUnit').value) - n * toGB(each, sel('#f-ramModSizeUnit').value)) > 0.01;
    hint.hidden = !off;
    if (off) hint.textContent = t('ram_mismatch', { n, s: withUnit(each, sel('#f-ramModSizeUnit').value), t: nf(n * toGB(each, sel('#f-ramModSizeUnit').value)) + ' GB' });
  };
  ['#f-ramSize', '#f-ramSizeUnit', '#f-ramModules', '#f-ramModSize', '#f-ramModSizeUnit'].forEach(s => sel(s).addEventListener('input', ramCheck));
  ramCheck();
  sel('#f-garantiaExt').addEventListener('change', e => { sel('#f-wexthint').hidden = e.target.value !== 'yes'; });
  sel('#f-wended').addEventListener('change', e => { const g = sel('#f-garantia'); g.disabled = e.target.checked; if (e.target.checked) g.value = ''; });
  const nics = sel('#f-nics');
  nics.onclick = e => { const b = e.target.closest('.nic-del'); if (b) b.closest('[data-nic]').remove(); };
  nics.onchange = e => { if (!e.target.matches('.nic-type')) return; const row = e.target.closest('[data-nic]'), wifi = e.target.value === 'wifi';
    row.querySelectorAll('.nic-w').forEach(x => x.hidden = !wifi); row.querySelectorAll('.nic-e').forEach(x => x.hidden = wifi);
    const ms = row.querySelector('select[name=nic_model]'); ms.innerHTML = nicModelOpts(e.target.value, ''); };
  sel('#f-nicadd').onclick = () => { nics.insertAdjacentHTML('beforeend', nicRow({ type: 'eth', speed: 1, speedUnit: 'Gbps' })); nics.lastElementChild.querySelector('select').focus(); };
}
function numUnit(name, val, unit, units) {
  return `<span class="numunit"><input name="${name}" id="f-${name}" type="number" min="0" step="any" value="${esc(val ?? '')}"><select name="${name}Unit" id="f-${name}Unit" aria-label="${T('unit_aria')}">${opts(units, unit || units[0])}</select></span>`;
}
const numOrNull = v => { const n = parseFloat(String(v ?? '').replace(',', '.')); return isFinite(n) && n > 0 ? n : null; };
function readDevice(v, fd, prev) {
  if (!v.tag.trim() || !v.serial.trim()) { toast(t('err_required')); return null; }
  const g = k => fd.getAll(k), types = g('nic_type'), models = g('nic_model'), macs = g('nic_mac'), gens = g('nic_gen'), bts = g('nic_bt'), speeds = g('nic_speed'), units = g('nic_speedUnit');
  const nics = [];
  for (let i = 0; i < types.length; i++) {
    const mac = normMac(macs[i] || '');
    if (!validMac(mac)) { toast(t('err_mac')); return null; }
    const wifi = types[i] === 'wifi';
    nics.push({ type: types[i], modelId: models[i] || '', mac, wifiGen: wifi ? gens[i] : '', btVer: wifi ? bts[i] : '', speed: wifi ? null : numOrNull(speeds[i]), speedUnit: units[i] || 'Gbps' });
  }
  const keep = (k, val) => prev && tx(prev[k]) === val ? prev[k] : val;   // keep translated example text when it was not changed
  const ty = v.typeId, named = usesName(ty), scr = hasScreen(ty), batt = hasBattery(ty), rr = v.ramRep === 'yes';
  if (!named && !v.modelId) { toast(t('err_model_req')); return null; }
  const dk = { size: g('disk_size'), unit: g('disk_sizeUnit'), type: g('disk_type'), rep: g('disk_rep'), form: g('disk_form'), conn: g('disk_conn') };
  const disks = dk.size.map((_, i) => ({ size: numOrNull(dk.size[i]), unit: dk.unit[i], type: dk.type[i], rep: dk.rep[i], form: dk.rep[i] === 'yes' ? dk.form[i] : '', conn: dk.conn[i] || '' }));
  const out = { tag: v.tag.trim(), nombre: S.settings.hostnameIsTag ? (prev?.nombre || '') : (v.nombre || '').trim(), serial: v.serial.trim(), typeId: ty, modelId: named ? '' : v.modelId, customName: named ? (v.customName || '').trim() : '', cpuId: v.cpuId, cpuRep: v.cpuRep,
    ramSize: numOrNull(v.ramSize), ramUnit: v.ramSizeUnit, ramGen: v.ramGen, ramSpeed: numOrNull(v.ramSpeed), ramSpeedUnit: v.ramSpeedUnit, ramRep: v.ramRep,
    ramModules: rr ? numOrNull(v.ramModules) : null, ramModSize: rr ? numOrNull(v.ramModSize) : null, ramModUnit: v.ramModSizeUnit, ramForm: rr ? v.ramForm : '',
    disks,
    gpuId: v.gpuId,
    osFamily: v.osFamily, osVerId: v.osFamily === 'mac' ? v.osVerMac : v.osFamily === 'win' ? v.osVerWin : v.osFamily === 'linux' ? v.osVerLinux : '', osVersion: '',
    osEditionId: v.osFamily === 'win' ? v.osEditionId : '', osDistroId: v.osFamily === 'linux' ? v.osDistroId : '', oclp: v.osFamily === 'mac' ? v.oclp : '', oclpVersion: v.osFamily === 'mac' && v.oclp === 'yes' ? (v.oclpVersion || '').trim() : '', hackintosh: v.osFamily === 'mac' ? v.hackintosh : '',
    enc: v.enc, ad: v.ad, loc: v.loc, nics,
    screen: scr ? numOrNull(v.screen) : null, touch: scr ? v.touch : '', batHealth: batt ? numOrNull(v.batHealth) : null, batDate: batt ? v.batDate : '',
    batLog: prev?.batLog ? [...prev.batLog] : [],
    compra: v.compra, precio: Number(v.precio) || 0, proveedor: keep('proveedor', v.proveedor), factura: v.factura,
    garantiaEnded: fd.has('garantiaEnded'), garantia: fd.has('garantiaEnded') ? '' : (v.garantia || ''), garantiaExt: v.garantiaExt, notas: keep('notas', v.notas) };
  // a new battery reading keeps the previous one in the history
  if (prev && has(prev.batHealth) && (prev.batHealth !== out.batHealth || prev.batDate !== out.batDate) && out.batHealth) out.batLog.unshift({ fecha: prev.batDate, salud: prev.batHealth });
  return out;
}
const personLocs = () => S.locations.filter(l => l.tipo !== 'storage').map(l => [l.id, tx(l.nombre)]);
function employeeForm(e) {
  e = e || { locs: [S.locations.find(l => l.tipo === 'office')?.id].filter(Boolean), depts: [], alta: today() };
  return `<div class="fields">
    <label class="full">${T('fe_name')}<input name="nombre" id="e-nombre" value="${esc(e.nombre)}"></label>
    <label class="full">${T('fe_email')}<input name="email" id="e-email" type="email" value="${esc(e.email)}"></label>
    ${multiList('depts', e.depts)}
    ${multiList('locs', e.locs)}
    <label>${T('fe_hired')}<input name="alta" id="e-alta" type="date" value="${esc(e.alta)}"></label>
    <label>${T('k_contract')}<select name="contrato" id="e-contrato">${opts(CONTRACTS.map(c => [c, t(ctKey(c))]), e.contrato || '')}</select></label>
  </div>`;
}
/* picking several of a list, like a device's drives: a menu per row, "add another" below, and remove on each row
   (hidden while there is only one, which can be left empty) */
const MULTI = {
  depts: { kind: 'departamentos', label: 'fe_depts', none: 'no_dept', add: 'add_dept', items: () => S.depts.map(x => [x.id, tx(x.nombre)]) },
  locs: { kind: 'ubicaciones', label: 'fe_locs', none: 'no_loc', add: 'add_loc', items: personLocs },
};
function multiRow(name, value) {
  const M = MULTI[name], i = ++nicSeq;
  return `<div class="multirow">${selPlus(M.kind, name, `e-${name}-${i}`, opts([['', t(M.none)], ...M.items()], value || ''))}<button type="button" class="btn small multi-del" aria-label="${T('nic_remove')}">${T('nic_remove')}</button></div>`;
}
function multiList(name, values) {
  const M = MULTI[name], rows = values && values.length ? values : [''];
  return `<div class="full multifield"><span class="multilabel">${T(M.label)}</span><div class="multilist" data-multi="${name}">${rows.map(v => multiRow(name, v)).join('')}</div>
    <div><button type="button" class="btn small" data-multi-add="${name}">${T(M.add)}</button></div></div>`;
}
const multiSync = list => { const rows = list.querySelectorAll('.multirow'); rows.forEach(r => { r.querySelector('.multi-del').hidden = rows.length < 2; }); };
document.addEventListener('click', e => {
  const del = e.target.closest('.multi-del'), add = e.target.closest('[data-multi-add]');
  if (del) { const list = del.closest('.multilist'); del.closest('.multirow').remove(); multiSync(list); list.querySelector('select')?.focus(); }
  if (add) {
    const list = add.closest('.multifield').querySelector('.multilist');
    list.insertAdjacentHTML('beforeend', multiRow(add.dataset.multiAdd, ''));
    multiSync(list); list.lastElementChild.querySelector('select').focus();
  }
});
const multiRead = (fd, name) => [...new Set(fd.getAll(name).filter(Boolean))];
function readEmployee(v, fd) { if (!v.nombre.trim() || !v.email.trim()) { toast(t('err_person')); return null; } return { nombre: v.nombre.trim(), email: v.email.trim(), depts: multiRead(fd, 'depts'), locs: multiRead(fd, 'locs'), alta: v.alta || today(), contrato: v.contrato || '' }; }
/* contract: not defined (''), indefinido, temporal or prácticas (the last two show a badge next to the name) */
const CONTRACTS = ['', 'indefinido', 'temporal', 'practicas'];
const ctKey = c => c ? 'ct_' + c : 'ct_unset';
const tempChip = e => e.contrato === 'temporal' || e.contrato === 'practicas' ? ` <span class="chip">${T('ct_' + e.contrato)}</span>` : '';

const ACTIONS = {
  nuevoDispositivo() {
    openDialog(t('new_device'), deviceForm(), async (v, fd) => {
      const data = readDevice(v, fd); if (!data) return false;
      const { device } = await mutate('POST', 'devices', data);
      location.hash = 'dispositivo-' + device.id; return t('created', { tag: device.tag });
    }, t('add'));
    bindHwForm();
    const tag = $('#f-tag'); tag.dataset.auto = tag.value;
  },
  editar(id) {
    const d = dev(id);
    openDialog(t('edit_title', { tag: d.tag }), deviceForm(d), async (v, fd) => {
      const data = readDevice(v, fd, d); if (!data) return false;
      await mutate('PUT', 'devices/' + d.id, data); return t('saved');
    });
    bindHwForm();
  },
  asignarDepto(id) { ACTIONS.asignar(id, 'dept'); },
  asignar(id, to = 'emp') {
    const d = dev(id);
    const people = S.employees.filter(e => empState(e) === 'activo').sort((a, b) => a.nombre.localeCompare(b.nombre, lang))
      .map(e => { const n = S.assignments.filter(a => a.employeeId === e.id && !a.hasta).length; return [e.id, `${e.nombre} · ${deptNames(e)}${n ? ' ' + t('already_has', { n }) : ''}`]; });
    openDialog(t(to === 'dept' ? 'assign_title_dept' : 'assign_title', { tag: d.tag }), `<div class="fields">
      <input type="hidden" name="to" value="${to}">
      <label class="full" id="a-empwrap"${to === 'dept' ? ' hidden' : ''}>${T('fa_emp')}<select name="emp" id="a-emp">${opts(people)}</select></label>
      <label class="full" id="a-deptwrap"${to === 'dept' ? '' : ' hidden'}>${T('fa_dept')}${selPlus('departamentos', 'dept', 'a-dept', opts(S.depts.map(x => [x.id, tx(x.nombre)])))}</label>
      <label>${T('fa_date')}<input type="date" name="desde" id="a-desde" value="${today()}"></label>
      <label>${T('fd_loc')}${selPlus('ubicaciones', 'loc', 'a-loc', opts(personLocs()))}</label>
      <label class="full">${T('fa_acc')}<input name="notas" id="a-notas" placeholder="${T('fa_acc_ph')}"></label></div>`, async v => {
      if (v.to === 'dept') {
        if (!v.dept) { toast(t('err_dept')); return false; }
        await mutate('POST', `devices/${d.id}/assign`, { deptId: v.dept, desde: v.desde, loc: v.loc, notas: v.notas }); return t('assigned_to', { name: deptName(v.dept) });
      }
      const e = emp(v.emp); if (!e) return false;
      await mutate('POST', `devices/${d.id}/assign`, { employeeId: e.id, desde: v.desde, loc: v.loc, notas: v.notas }); return t('assigned_to', { name: e.nombre });
    }, t('assign_btn'));
    // default the location to the chosen person's (first) workplace
    const sync = () => { const e = emp($('#a-emp').value), l = e && (e.locs || []).find(x => $('#a-loc').querySelector(`option[value="${x}"]`)); if (l) $('#a-loc').value = l; };
    $('#a-emp').onchange = sync; sync();
  },
  devolver(id) {
    const d = dev(id), a = openAsg(id);
    openDialog(t('return_title', { tag: d.tag }), `<p class="muted" style="margin:0 0 12px">${T('return_intro', { name: holderName(a), d: fmt(a.desde) })}</p><div class="fields">
      <label>${T('fr_date')}<input type="date" name="hasta" id="r-hasta" value="${today()}"></label>
      <label>${T('fr_cond')}<select name="condicion" id="r-cond">${kopts(CONDS, cd)}</select></label>
      <label class="full">${T('fr_next')}<select name="next" id="r-next">${opts([['disponible', t('next_avail')], ['reparacion', t('next_rep')], ['averiado', t('next_faulty')], ['descartado', t('next_disc')]])}</select></label>
      <label class="full">${T('notes')}<input name="notas" id="r-notas" placeholder="${T('fr_notes_ph')}"></label></div>`, async v => {
      await mutate('POST', `devices/${d.id}/return`, { hasta: v.hasta, condicion: v.condicion, next: v.next, notas: v.notas ? t('return_prefix') + v.notas : '' }); return t('return_done');
    }, t('ok_record'));
  },
  incidencia(id) {
    const d = dev(id);
    const ph = d.garantia && daysUntil(d.garantia) >= 0 ? t('in_war', { d: fmt(d.garantia) }) : t('out_war');
    openDialog(t('fault_title', { tag: d.tag }), `<div class="fields">
      <label>${T('fi_date')}<input type="date" name="fecha" id="i-fecha" value="${today()}"></label>
      <label>${T('fi_type')}<select name="tipo" id="i-tipo">${kopts(TIPOS_INC, itp)}</select></label>
      <label class="full">${T('fi_desc')}<textarea name="descripcion" id="i-desc"></textarea></label>
      <label>${T('fi_parts')}<input name="piezas" id="i-piezas"></label>
      <label>${T('fi_cost', { c: curSym() })}<input type="number" min="0" step="1" name="coste" id="i-coste" value="0"></label>
      <label class="full">${T('fi_tech')}<input name="proveedor" id="i-prov" placeholder="${esc(ph)}"></label>
      <label class="check full"><input type="checkbox" name="rep" id="i-rep"> ${T('fi_rep')}</label></div>`, async (v, fd) => {
      const desc = v.descripcion.trim();
      if (!desc) { toast(t('err_desc')); return false; }
      await mutate('POST', `devices/${d.id}/incidents`, { fecha: v.fecha, tipo: v.tipo, descripcion: desc, piezas: v.piezas, coste: Number(v.coste) || 0, proveedor: v.proveedor, rep: fd.has('rep') }); return t('fault_done');
    }, t('ok_record'));
  },
  resolver(iid) {
    const i = S.incidents.find(x => x.id === iid), d = dev(i.deviceId);
    openDialog(t('resolve_title'), `<p class="muted" style="margin:0 0 12px">${esc(tx(i.descripcion))}</p><div class="fields">
      <label>${T('fs_date')}<input type="date" name="resuelta" id="s-fecha" value="${today()}"></label>
      <label>${T('fs_cost', { c: curSym() })}<input type="number" min="0" step="1" name="coste" id="s-coste" value="${esc(i.coste)}"></label>
      <label class="full">${T('fi_parts')}<input name="piezas" id="s-piezas" value="${esc(tx(i.piezas))}"></label></div>`, async v => {
      await mutate('POST', `incidents/${i.id}/resolve`, { resuelta: v.resuelta, coste: Number(v.coste) || 0, piezas: v.piezas }); return t('resolve_done');
    }, t('ok_resolve'));
  },
  estado(id) {
    const d = dev(id), a = openAsg(id);
    const choices = ST.filter(k => k !== d.estado && (k !== 'uso' || a));
    openDialog(t('status_title', { tag: d.tag }), `<div class="fields">
      <label class="full">${T('fc_new')}<select name="estado" id="c-estado">${kopts(choices, st)}</select></label>
      ${a ? `<p class="full muted" style="margin:0">${T('fc_warn', { name: holderName(a) })}</p>` : ''}
      <div class="sect">${T('sect_disposal')}</div>
      <label>${T('fc_dest')}<select name="metodo" id="c-metodo">${kopts(DISPOSAL, dsp)}</select></label>
      <label>${T('fc_cert')}<input name="cert" id="c-cert" placeholder="BR-2026-0XX"></label>
      <label class="full">${T('fc_reason')}<input name="motivo" id="c-motivo"></label></div>`, async v => {
      const extra = v.estado === 'descartado' ? t('disc_note', { d: fmt(today()), m: dsp(v.metodo), c: v.cert.trim() }) : '';
      await mutate('POST', `devices/${d.id}/status`, { estado: v.estado, metodo: v.estado === 'descartado' ? v.metodo : '', cert: v.cert.trim(), motivo: v.motivo.trim(), note: extra }); return t('status_done');
    });
  },
  nuevoEmpleado() {
    openDialog(t('new_person'), employeeForm(), async (v, fd) => {
      const r = readEmployee(v, fd); if (!r) return false;
      const { employee } = await mutate('POST', 'employees', r);
      location.hash = 'empleado-' + employee.id; return t('person_added', { name: employee.nombre });
    }, t('add'));
  },
  editarEmpleado(id) {
    const e = emp(id);
    openDialog(t('edit_person', { name: e.nombre }), employeeForm(e), async (v, fd) => { const r = readEmployee(v, fd); if (!r) return false; await mutate('PUT', 'employees/' + e.id, r); return t('saved'); });
  },
  situacion(id) {
    const e = emp(id), ds = S.assignments.filter(a => a.employeeId === e.id && !a.hasta).map(a => dev(a.deviceId)).filter(Boolean);
    const tags = ds.map(d => d.tag).join(', ');
    openDialog(t('sit_title', { name: e.nombre }), `<div class="fields">
      <label>${T('fs_state')}<select name="estado" id="b-estado">${kopts(EMP_STATES, s => t('es_' + s), empState(e))}</select></label>
      <label id="b-fechawrap">${T('fs_since')}<input type="date" name="fecha" id="b-fecha" value="${esc(e.estadoFecha || today())}"></label>
      ${ds.length ? `<div class="notice full" id="b-pending">${T('fl_pending', { n: ds.length, tags })}</div>` : ''}</div>`, async v => {
      await mutate('POST', `employees/${e.id}/status`, { estado: v.estado, fecha: v.fecha });
      return t('sit_done');
    });
    const sync = () => { const s = $('#b-estado').value; $('#b-fechawrap').hidden = s === 'activo'; const p = $('#b-pending'); if (p) p.hidden = s !== 'salida'; };
    $('#b-estado').onchange = sync; sync();
  },

};

function closeMenus() {
  [['#userBtn', '#userMenu'], ['#addBtn', '#addMenu']].forEach(([b, m]) => { $(m).hidden = true; $(b).setAttribute('aria-expanded', 'false'); });
  document.querySelectorAll('#view [data-menu]').forEach(b => { b.setAttribute('aria-expanded', 'false'); const m = document.getElementById(b.dataset.menu); if (m) m.hidden = true; });
}
function toggleMenu(b, m) { const open = $(m).hidden; closeMenus(); if (open) { $(m).hidden = false; $(b).setAttribute('aria-expanded', 'true'); $(m).querySelector('.mi')?.focus(); } }
$('#userBtn').onclick = e => { e.stopPropagation(); toggleMenu('#userBtn', '#userMenu'); };
$('#addBtn').onclick = e => { e.stopPropagation(); toggleMenu('#addBtn', '#addMenu'); };
document.addEventListener('click', e => { if (!e.target.closest('.menu')) closeMenus(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenus(); });
$('#miSettings').addEventListener('click', closeMenus);
$('#addMenu').addEventListener('click', e => { const b = e.target.closest('[data-add]'); if (!b) return; closeMenus(); if (!can('edit')) return; b.dataset.add === 'device' ? ACTIONS.nuevoDispositivo() : ACTIONS.nuevoEmpleado(); });
$('#logoutBtn').onclick = async () => { closeMenus(); await api('POST', 'logout', {}).catch(() => {}); cur = null; S = emptyState(S.settings); location.hash = ''; applyChrome(); route(); };

/* ================= chrome ================= */
function applyChrome() {
  requestAnimationFrame(() => { const i = $('#tabs .tabind'); if (i) i.classList.remove('live'); moveTabInd(); });
  document.documentElement.lang = lang;
  document.title = t('brand');
  $('#brandName').textContent = t('brand');
  document.querySelectorAll('[data-i]').forEach(el => el.textContent = t(el.dataset.i));
  $('#langSeg').setAttribute('aria-label', t('lang_group'));
  $('#themeSeg').setAttribute('aria-label', t('theme_group'));
  document.querySelectorAll('#langSeg button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.lang === lang)));
  document.querySelectorAll('#themeSeg button').forEach(b => { const l = t('theme_' + b.dataset.themeSet); b.title = l; b.setAttribute('aria-label', l); });
  const inApp = !!cur && !cur.mustChange;   // a required password change looks like the sign-in page
  applyBrand();
  document.body.classList.toggle('authed', inApp);
  $('#tabs').hidden = !inApp; $('#userWrap').hidden = !inApp; $('#addWrap').hidden = !inApp || !can('edit'); $('#miSettings').hidden = !can('admin');
  // language + theme live in the account menu once signed in, in the header otherwise
  $(inApp ? '#langSlot' : '#prefSlot .row').appendChild($('#langSeg'));
  $(inApp ? '#themeSlot' : '#prefSlot .row').appendChild($('#themeSeg'));
  $(inApp ? '#uiSlot' : '#prefSlot .row').appendChild($('#uiSeg'));
  $('#mUiLbl').textContent = t('menu_ui'); $('#uiSeg').setAttribute('aria-label', t('menu_ui'));
  $('#prefSlot').hidden = inApp;
  $('#miSettingsTxt').textContent = t('settings'); $('#logoutTxt').textContent = t('logout');
  $('#installTxt').textContent = t('install_app'); updateInstallItem();
  $('#mLangLbl').textContent = t('menu_lang'); $('#mThemeLbl').textContent = t('menu_theme');
  $('#userBtn').setAttribute('aria-label', t('account_menu'));
  $('#addBtn').title = t('add_menu'); $('#addBtn').setAttribute('aria-label', t('add_menu'));
  $('#miAddDev').textContent = t('new_device'); $('#miAddDevD').textContent = t('add_device_d');
  $('#miAddPer').textContent = t('new_person'); $('#miAddPerD').textContent = t('add_person_d');
  if (cur) { $('#whoAvatar').textContent = initials(cur.nombre); $('#whoName').textContent = cur.nombre; $('#whoRole').textContent = rl(cur.rol); $('#mName').textContent = cur.nombre; $('#mEmail').textContent = cur.email; }
}
$('#langSeg').addEventListener('click', e => {
  const b = e.target.closest('[data-lang]'); if (!b || b.dataset.lang === lang) return;
  lang = b.dataset.lang; savePrefs(); applyChrome(); route();
});
$('#uiSeg').addEventListener('click', e => {
  const b = e.target.closest('[data-ui-set]'); if (!b) return;
  prefs.ui = b.dataset.uiSet; prefs.uiChosen = true; savePrefs(); applyUi(); const i = $('#tabs .tabind'); if (i) i.classList.remove('live'); moveTabInd();
});
$('#themeSeg').addEventListener('click', e => {
  const b = e.target.closest('[data-theme-set]'); if (!b) return;
  prefs.theme = b.dataset.themeSet; savePrefs(); applyTheme();
});

/* ================= routing ================= */
const view = $('#view');
view.addEventListener('click', ev => {
  const ig = ev.target.closest('[data-ignore]');
  if (ig) { if (can('edit')) ignoreCheck(ig.dataset.id, ig.dataset.ignore); return; }
  const ui = ev.target.closest('[data-unignore]');
  if (ui) { if (can('edit')) mutate('POST', `devices/${ui.dataset.unignore}/checks`, { reset: true }).then(route).catch(err => { if (err.status !== 401) toast(t(err.code)); }); return; }
  const rb = ev.target.closest('[data-reload]');
  if (rb) { reloadNow(rb); return; }
  const menuBtn = ev.target.closest('[data-menu]');
  if (menuBtn) { ev.stopPropagation(); toggleMenu('#' + menuBtn.id, '#' + menuBtn.dataset.menu); return; }
  const act = ev.target.closest('[data-act]');
  if (act) { closeMenus(); if (can('edit')) ACTIONS[act.dataset.act](act.dataset.id); return; }
  const s = ev.target.closest('[data-set]');
  if (s) { if (can('admin')) SET_ACTIONS[s.dataset.set](s.dataset.list, s.dataset.id); return; }
  const f = ev.target.closest('[data-filter]');
  if (f) { F.estado = f.dataset.filter; F.q = ''; F.dept = ''; F.tipo = ''; F.campo = ''; }
  if (ev.target.closest('a')) return;
  const go = ev.target.closest('[data-go]');
  if (go) location.hash = go.dataset.go;
});
function route() {
  if (cur && cur.mustChange) { renderPwChange(); document.querySelectorAll('#tabs a').forEach(a => a.classList.remove('on')); return; }
  if (!cur) { setupInfo ? renderSetup() : renderLogin(); document.querySelectorAll('#tabs a').forEach(a => a.classList.remove('on')); return; }
  const h = location.hash.slice(1) || 'panel';
  const sec = h.startsWith('dispositivo') ? 'dispositivos' : h.startsWith('empleado') ? 'empleados' : h.startsWith('ajustes') ? 'ajustes' : 'panel';
  document.querySelectorAll('#tabs a').forEach(a => a.classList.toggle('on', a.dataset.r === sec));
  if (h === 'dispositivos') {
    view.innerHTML = viewDevices(); drawDeviceRows();
    $('#fq').oninput = e => { F.q = e.target.value; drawDeviceRows(); };
    $('#festado').onchange = e => { F.estado = e.target.value; drawDeviceRows(); };
    $('#fdept').onchange = e => { F.dept = e.target.value; drawDeviceRows(); };
    $('#ftipo').onchange = e => { F.tipo = e.target.value; drawDeviceRows(); };
    $('#fcampo').onchange = e => { F.campo = e.target.value; $('#fq').placeholder = F.campo ? t('search_in', { x: t('sf_' + F.campo) }) : t('search_dev'); drawDeviceRows(); $('#fq').focus(); };
  } else if (h.startsWith('dispositivo-')) view.innerHTML = viewDevice(h.slice(12));
  else if (h === 'empleados') {
    view.innerHTML = viewEmployees(); drawEmpRows();
    $('#eq').oninput = e => { FE.q = e.target.value; drawEmpRows(); };
    $('#eactivos').onchange = e => { FE.activos = e.target.value; drawEmpRows(); };
    $('#econtrato').onchange = e => { FE.contrato = e.target.value; drawEmpRows(); };
  } else if (h.startsWith('empleado-')) view.innerHTML = viewEmployee(h.slice(9));
  else if (sec === 'ajustes') { view.innerHTML = viewSettings(h.slice(8)); bindRegion(); bindPwForm(); bindBrand(); bindData(); bindAbout(); bindUpdates(); }
  else view.innerHTML = viewPanel();
  requestAnimationFrame(moveTabInd);
}
window.addEventListener('hashchange', () => { route(); window.scrollTo(0, 0); enter(); });
/* other people's changes appear when you come back to the tab */
document.addEventListener('visibilitychange', async () => {
  if (document.visibilityState !== 'visible' || !cur || cur.mustChange || document.querySelector('dialog[open]')) return;
  try { await reload(); applyChrome(); route(); } catch (e) {}
});
(async () => {
  applyUi(); applyTheme();
  let underMaintenance = null;
  try {
    const d = await api('GET', 'bootstrap');
    if (d.maintenance) { underMaintenance = d.maintenance; S = emptyState(d.settings); }
    else if (d.me) adopt(d); else { S = emptyState(d.settings); setupInfo = d.setup || null; }
  } catch (e) { toast(t('err_network')); }
  applyChrome(); route(); enter();
  if (underMaintenance) enterMaintenance(underMaintenance);
  let updatedTo = null; try { updatedTo = sessionStorage.getItem('inv-updated'); sessionStorage.removeItem('inv-updated'); } catch (e) {}
  if (updatedTo && cur) toast(t('up_installed_toast', { v: updatedTo }), true);
})();
