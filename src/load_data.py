import pandas as pd
from sqlalchemy import create_engine

DB_URL   = "postgresql://shivanshpandey:admin123@127.0.0.1:5432/hospital_readmission"
CSV_PATH = "data/raw/diabetic_data.csv"
engine   = create_engine(DB_URL)

print("Loading CSV...")
df = pd.read_csv(CSV_PATH)
print(f"   Loaded {len(df):,} rows x {df.shape[1]} columns")

# Clean ? values
df.replace("?", None, inplace=True)

# ── patients: unique patients only (71K) ──────────
print("\nInserting patients...")
patients = df.drop_duplicates(subset="patient_nbr", keep="first")[
    ["patient_nbr","race","gender","age"]
].copy()
patients.to_sql("patients", engine, if_exists="append",
                index=False, chunksize=500)
print(f"   Done: {len(patients):,} unique patients")

# ── encounters: ALL 101K rows ─────────────────────
print("\nInserting encounters...")
enc_cols = [
    "encounter_id","patient_nbr","admission_type_id",
    "discharge_disposition_id","admission_source_id",
    "time_in_hospital","num_lab_procedures","num_procedures",
    "num_medications","number_outpatient","number_emergency",
    "number_inpatient","number_diagnoses",
    "diag_1","diag_2","diag_3",
    "A1Cresult","insulin","change","diabetesMed"
]
enc = df[enc_cols].rename(columns={
    "A1Cresult"  : "a1c_result",
    "change"     : "change_in_meds",
    "diabetesMed": "diabetes_med"
})
enc.to_sql("encounters", engine, if_exists="append",
           index=False, chunksize=500)
print(f"   Done: {len(enc):,} encounters")

# ── readmission labels: ALL 101K rows ─────────────
print("\nInserting labels...")
labels = df[["encounter_id","readmitted"]].copy()
labels.rename(columns={"readmitted":"readmitted_raw"}, inplace=True)
labels["readmitted_30d"] = (labels["readmitted_raw"] == "<30").astype(int)
labels.to_sql("readmission_labels", engine, if_exists="append",
              index=False, chunksize=500)

rate = labels["readmitted_30d"].mean() * 100
print(f"   Done: {len(labels):,} labels")
print(f"   Readmission rate: {rate:.1f}%")
print("\nAll data loaded successfully!")