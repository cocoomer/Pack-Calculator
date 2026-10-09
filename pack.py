import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="GT Pack Profit Calculator", page_icon="📦", layout="centered"
)

st.title("📦 Growtopia - Pack Profit Calculator")
st.write(
    "Kalkulator profit interaktif untuk Galactic Goodies dan Surgical Tools."
)

st.divider()

# 1. SETUP 3 MATRIKS UTAMA
st.subheader("Data Taking")
col1, col2, col3 = st.columns(3)

with col1:
    total_wl_modal = st.number_input(
        "1. Modal (in WL)", min_value=1, value=1000, step=1
    )
with col2:
    nama_pack = st.selectbox(
        "2. Select Pack", ["Galactic Goodies", "Surgical Tools"]
    )
with col3:
    harga_pack_wl = st.number_input(
        "3. Pack Price (WL)", min_value=1, value=2, step=1
    )

jumlah_pack = total_wl_modal // harga_pack_wl
sisa_wl = total_wl_modal % harga_pack_wl

st.info(
    f"💡 With **{total_wl_modal} WL**, you can buy **{jumlah_pack:,} Pack** (Remainder: **{sisa_wl} WL**)."
)

st.divider()

# 2. INISIALISASI DATA BERDASARKAN PACK YANG DIPILIH
session_key = f"df_tools_{nama_pack}"

if (
    session_key not in st.session_state
    or st.session_state.get("last_jumlah_pack") != jumlah_pack
    or st.session_state.get("last_pack_type") != nama_pack
):
    if nama_pack == "Galactic Goodies":
        tools_data = [
            {"Tools Name": "AI Brain", "Rate/Pack": 5, "Select Categories": "Items/WL", "Price in WL": 8.0},
            {"Tools Name": "Cyborg Diplomat", "Rate/Pack": 5, "Select Categories": "Items/WL", "Price in WL": 7.0},
            {"Tools Name": "Galacticbolt", "Rate/Pack": 5, "Select Categories": "Items/WL", "Price in WL": 8.0},
            {"Tools Name": "Gigablaster", "Rate/Pack": 5, "Select Categories": "Items/WL", "Price in WL": 8.0},
            {"Tools Name": "Growton Torpedo", "Rate/Pack": 5, "Select Categories": "Items/WL", "Price in WL": 5.0},
            {"Tools Name": "Hyper Shields", "Rate/Pack": 5, "Select Categories": "Items/WL", "Price in WL": 7.0},
            {"Tools Name": "Quadriscanner", "Rate/Pack": 5, "Select Categories": "Items/WL", "Price in WL": 7.0},
            {"Tools Name": "Space Meds", "Rate/Pack": 5, "Select Categories": "Items/WL", "Price in WL": 8.0},
            {"Tools Name": "Star Supplies", "Rate/Pack": 5, "Select Categories": "Items/WL", "Price in WL": 8.0},
            {"Tools Name": "Stellar Documents", "Rate/Pack": 5, "Select Categories": "Items/WL", "Price in WL": 7.0},
            {"Tools Name": "Starfuel", "Rate/Pack": 25, "Select Categories": "Items/WL", "Price in WL": 50.0},
            {"Tools Name": "Tactical Drone", "Rate/Pack": 5, "Select Categories": "Items/WL", "Price in WL": 3.0},
            {"Tools Name": "Teleporter Charge", "Rate/Pack": 5, "Select Categories": "WL/Items", "Price in WL": 2.0},
        ]
    else:
        tools_data = [
            {"Tools Name": "Surg-E", "Rate/Pack": 5, "Select Categories": "Items/WL", "Price in WL": 5.0},
            {"Tools Name": "Surgical Anesthetic", "Rate/Pack": 20, "Select Categories": "Items/WL", "Price in WL": 12.0},
            {"Tools Name": "Surgical Antibiotics", "Rate/Pack": 20, "Select Categories": "Items/WL", "Price in WL": 9.0},
            {"Tools Name": "Surgical Antiseptic", "Rate/Pack": 20, "Select Categories": "Items/WL", "Price in WL": 13.0},
            {"Tools Name": "Surgical Clamp", "Rate/Pack": 20, "Select Categories": "Items/WL", "Price in WL": 13.0},
            {"Tools Name": "Surgical Defibrillator", "Rate/Pack": 20, "Select Categories": "Items/WL", "Price in WL": 13.0},
            {"Tools Name": "Surgical Lab Kit", "Rate/Pack": 20, "Select Categories": "Items/WL", "Price in WL": 13.0},
            {"Tools Name": "Surgical Pins", "Rate/Pack": 20, "Select Categories": "Items/WL", "Price in WL": 13.0},
            {"Tools Name": "Surgical Scalpel", "Rate/Pack": 20, "Select Categories": "Items/WL", "Price in WL": 9.0},
            {"Tools Name": "Surgical Splint", "Rate/Pack": 20, "Select Categories": "Items/WL", "Price in WL": 13.0},
            {"Tools Name": "Surgical Sponge", "Rate/Pack": 20, "Select Categories": "Items/WL", "Price in WL": 10.0},
            {"Tools Name": "Surgical Stitches", "Rate/Pack": 20, "Select Categories": "Items/WL", "Price in WL": 1.14},
            {"Tools Name": "Surgical Transfusion", "Rate/Pack": 20, "Select Categories": "Items/WL", "Price in WL": 13.0},
            {"Tools Name": "Surgical Ultrasound", "Rate/Pack": 20, "Select Categories": "Items/WL", "Price in WL": 13.0},
        ]

    df_initial = pd.DataFrame(tools_data)
    df_initial["Total Tools Obtained"] = df_initial["Rate/Pack"] * jumlah_pack
    st.session_state[session_key] = df_initial
    st.session_state["last_jumlah_pack"] = jumlah_pack
    st.session_state["last_pack_type"] = nama_pack
else:
    st.session_state[session_key]["Total Tools Obtained"] = (
        st.session_state[session_key]["Rate/Pack"] * jumlah_pack
    )

st.subheader(f"Profit Summary {nama_pack} & Revenue")
st.write("Select Categories Info:")
st.write("- Items/WL: How much items you get with 1 WL.")
st.write("- WL/Items: How much WL you need to buy 1 item.")
st.write("- Price in WL: Can be written in decimal if necessary.")

col_cfg = {
    "Tools Name": st.column_config.TextColumn("Tools Name", disabled=True),
    "Rate/Pack": None,
    "Total Tools Obtained": st.column_config.NumberColumn(
        "Total Tools Obtained", format="%d pcs", disabled=True
    ),
    "Select Categories": st.column_config.SelectboxColumn(
        "Select Categories",
        options=["Items/WL", "WL/Items"],
        required=True,
    ),
    "Price in WL": st.column_config.NumberColumn(
        "Price in WL", min_value=0.01, step=0.01, format="%.2f"
    ),
}

editor_key = f"editor_tabel_{nama_pack}"
edited_df = st.data_editor(
    st.session_state[session_key],
    column_config=col_cfg,
    hide_index=True,
    use_container_width=True,
    key=editor_key,
)

# Simpan state tabel yang diedit ke session state
st.session_state[session_key] = edited_df

st.divider()

# TOMBOL PERTAMA: Cek Profit Summary (Setting Harga)
if st.button("📊 Check Profit Summary (Set Prices)", use_container_width=True):
    st.success("Prices saved successfully! You can check the total profit below.")

st.divider()

# TOMBOL KEDUA: Cek Total Profit
if st.button("🚀 Check Total Profit Calculation", use_container_width=True):
    if jumlah_pack <= 0:
        st.error("Modal WL is not enough to buy 1 pack!")
    else:
        calc_df = st.session_state[session_key].copy()
        unit_price_list = []
        revenue_list = []

        for index, row in calc_df.iterrows():
            kategori = row["Select Categories"]
            val = float(row["Price in WL"])
            if val <= 0:
                val = 0.01

            if kategori == "Items/WL":
                unit_price = 1.0 / val
            else:
                unit_price = val

            unit_price_list.append(unit_price)
            revenue_list.append(row["Total Tools Obtained"] * unit_price)

        calc_df["Unit Price"] = unit_price_list
        calc_df["Est. Revenue (WL)"] = revenue_list

        total_pendapatan_barang = calc_df["Est. Revenue (WL)"].sum()
        total_pendapatan_akhir = total_pendapatan_barang + sisa_wl
        profit = total_pendapatan_akhir - total_wl_modal

        col_res1, col_res2 = st.columns(2)
        col_res1.metric(
            label="Total Final Income",
            value=f"{total_pendapatan_akhir:.2f} WL",
        )
        col_res2.metric(
            label="Profit / Loss Estimation",
            value=f"{profit:+.2f} WL",
            delta=f"{profit/100:+.2f} DL",
        )

        st.subheader("📋 Selling Summary")
        res_cfg = {
            "Total Tools Obtained": st.column_config.NumberColumn(
                format="%d pcs"
            ),
            "Price in WL": st.column_config.NumberColumn(format="%.2f"),
            "Est. Revenue (WL)": st.column_config.NumberColumn(
                format="%.2f WL"
            ),
        }
        res_columns = [
            "Tools Name",
            "Total Tools Obtained",
            "Select Categories",
            "Price in WL",
            "Est. Revenue (WL)",
        ]
        st.dataframe(
            calc_df[res_columns],
            column_config=res_cfg,
            hide_index=True,
            use_container_width=True,
        )