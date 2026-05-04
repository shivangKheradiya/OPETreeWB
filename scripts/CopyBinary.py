import psycopg2
import os

# --------------------
# Configuration
# --------------------
OUTPUT_FILE = r"C:\db\dict_data.bin"   # ✅ change folder if needed

src_conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="xyz",
    user="postgres",
    password="postgres"
)

src_cur = src_conn.cursor()

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# --------------------
# Binary COPY to file
# --------------------
with open(OUTPUT_FILE, "wb") as f:
    src_cur.copy_expert(
        """
        COPY public.dict_data
        TO STDOUT WITH BINARY
        """,
        f
    )

# Cleanup
src_cur.close()
src_conn.close()

print(f"✅ Binary COPY saved successfully to: {OUTPUT_FILE}")


import psycopg2
import os

# --------------------
# Configuration
# --------------------
BIN_FILE = r"C:\db\dict_data.bin"    # path to saved binary file

dst_conn = psycopg2.connect(
    host="localhost",
    port=5433,          # destination PostgreSQL port
    dbname="xyz",
    user="postgres",
    password="postgres"
)

dst_cur = dst_conn.cursor()

# --------------------
# Validate file exists
# --------------------
if not os.path.exists(BIN_FILE):
    raise FileNotFoundError(f"Binary file not found: {BIN_FILE}")

# --------------------
# Load binary data
# --------------------
with open(BIN_FILE, "rb") as f:

    # OPTIONAL but recommended for full reload
    dst_cur.execute("TRUNCATE TABLE public.dict_data")

    # Import data
    dst_cur.copy_expert(
        """
        COPY public.dict_data
        FROM STDIN WITH BINARY
        """,
        f
    )

dst_conn.commit()

dst_cur.close()
dst_conn.close()

print("✅ Binary data loaded into PostgreSQL successfully")