FIRST, SECOND, THIRD = 2, 3, 4
FIRST_BOOSTER, SECOND_BOOSTER = 5, 9

RULES = [
    ("90585", None, None, "IAG_08", "BCG"),
    ("90585", None, None, "INMUNIZACIONES", "RN_BCG"),
    ("90744", None, None, "IAG_08", "HVB"),
    ("90744", None, None, "INMUNIZACIONES", "RN_HVB"),
    ("36416", None, None, "IAG_08", "TAMIZAJE"),
    ("99381.01", None, "1", "IAG_08", "CRED_RN_1"),
    ("99381.01", None, "2", "IAG_08", "CRED_RN_2"),
    ("99381.01", None, "3", "IAG_08", "CRED_RN_3"),
    ("99381.01", None, "4", "IAG_08", "CRED_RN_4"),
    ("99381.01", None, None, "IAG_10", "CRED_RN"),
    ("99502", None, None, "IAG_11", "VISITA_RN"),
    ("C0011", None, None, "IAG_08", "VISITA_FAMILIAR"),
    ("99401.03", None, None, "IAG_08", "VISITA_LACTANCIA"),
    ("99401.04", None, None, "IAG_08", "VISITA_CORDON"),
    ("99401.08", None, None, "IAG_08", "VISITA_ALARMA"),
    ("99401.10", None, None, "IAG_08", "VISITA_HIGIENE"),
    ("99381", None, None, "IAG_10", "CRED_MENOR"),
    ("90722", FIRST, None, "INMUNIZACIONES", "PENTA1"),
    ("90722", SECOND, None, "INMUNIZACIONES", "PENTA2"),
    ("90722", THIRD, None, "INMUNIZACIONES", "PENTA3"),
    ("90722", None, None, "IAG_10", "PENTA"),
    ("90713", FIRST, None, "INMUNIZACIONES", "IPV1"),
    ("90713", SECOND, None, "INMUNIZACIONES", "IPV2"),
    ("90713", THIRD, None, "INMUNIZACIONES", "IPV3"),
    ("90713", None, None, "IAG_10", "IPV"),
    ("90681", FIRST, None, "INMUNIZACIONES", "ROTAVIRUS1"),
    ("90681", SECOND, None, "INMUNIZACIONES", "ROTAVIRUS2"),
    ("90681", None, None, "IAG_10", "ROTAVIRUS"),
    ("90670", FIRST, None, "INMUNIZACIONES", "NEUMO1"),
    ("90670", SECOND, None, "INMUNIZACIONES", "NEUMO2"),
    ("90670", None, None, "IAG_10", "NEUMO"),
    ("90657", None, None, "INMUNIZACIONES", "INFLUENZA"),
    ("90655", None, None, "INMUNIZACIONES", "INFLUENZA"),
    ("90685", None, None, "INMUNIZACIONES", "INFLUENZA"),
    ("90707", FIRST, None, "INMUNIZACIONES", "SPR1"),
    ("90701", FIRST_BOOSTER, None, "INMUNIZACIONES", "DPT1"),
    ("90701", SECOND_BOOSTER, None, "IAG_20", "INMUNIZACION_4"),
    ("90649", None, None, "IAG_25", "VPH"),
    ("90651", None, None, "IAG_25", "VPH"),
    ("85018.01", None, None, "IAG_09", "HB_PREMATURO"),
    ("85018.01", None, None, "IAG_10", "HB"),
    ("85018.01", None, None, "IAG_13", "HB_1"),
    ("85018.01", None, None, "IAG_17", "HB_2"),
    ("85018.01", None, None, "IAG_19", "HB_3"),
    ("85018.01", None, None, "IAG_20", "HB_4"),
    ("85018.01", None, None, "IAG_25", "HB_5_11"),
    ("85018", None, None, "IAG_10", "HB"),
    ("85018", None, None, "IAG_13", "HB_1"),
    ("85018", None, None, "IAG_17", "HB_2"),
    ("85018", None, None, "IAG_19", "HB_3"),
    ("85018", None, None, "IAG_20", "HB_4"),
    ("85018", None, None, "IAG_25", "HB_5_11"),
    ("99199.17", None, None, "IAG_09", "HIERRO_PREMATURO"),
    ("99199.17", None, None, "IAG_10", "HIERRO"),
    ("99199.17", None, None, "IAG_13", "HIERRO_1"),
    ("99199.17", None, None, "IAG_17", "HIERRO_2"),
    ("99199.17", None, None, "IAG_19", "HIERRO_3"),
    ("99199.17", None, None, "IAG_20", "HIERRO_4"),
    ("Z2982", None, None, "IAG_10", "SOFE"),
    ("Z2982", None, "TA", "IAG_25", "SOFE_TA"),
    ("Z2982", None, None, "IAG_25", "SOFE1"),
    ("Z2982", None, None, "IAG_25", "SOFE2"),
    ("Z2982", None, None, "IAG_25", "SOFE3"),
    ("C0011", None, None, "IAG_11", "VISITA_4M"),
    ("C0011", None, None, "IAG_11", "VISITA_6M"),
    ("C0011", None, None, "IAG_11", "VISITA_8M"),
    ("C0011", None, None, "IAG_11", "VISITA_9M"),
    ("C0010", None, "ALI", "IAG_26", "ALI"),
    ("C0010", None, "GL", "IAG_26", "ALI_GOBIERNO_LOCAL"),
    ("99382", None, None, "IAG_13", "CRED_1"),
    ("99382", None, None, "IAG_17", "CRED_2"),
    ("99382", None, None, "IAG_19", "CRED_3"),
    ("99382", None, None, "IAG_20", "CRED_4"),
    ("99383", None, None, "IAG_25", "CRED_5_11"),
    ("99199.28", None, None, "IAG_17", "ANTIPARASITARIO_2"),
    ("99199.28", None, None, "IAG_19", "ANTIPARASITARIO_3"),
    ("99199.28", None, None, "IAG_20", "ANTIPARASITARIO_4"),
    ("99199.28", None, None, "IAG_25", "ANTIPARASITARIO_5_11"),
    ("D0150", None, None, "AG_21", "EVAL_ORAL"),
    ("D1206", None, None, "AG_21", "PAQ_ODONT_1"),
    ("D1206", None, None, "AG_21", "PAQ_ODONT_2"),
]


async def seed_his_rules(conn) -> int:
    saved = 0
    for priority, (his_code, dose_id, lab_value, package_code, service_code) in enumerate(RULES):
        row = await conn.fetchrow(
            """
            INSERT INTO his_service_rules (his_code, dose_id, lab_value, service_id, priority)
            SELECT $1, $2, $3, s.id, $6
            FROM care_services s
            JOIN care_packages p ON p.id = s.package_id
            WHERE p.code = $4 AND s.code = $5
            ON CONFLICT ON CONSTRAINT uq_his_service_rules DO NOTHING
            RETURNING id
            """,
            his_code,
            dose_id,
            lab_value,
            package_code,
            service_code,
            priority,
        )
        saved += row is not None

    print(f"reglas HIS -> SICNA: {saved} nuevas de {len(RULES)}")
    return saved
